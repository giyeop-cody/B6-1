import json
import boto3
from pathlib import Path

region = 'ap-northeast-2'
iam = boto3.client('iam')
ec2 = boto3.client('ec2', region_name=region)
account = boto3.client('sts').get_caller_identity()['Account']
assert account == '171180524802'
policy = json.loads(Path('/tmp/b61-network-tag-policy.json').read_text())
findings = boto3.client('accessanalyzer', region_name=region).validate_policy(
    policyDocument=json.dumps(policy), policyType='IDENTITY_POLICY')['findings']
print('policy-findings', json.dumps(findings))
assert not findings
iam.put_user_policy(UserName='b6-1-learner', PolicyName='B61RetagExactNetwork20261003', PolicyDocument=json.dumps(policy))
assert iam.get_user_policy(UserName='b6-1-learner', PolicyName='B61RetagExactNetwork20261003')['PolicyDocument'] == policy
print('policy-readback MATCH')
base = {'aws:RequestedRegion': region, 'aws:CalledViaFirst': 'cloudformation.amazonaws.com'}
def check(label, action, resource, values, expected='allowed'):
    result = iam.simulate_principal_policy(PolicySourceArn=f'arn:aws:iam::{account}:user/b6-1-learner', ActionNames=[action], ResourceArns=[resource], ContextEntries=[{'ContextKeyName':k, 'ContextKeyValues':[str(v)], 'ContextKeyType':'string'} for k,v in values.items()])['EvaluationResults'][0]
    print(label, result['EvalDecision'], 'missing='+str(result.get('MissingContextValues', [])))
    assert result['EvalDecision'] == expected
resources = [
    ('internet-gateway', 'igw-00647fac7637690a3', ec2.describe_internet_gateways(InternetGatewayIds=['igw-00647fac7637690a3'])['InternetGateways'][0]),
    ('route-table', 'rtb-048e2cf96a90714d5', ec2.describe_route_tables(RouteTableIds=['rtb-048e2cf96a90714d5'])['RouteTables'][0]),
    ('security-group', 'sg-07d5aa052361be676', ec2.describe_security_groups(GroupIds=['sg-07d5aa052361be676'])['SecurityGroups'][0]),
    ('subnet', 'subnet-0500b041bfa685be6', ec2.describe_subnets(SubnetIds=['subnet-0500b041bfa685be6'])['Subnets'][0]),
    ('launch-template', 'lt-03da8c5fb9551abf8', ec2.describe_launch_templates(LaunchTemplateIds=['lt-03da8c5fb9551abf8'])['LaunchTemplates'][0]),
]
for kind, rid, obj in resources:
    values = {**base, **{'aws:ResourceTag/'+t['Key']:t['Value'] for t in obj.get('Tags', [])}}
    arn = f'arn:aws:ec2:{region}:{account}:{kind}/{rid}'
    if kind in ['internet-gateway', 'route-table', 'security-group']:
        check('retag-'+kind, 'ec2:CreateTags', arn, values)
        direct = {k:v for k,v in values.items() if k != 'aws:CalledViaFirst'}
        check('direct-retag-'+kind, 'ec2:CreateTags', arn, direct, 'implicitDeny')
    if kind in ['subnet', 'security-group', 'launch-template']:
        check('launch-'+kind, 'ec2:RunInstances', arn, values)
new = {**base, 'aws:RequestTag/Project':'b6-1'}
check('launch-instance', 'ec2:RunInstances', f'arn:aws:ec2:{region}:{account}:instance/*', {**new,'ec2:InstanceType':'t3.micro','ec2:MetadataHttpTokens':'required','ec2:Tenancy':'default'})
check('launch-volume', 'ec2:RunInstances', f'arn:aws:ec2:{region}:{account}:volume/*', {**new,'ec2:VolumeType':'gp3','ec2:Encrypted':'true','ec2:VolumeSize':'8'})
check('launch-interface', 'ec2:RunInstances', f'arn:aws:ec2:{region}:{account}:network-interface/*', new)
check('launch-key', 'ec2:RunInstances', f'arn:aws:ec2:{region}:{account}:key-pair/b6-1-key', {**base,'ec2:KeyPairName':'b6-1-key'})
ami = boto3.client('ssm', region_name=region).get_parameter(Name='/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64')['Parameter']['Value']
check('launch-amazon-image', 'ec2:RunInstances', f'arn:aws:ec2:{region}::image/{ami}', {**base,'ec2:Owner':'amazon'})
for kind in ['instance', 'volume', 'network-interface']:
    check('create-tags-'+kind, 'ec2:CreateTags', f'arn:aws:ec2:{region}:{account}:{kind}/*', {**new,'ec2:CreateAction':'RunInstances'})
stack = boto3.client('cloudformation', region_name=region).describe_stacks(StackName='b6-1-learning')['Stacks'][0]
check('update-stack', 'cloudformation:UpdateStack', stack['StackId'], {'aws:RequestedRegion':region})
print('ALL CHECKS PASSED; simulation does not replace actual deployment verification')
