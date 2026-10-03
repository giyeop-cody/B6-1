# 세부 청구서 조회 수정안

적용 결과: 사용자 재로그인 후 준비 세션에서 AWSBillingReadOnlyAccess 연결 완료 및 실제 연결 목록 readback 확인. account/GetBillingData/GetBillingDetails/GetCredits, invoicing ListInvoiceSummaries/GetInvoicePDF, payments GetPaymentStatus, consolidatedbilling GetAccountBillingRole 시뮬레이션 모두 allowed. iam AttachUserPolicy, payments MakePayment, billing UpdateBillingPreferences는 implicitDeny. 증거 31 JPG/TXT 저장. 실제 IAM 재로그인 후 18:42 KST에 청구서·청구 문서 화면 조회 성공(32·33). 10월 예상 USD 0.00/상세 데이터 없음, 발행 문서 0건. 실제 PDF는 발행되지 않아 다운로드하지 않았다. 삭제·해제 미수행.

이전 제한 정책을 만들 때 AWSBillingReadOnlyAccess v28에서 account:GetAccountInformation, invoicing 및 일부 연결 조회 동작을 제외했다. Billing 홈/크레딧은 조회되지만 청구서 페이지는 거부된다. 해당 제외가 어느 API의 거부를 일으켰는지는 아직 개별 확정하지 않았다.

공식 문서가 청구서 조회용으로 명시하는 AWSBillingReadOnlyAccess를 b6-1-learner에 연결하여 필요한 조회 의존성을 함께 제공한다. AdministratorAccess, IAM 쓰기 또는 결제 변경 권한은 이 정책에 없다. 읽기 범위는 기존 맞춤 정책보다 넓다.

관리 권한이 있는 준비 세션에서 실행할 정확한 명령:

```bash
aws iam attach-user-policy --user-name b6-1-learner --policy-arn arn:aws:iam::aws:policy/AWSBillingReadOnlyAccess
aws iam list-attached-user-policies --user-name b6-1-learner --query 'AttachedPolicies[].PolicyName' --output text
```

출처: https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSBillingReadOnlyAccess.html

계정 IAM Billing 접근 활성화는 앞선 준비에서 완료했다. 키 생성 권한은 이미 정확한 서울 b6-1-key에 대해 IAM dry-run 허용으로 확인됐다. 이 수정과 관련하여 기존 리소스 삭제/해제/중복 생성은 하지 않는다.

연결 성공은 실제 IAM 청구서 조회 성공을 대신하지 않는다. 적용 후 IAM 세션의 청구서 페이지와 월/상태/금액을 확인하여 JPG/TXT 증거를 수집한다. root 화면을 IAM 증거로 사용하지 않는다.
