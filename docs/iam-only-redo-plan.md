# IAM으로 준비·증거 재수집 — 실행 전 기록

최신 상태: 사용자 요청으로 전환한 준비 세션에서 계정 Billing IAM 접근 설정의 비활성화를 확인하고 활성화했다. b6-1-learner에 관리형 정책 B61EvidenceAndKeyPreparation20261003을 추가했다. 정책은 AWSBillingReadOnlyAccess v28에서 Billing/FreeTier/Budget/CostExplorer의 조회 동작만 추려내고, 서울의 b6-1-key 생성 및 본인 IAM 설정 조회를 허용한다. IAM 쓰기/결제 변경/다른 키 생성은 부여하지 않았다. Access Analyzer findings [], 저장 정책 readback 일치 및 허용/거부 시뮬레이션 통과. 19, 20 증거 보관.

준비 세션 STS는 root였으며, 이를 IAM 실행으로 기록하지 않는다. 이 세션에서 스택/EC2/키페어 생성 또는 삭제는 하지 않았다. 기존 키페어를 삭제·재생성하는 것은 삭제 보류 지시와 충돌하므로 수행하지 않았다. 실제 IAM Billing 조회 및 증거 재수집은 사용자 IAM 재로그인 대기 중이다.

사용자 요청: 키페어·권한 준비도 IAM으로 다시 수행하고 Billing을 IAM으로 확인한다. 증거를 다시 수집하되 삭제·해제는 보류한다.

현재 실행 가능한 권한: b6-1-learner로 실제 스택 배포와 조회 가능. 직접 CreateKeyPair dry-run 및 iam:ListUsers는 거부됨. 사용자에게 기존 관리자 IAM 사용자/Role 유무 확인 중이다. 루트 로그인이나 권한 확대를 임의로 요청/실행하지 않는다.

Billing은 IAM 조회가 가능하다. 공식 문서에 따라 계정의 Activate IAM Access 설정과 사용자/Role의 Billing 조회 정책이 함께 필요하다. 현재 AccessDenied만으로 둘 중 어느 설정이 빠졌는지 확정하지 않는다. 관리자 IAM에서 조회 정책을 부여하고 IAM으로 재검증한다. 계정 접근 설정이 꺼져 있으면 AWS 문서에서 루트 계정의 활성화 단계가 명시되어 있으므로, IAM만으로 활성화할 수 있다고 약속하지 않는다.

출처:
- https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/control-access-billing.html
- https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/managed-policies.html

삭제·해제 보류 조건:
- 기존 키페어·스택·EC2를 삭제하거나 교체해 기존 리소스를 제거하지 않는다.
- 기존 리소스 개수 규정과 보존 지시를 함께 확인하기 전 새 키페어/EC2를 중복 생성하지 않는다.
- 기존 루트 준비 이력은 삭제하거나 IAM 이력으로 고쳐 쓰지 않는다. 새 실행은 별도 날짜/시각과 실제 수행자 ARN으로 구분한다.
- 관리자 IAM 세션에서 필요한 권한과 기존 자원을 한 번에 확인한 후 준비한다. 준비가 끝나기 전에 IAM 계정 전환을 요구하지 않는다.

이번 문서는 실행 계획이며 IAM 재준비·Billing 조회 성공·새 배포 완료 증거가 아니다.
