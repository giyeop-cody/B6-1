#!/usr/bin/env python3
"""B6-1 files and security invariants that can be checked without AWS or Docker."""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def read(relative: str) -> str:
    path = ROOT / relative
    check(path.is_file(), f"required file missing: {relative}")
    return path.read_text(encoding="utf-8") if path.is_file() else ""


required = [
    "Dockerfile",
    "nginx/default.conf",
    "site/index.html",
    "site/styles.css",
    "site/app.js",
    "infra/cloudformation.yml",
    "infra/deployer-policy.json",
    "docs/architecture.svg",
    "docs/account-setup.md",
    "docs/deployment-guide.md",
    "docs/troubleshooting.md",
    "docs/cleanup-checklist.md",
    "evidence/README.md",
]
for item in required:
    read(item)

# Container and application
nginx = read("nginx/default.conf")
dockerfile = read("Dockerfile")
index = read("site/index.html")
check("location = /health" in nginx, "Nginx exact /health location is missing")
check('return 200 "OK\\n"' in nginx, "Nginx /health must return 200 OK")
check("HEALTHCHECK" in dockerfile, "Docker HEALTHCHECK is missing")
check("EXPOSE 80" in dockerfile, "Docker port 80 is not documented")
check("B6-1 Cloud Lab" in index, "site identity is missing")
check("https://" not in index, "site must not depend on an external HTTPS asset")

# CloudFormation syntax and resources
try:
    template = yaml.safe_load(read("infra/cloudformation.yml"))
except Exception as exc:  # pragma: no cover - used as CLI
    template = {}
    ERRORS.append(f"CloudFormation YAML parse failed: {exc}")

resources = template.get("Resources", {}) if isinstance(template, dict) else {}
expected_types = {
    "Vpc": "AWS::EC2::VPC",
    "InternetGateway": "AWS::EC2::InternetGateway",
    "InternetGatewayAttachment": "AWS::EC2::VPCGatewayAttachment",
    "PublicSubnet": "AWS::EC2::Subnet",
    "PublicRouteTable": "AWS::EC2::RouteTable",
    "DefaultPublicRoute": "AWS::EC2::Route",
    "PublicSubnetRouteTableAssociation": "AWS::EC2::SubnetRouteTableAssociation",
    "WebSecurityGroup": "AWS::EC2::SecurityGroup",
    "WebInstance": "AWS::EC2::Instance",
}
for logical_id, resource_type in expected_types.items():
    check(resources.get(logical_id, {}).get("Type") == resource_type, f"{logical_id} type must be {resource_type}")

params = template.get("Parameters", {})
check(params.get("InstanceType", {}).get("Default") == "t3.micro", "default instance must be t3.micro")
check(params.get("AllowedSshCidr", {}).get("Default") != "0.0.0.0/0", "SSH default must not be public")
check("RejectPublicSsh" in template.get("Rules", {}), "public SSH rejection Rule is missing")

route = resources.get("DefaultPublicRoute", {}).get("Properties", {})
check(route.get("DestinationCidrBlock") == "0.0.0.0/0", "public route destination is missing")
check(route.get("GatewayId") == {"Ref": "InternetGateway"}, "public route must use InternetGateway")

sg = resources.get("WebSecurityGroup", {}).get("Properties", {})
ingress = sg.get("SecurityGroupIngress", [])
http_rules = [r for r in ingress if r.get("FromPort") == 80 and r.get("ToPort") == 80]
ssh_rules = [r for r in ingress if r.get("FromPort") == 22 and r.get("ToPort") == 22]
check(len(http_rules) == 1 and http_rules[0].get("CidrIp") == "0.0.0.0/0", "HTTP 80 must be public exactly once")
check(len(ssh_rules) == 1 and ssh_rules[0].get("CidrIp") == {"Ref": "AllowedSshCidr"}, "SSH must use AllowedSshCidr")
check(not any(r.get("FromPort") == 0 and r.get("ToPort") == 65535 for r in ingress), "all TCP ports must not be public")

instance = resources.get("WebInstance", {}).get("Properties", {})
check(instance.get("MetadataOptions", {}).get("HttpTokens") == "required", "IMDSv2 must be required")
block = instance.get("BlockDeviceMappings", [{}])[0].get("Ebs", {})
check(block.get("VolumeSize") == 8, "EBS must start at 8GiB")
check(block.get("VolumeType") == "gp3", "EBS must use gp3")
check(block.get("Encrypted") is True, "EBS must be encrypted")
check(block.get("DeleteOnTermination") is True, "EBS must delete with the instance")

user_data = (
    instance.get("UserData", {})
    .get("Fn::Base64", {})
    .get("Fn::Sub", "")
)
for token in ["dnf install -y docker", "git clone", "docker build", "docker run", "cfn-signal"]:
    check(token in user_data, f"UserData missing: {token}")

outputs = template.get("Outputs", {})
for key in ["WebsiteURL", "HealthURL", "PublicIp", "InstanceId", "VpcId", "PublicSubnetId", "SecurityGroupId"]:
    check(key in outputs, f"CloudFormation output missing: {key}")

# IAM policy must be action-limited and region-constrained for EC2 writes.
try:
    policy = json.loads(read("infra/deployer-policy.json"))
except Exception as exc:
    policy = {}
    ERRORS.append(f"IAM policy JSON parse failed: {exc}")

statements = policy.get("Statement", [])
for statement in statements:
    if statement.get("Effect") != "Allow":
        continue
    actions = statement.get("Action", [])
    if isinstance(actions, str):
        actions = [actions]
    check("*" not in actions and "ec2:*" not in actions and "iam:*" not in actions, "Allow statement contains wildcard administration")
check(any(s.get("Sid") == "DenyEc2OutsideSeoul" and s.get("Effect") == "Deny" for s in statements), "Seoul region deny guard is missing")

# SVG must be a real parseable diagram.
try:
    ET.parse(ROOT / "docs/architecture.svg")
except Exception as exc:
    ERRORS.append(f"architecture SVG parse failed: {exc}")

if ERRORS:
    for error in ERRORS:
        print(f"FAIL: {error}", file=sys.stderr)
    print(f"B6-1 STATIC VALIDATION: {len(ERRORS)} FAILURE(S)", file=sys.stderr)
    raise SystemExit(1)

print(f"required_files={len(required)} PASS")
print(f"cloudformation_resources={len(expected_types)} PASS")
print("security_group=http80_public+ssh22_parameterized PASS")
print("ebs=8GiB_gp3_encrypted_delete_on_termination PASS")
print("iam=no_allow_wildcard+seoul_deny_guard PASS")
print("B6-1 STATIC VALIDATION: ALL PASS")
