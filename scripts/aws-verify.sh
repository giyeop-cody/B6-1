#!/usr/bin/env bash
set -euo pipefail

STACK_NAME="${1:-b6-1-learning}"
REGION="ap-northeast-2"

for command in aws curl python3; do
  command -v "$command" >/dev/null 2>&1 || { echo "FAIL: ${command}가 필요합니다." >&2; exit 2; }
done

output() {
  local key="$1"
  aws cloudformation describe-stacks \
    --region "$REGION" \
    --stack-name "$STACK_NAME" \
    --query "Stacks[0].Outputs[?OutputKey=='${key}'].OutputValue | [0]" \
    --output text
}

STATUS="$(aws cloudformation describe-stacks --region "$REGION" --stack-name "$STACK_NAME" --query 'Stacks[0].StackStatus' --output text)"
case "$STATUS" in
  CREATE_COMPLETE|UPDATE_COMPLETE) ;;
  *) echo "FAIL: Stack 상태가 완료가 아닙니다: ${STATUS}" >&2; exit 1 ;;
esac

WEBSITE_URL="$(output WebsiteURL)"
HEALTH_URL="$(output HealthURL)"
INSTANCE_ID="$(output InstanceId)"
VPC_ID="$(output VpcId)"
SUBNET_ID="$(output PublicSubnetId)"
SG_ID="$(output SecurityGroupId)"

[[ "$WEBSITE_URL" == http://* ]] || { echo "FAIL: WebsiteURL 출력 없음" >&2; exit 1; }
[[ "$HEALTH_URL" == http://*/health ]] || { echo "FAIL: HealthURL 출력 없음" >&2; exit 1; }

STATE="$(aws ec2 describe-instances --region "$REGION" --instance-ids "$INSTANCE_ID" --query 'Reservations[0].Instances[0].State.Name' --output text)"
[[ "$STATE" == "running" ]] || { echo "FAIL: EC2 state=${STATE}" >&2; exit 1; }

ACTUAL_VPC="$(aws ec2 describe-instances --region "$REGION" --instance-ids "$INSTANCE_ID" --query 'Reservations[0].Instances[0].VpcId' --output text)"
ACTUAL_SUBNET="$(aws ec2 describe-instances --region "$REGION" --instance-ids "$INSTANCE_ID" --query 'Reservations[0].Instances[0].SubnetId' --output text)"
[[ "$ACTUAL_VPC" == "$VPC_ID" && "$ACTUAL_SUBNET" == "$SUBNET_ID" ]] || { echo "FAIL: EC2 network mismatch" >&2; exit 1; }

HTTP_CIDR="$(aws ec2 describe-security-groups --region "$REGION" --group-ids "$SG_ID" --query 'SecurityGroups[0].IpPermissions[?FromPort==`80` && ToPort==`80`].IpRanges[].CidrIp' --output text)"
SSH_CIDR="$(aws ec2 describe-security-groups --region "$REGION" --group-ids "$SG_ID" --query 'SecurityGroups[0].IpPermissions[?FromPort==`22` && ToPort==`22`].IpRanges[].CidrIp' --output text)"
[[ "$HTTP_CIDR" == *"0.0.0.0/0"* ]] || { echo "FAIL: HTTP 80 public rule missing" >&2; exit 1; }
[[ -n "$SSH_CIDR" && "$SSH_CIDR" != *"0.0.0.0/0"* ]] || { echo "FAIL: SSH rule missing or public" >&2; exit 1; }

ROUTE_GATEWAY="$(aws ec2 describe-route-tables --region "$REGION" --filters "Name=association.subnet-id,Values=${SUBNET_ID}" --query "RouteTables[0].Routes[?DestinationCidrBlock=='0.0.0.0/0'].GatewayId | [0]" --output text)"
[[ "$ROUTE_GATEWAY" == igw-* ]] || { echo "FAIL: public subnet IGW route missing" >&2; exit 1; }

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
HTTP_CODE="$(curl --connect-timeout 5 --max-time 15 -sS -o "$TMP_DIR/home.html" -w '%{http_code}' "$WEBSITE_URL")"
HEALTH_BODY="$(curl --connect-timeout 5 --max-time 15 -fsS "$HEALTH_URL" | tr -d '\r\n')"
[[ "$HTTP_CODE" == "200" ]] || { echo "FAIL: website HTTP ${HTTP_CODE}" >&2; exit 1; }
[[ "$HEALTH_BODY" == "OK" ]] || { echo "FAIL: health body=${HEALTH_BODY}" >&2; exit 1; }
grep -q "인터넷에서" "$TMP_DIR/home.html" || { echo "FAIL: deployed page identity mismatch" >&2; exit 1; }

printf '%s\n' \
  "timestamp=$(date -u '+%Y-%m-%dT%H:%M:%SZ')" \
  "region=${REGION}" \
  "stack=${STACK_NAME}" \
  "stack_status=${STATUS} PASS" \
  "ec2_state=${STATE} PASS" \
  "vpc_and_subnet=PASS" \
  "route_0.0.0.0/0_to_igw=PASS" \
  "http_80_public=PASS" \
  "ssh_22_private=PASS" \
  "website_http_200=PASS" \
  "health_ok=PASS" \
  "B6-1 AWS VERIFICATION: ALL PASS"
