#!/usr/bin/env bash
set -euo pipefail

STACK_NAME="${B6_STACK_NAME:-b6-1-learning}"
REGION="ap-northeast-2"
KEY_NAME="${1:-}"
SSH_CIDR="${2:-}"

if ! command -v aws >/dev/null 2>&1; then
  echo "FAIL: AWS CLI가 필요합니다. AWS CloudShell에서 실행할 수 있습니다." >&2
  exit 2
fi
if [[ -z "$KEY_NAME" || -z "$SSH_CIDR" ]]; then
  echo "사용: $0 <서울 리전 Key Pair 이름> <내 공인IP/32>" >&2
  echo "예: $0 b6-1-key 203.0.113.10/32" >&2
  exit 2
fi
if [[ "$SSH_CIDR" == "0.0.0.0/0" ]]; then
  echo "FAIL: SSH를 전체 인터넷에 공개할 수 없습니다." >&2
  exit 2
fi
if [[ ! "$SSH_CIDR" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}/32$ ]]; then
  echo "FAIL: SSH CIDR은 개인 IPv4 한 개를 뜻하는 /32 형식이어야 합니다." >&2
  exit 2
fi

CALLER_ARN="$(aws sts get-caller-identity --query Arn --output text)"
if [[ "$CALLER_ARN" == *:root ]]; then
  echo "FAIL: 과제는 루트 배포를 금지합니다. 실습 IAM 사용자/Role로 로그인하세요." >&2
  exit 2
fi
ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
echo "AWS account: ${ACCOUNT_ID}"
echo "Region: ${REGION}"
echo "Stack: ${STACK_NAME}"
echo "SSH source: ${SSH_CIDR}"
read -r -p "위 계정에 리소스를 생성합니다. DEPLOY를 입력하세요: " answer
[[ "$answer" == "DEPLOY" ]] || { echo "취소했습니다."; exit 1; }

[[ "$STACK_NAME" == "b6-1-learning" ]] || { echo "FAIL: permitted stack is b6-1-learning" >&2; exit 2; }
[[ "$KEY_NAME" == "b6-1-key" ]] || { echo "FAIL: permitted key is b6-1-key" >&2; exit 2; }

STACK_PARAMS=(
  "ParameterKey=ProjectName,ParameterValue=b6-1"
  "ParameterKey=KeyName,ParameterValue=${KEY_NAME}"
  "ParameterKey=AllowedSshCidr,ParameterValue=${SSH_CIDR}"
  "ParameterKey=InstanceType,ParameterValue=t3.micro"
)

# Create on the first run and update the same named stack on later runs.
# No change sets, S3 upload, or execution role are used.
if aws cloudformation describe-stacks --region "$REGION" --stack-name "$STACK_NAME" >/dev/null 2>&1; then
  echo "Existing stack found; updating the reviewed template."
  set +e
  UPDATE_OUTPUT="$(aws cloudformation update-stack \
    --region "$REGION" \
    --stack-name "$STACK_NAME" \
    --template-body file://infra/cloudformation.yml \
    --parameters "${STACK_PARAMS[@]}" 2>&1)"
  UPDATE_STATUS=$?
  set -e
  if [[ "$UPDATE_STATUS" -ne 0 && "$UPDATE_OUTPUT" != *"No updates are to be performed"* ]]; then
    echo "$UPDATE_OUTPUT" >&2
    exit "$UPDATE_STATUS"
  fi
  if [[ "$UPDATE_STATUS" -eq 0 ]]; then
    aws cloudformation wait stack-update-complete --region "$REGION" --stack-name "$STACK_NAME"
  else
    echo "No updates are to be performed."
  fi
else
  aws cloudformation create-stack \
    --region "$REGION" \
    --stack-name "$STACK_NAME" \
    --template-body file://infra/cloudformation.yml \
    --parameters "${STACK_PARAMS[@]}"
  aws cloudformation wait stack-create-complete --region "$REGION" --stack-name "$STACK_NAME"
fi

aws cloudformation describe-stacks \
  --region "$REGION" \
  --stack-name "$STACK_NAME" \
  --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
  --output table
