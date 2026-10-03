"""Prepare the historical template for current restrictive deployment permissions."""
from pathlib import Path
import yaml

root = Path(__file__).resolve().parents[1]
path = root / "infra/cloudformation.yml"
template = yaml.safe_load(path.read_text(encoding="utf-8"))
template["Parameters"]["ProjectName"].pop("AllowedPattern", None)
template["Parameters"]["ProjectName"]["AllowedValues"] = ["b6-1"]
template["Parameters"]["InstanceType"]["AllowedValues"] = ["t3.micro"]
template["Parameters"]["AllowedSshCidr"]["AllowedPattern"] = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/32$"
resources = template["Resources"]
resources["LaunchTags"] = {
    "Type": "AWS::EC2::LaunchTemplate",
    "Properties": {
        "TagSpecifications": [{"ResourceType": "launch-template", "Tags": [
            {"Key": "Project", "Value": "b6-1"}]}],
        "LaunchTemplateData": {
            "TagSpecifications": [{"ResourceType": kind, "Tags": [
                {"Key": "Project", "Value": "b6-1"}]} for kind in ["volume", "network-interface"]]
        }
    }
}
instance = resources["WebInstance"]["Properties"]
instance["LaunchTemplate"] = {
    "LaunchTemplateId": {"Ref": "LaunchTags"},
    "Version": {"Fn::GetAtt": ["LaunchTags", "LatestVersionNumber"]}}
instance["CreditSpecification"] = {"CPUCredits": "standard"}
script = instance["UserData"]["Fn::Base64"]["Fn::Sub"]
script = script.replace(
    "git clone --depth 1 https://github.com/giyeop-cody/B6-1.git /opt/b6-1",
    "git init /opt/b6-1\n"
    "git -C /opt/b6-1 remote add origin https://github.com/giyeop-cody/B6-1.git\n"
    "git -C /opt/b6-1 fetch --depth 1 origin 6bc1076c4311cc2685b483ca326be8bc7e5f4bb1\n"
    "git -C /opt/b6-1 checkout --detach FETCH_HEAD\n"
    "git -C /opt/b6-1 rev-parse HEAD > /opt/b6-1-deployed-commit.txt")
instance["UserData"]["Fn::Base64"]["Fn::Sub"] = script
path.write_text(yaml.safe_dump(template, sort_keys=False, allow_unicode=True), encoding="utf-8")
print("Prepared: historical app pinned, SSH /32, t3.micro, tagged EBS/ENI, standard CPU credits")
