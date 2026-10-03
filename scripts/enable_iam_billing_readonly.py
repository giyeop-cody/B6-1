"""Run only from an already authorized administrator IAM session, never root.

Attaches AWS's read-only Billing policy to the named learner. Does not enable
the account-level IAM Billing access switch or create/delete any resources.
"""
import boto3

sts = boto3.client('sts')
identity = sts.get_caller_identity()
assert identity['Account'] == '171180524802', 'Wrong account'
assert not identity['Arn'].endswith(':root'), 'Administrator IAM user/Role required'
iam = boto3.client('iam')
policy_arn = 'arn:aws:iam::aws:policy/AWSBillingReadOnlyAccess'
iam.get_policy(PolicyArn=policy_arn)
iam.attach_user_policy(UserName='b6-1-learner', PolicyArn=policy_arn)
attached = []
for page in iam.get_paginator('list_attached_user_policies').paginate(UserName='b6-1-learner'):
    attached.extend(page['AttachedPolicies'])
assert any(policy['PolicyArn'] == policy_arn for policy in attached)
print('Administrator principal:', identity['Arn'])
print('b6-1-learner AWSBillingReadOnlyAccess attached and verified')
print('Account IAM Billing access switch and learner console access still need verification')
