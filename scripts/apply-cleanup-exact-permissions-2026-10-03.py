import boto3
from pathlib import Path

POLICY_NAME = 'B61CleanupExactResources20261003'
USER_NAME = 'b6-1-learner'
ACCOUNT_ID = '171180524802'

def main():
    caller = boto3.client('sts').get_caller_identity()
    if caller['Account'] != ACCOUNT_ID:
        raise RuntimeError('Unexpected AWS account; no changes applied')
    policy_path = Path(__file__).resolve().parents[1] / 'infra' / 'iam-cleanup-exact-resources-2026-10-03.json'
    iam = boto3.client('iam')
    iam.put_user_policy(UserName=USER_NAME, PolicyName=POLICY_NAME, PolicyDocument=policy_path.read_text(encoding='utf-8'))
    result = iam.get_user_policy(UserName=USER_NAME, PolicyName=POLICY_NAME)
    print('APPLIED', result['UserName'], result['PolicyName'])
    print(result['PolicyDocument'])

if __name__ == '__main__':
    main()
