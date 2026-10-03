"""One-time authorized account setup; never creates/deletes workload resources."""
import copy
import json
from pathlib import Path
import boto3

iam = boto3.client('iam')
account = boto3.client('sts').get_caller_identity()['Account']
assert account == '171180524802'
user = 'b6-1-learner'
managed = 'arn:aws:iam::aws:policy/AWSBillingReadOnlyAccess'
version = iam.get_policy(PolicyArn=managed)['Policy']['DefaultVersionId']
source = iam.get_policy_version(PolicyArn=managed, VersionId=version)['PolicyVersion']['Document']
statements = []
for statement in source['Statement']:
    actions = statement.get('Action', [])
    if isinstance(actions, str):
        actions = [actions]
    selected = [action for action in actions if action.startswith(('billing:Get', 'billing:List', 'freetier:Get', 'freetier:List', 'budgets:Describe', 'budgets:View', 'ce:Get', 'ce:List')) or action in ['aws-portal:ViewBilling', 'aws-portal:ViewUsage']]
    if selected and statement['Effect'] == 'Allow':
        restricted = copy.deepcopy(statement)
        restricted['Action'] = selected
        statements.append(restricted)
assert statements
policy = {'Version':'2012-10-17', 'Statement':statements + [
    {'Sid':'CreateOnlyLearningKeyInSeoul','Effect':'Allow','Action':['ec2:CreateKeyPair'], 'Resource':f'arn:aws:ec2:ap-northeast-2:{account}:key-pair/b6-1-key','Condition':{'StringEquals':{'aws:RequestedRegion':'ap-northeast-2'}}},
    {'Sid':'TagLearningKeyOnlyAtCreation','Effect':'Allow','Action':'ec2:CreateTags','Resource':f'arn:aws:ec2:ap-northeast-2:{account}:key-pair/b6-1-key','Condition':{'StringEquals':{'aws:RequestedRegion':'ap-northeast-2','ec2:CreateAction':'CreateKeyPair'}}},
    {'Sid':'ReadOwnIAMConfiguration','Effect':'Allow','Action':['iam:GetUser','iam:ListAttachedUserPolicies','iam:ListUserPolicies','iam:GetUserPolicy'], 'Resource':f'arn:aws:iam::{account}:user/{user}'},
    {'Sid':'ReadAttachedDeploymentPolicyDefinitions','Effect':'Allow','Action':['iam:GetPolicy','iam:GetPolicyVersion'], 'Resource':[f'arn:aws:iam::{account}:policy/B61DeployerPolicyRestricted',f'arn:aws:iam::{account}:policy/B61Ec2DeploymentPolicy','arn:aws:iam::aws:policy/IAMUserChangePassword']},
]}
findings = boto3.client('accessanalyzer', region_name='ap-northeast-2').validate_policy(policyDocument=json.dumps(policy), policyType='IDENTITY_POLICY')['findings']
print('Access Analyzer:', json.dumps(findings))
assert not any(f['findingType'] in ['ERROR','SECURITY_WARNING'] for f in findings)
policy_name = 'B61EvidenceAndKeyPreparation20261003'
policy_arn = f'arn:aws:iam::{account}:policy/{policy_name}'
try:
    iam.create_policy(PolicyName=policy_name, PolicyDocument=json.dumps(policy), Description='Read-only billing evidence and exact Seoul learning key preparation')
except iam.exceptions.EntityAlreadyExistsException:
    current_version = iam.get_policy(PolicyArn=policy_arn)['Policy']['DefaultVersionId']
    assert iam.get_policy_version(PolicyArn=policy_arn, VersionId=current_version)['PolicyVersion']['Document'] == policy
iam.attach_user_policy(UserName=user, PolicyArn=policy_arn)
stored_version = iam.get_policy(PolicyArn=policy_arn)['Policy']['DefaultVersionId']
assert iam.get_policy_version(PolicyArn=policy_arn, VersionId=stored_version)['PolicyVersion']['Document'] == policy
Path('/tmp/b61-evidence-policy.json').write_text(json.dumps(policy, indent=2))
print('Policy stored and readback MATCH; based on AWS read-only version', version)
for label, action, resource, context, expected in [
    ('own-key','ec2:CreateKeyPair',f'arn:aws:ec2:ap-northeast-2:{account}:key-pair/b6-1-key', {'aws:RequestedRegion':'ap-northeast-2'},'allowed'),
    ('other-key','ec2:CreateKeyPair',f'arn:aws:ec2:ap-northeast-2:{account}:key-pair/other-key', {'aws:RequestedRegion':'ap-northeast-2'},'implicitDeny'),
    ('iam-write','iam:PutUserPolicy',f'arn:aws:iam::{account}:user/{user}', {},'implicitDeny'),
    ('billing-write','billing:UpdateIAMAccessPreference','*',{},'implicitDeny'),
    ('billing-read','billing:GetBillingData','*',{},'allowed'),
]:
    result = iam.simulate_principal_policy(PolicySourceArn=f'arn:aws:iam::{account}:user/{user}', ActionNames=[action], ResourceArns=[resource], ContextEntries=[{'ContextKeyName':k,'ContextKeyValues':[v],'ContextKeyType':'string'} for k,v in context.items()])['EvaluationResults'][0]
    print(label, result['EvalDecision'])
    assert result['EvalDecision'] == expected
print('No AdministratorAccess, IAM write, payment changes, key deletion, or workload changes granted/performed')
