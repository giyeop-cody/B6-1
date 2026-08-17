#!/usr/bin/env bash
set -euo pipefail

STACK_NAME="${B6_STACK_NAME:-b6-1-learning}"
REGION="ap-northeast-2"

if ! command -v aws >/dev/null 2>&1; then
  echo "FAIL: AWS CLI가 필요합니다." >&2
  exit 2
fi

ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
echo "AWS account: ${ACCOUNT_ID}"
echo "삭제할 Stack: ${STACK_NAME} (${REGION})"
read -r -p "EC2, VPC, Subnet, Route Table, IGW, Security Group이 삭제됩니다. DELETE를 입력하세요: " answer
[[ "$answer" == "DELETE" ]] || { echo "취소했습니다."; exit 1; }

aws cloudformation delete-stack --region "$REGION" --stack-name "$STACK_NAME"
echo "삭제 완료를 기다립니다."
aws cloudformation wait stack-delete-complete --region "$REGION" --stack-name "$STACK_NAME"
echo "STACK DELETE: COMPLETE"
echo "다음은 Stack 밖에서 만든 Key Pair와 Billing 화면을 별도로 확인하세요."
