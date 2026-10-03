# 2026-10-03 IAM 실행 기록

실제 CloudFormation CreateStack 및 UpdateStack 실행은 서울 리전의 `b6-1-learner` IAM 사용자 CloudShell에서 수행했다. STS ARN의 사용자 부분과 실제 EC2/보안 그룹 출력은 `evidence/2026-10-03/09-iam-ec2-security-group.jpg`, `.txt`에 보관했다.

관리자 준비 단계에서는 루트 세션을 사용하여 키페어 준비와 제한 IAM 정책 보정을 수행했다. 과제의 루트 계정 사용 금지 문구와 이 준비 단계의 차이는 숨기지 않는다. 실제 스택 배포를 루트가 수행한 것으로 기록하거나 관리자 준비 화면을 IAM 사용 증거로 제출하지 않는다.

배포 계정의 기본 정책은 `B61DeployerPolicyRestricted`, `B61Ec2DeploymentPolicy`, `IAMUserChangePassword`이다. 이번 배포에서 추가한 인라인 정책은 다음 두 가지다.

- `B61UseExactLaunchTemplate20261003`: 이번 시작 템플릿 ARN 하나에 대해 서울 리전, CloudFormation 경유, Project=b6-1 조건으로 RunInstances 허용.
- `B61RetagExactNetwork20261003`: 이번 IGW·라우팅 테이블·보안 그룹 ARN 세 개에 대해 서울 리전, CloudFormation 경유 및 기존 Project/stack-name 태그 조건으로 CreateTags 허용.

정책 원문은 `infra/launch-template-use-policy.json`, `infra/owned-network-tag-update-policy.json`에 있다. 계정 ID가 포함되어 있으므로 공개 제출 전 가림 처리가 필요하다. 정책 검증 결과는 05 및 08 증거에 있다. 시뮬레이션 허용은 실제 배포 성공을 대신하지 않는다.

개인 키는 저장소 밖에 보관하며, 비밀번호·액세스 키·세션 자격 증명은 증거에 기록하지 않는다. MFA 및 Budget 설정 완료는 이번 실행에서 확인하지 않았으므로 완료로 표시하지 않는다.


## 최종 정리 실행

2026-10-03 19:11 KST 루트 준비 세션에서 B61CleanupExactResources20261003 연결·검증(42). 19:17 KST IAM b6-1-learner로 스택 삭제 재시도·키페어 삭제 성공(43), DELETE_COMPLETE 및 잔여 조회(44), 최종 Billing(46·47). 초기 키페어 루트 생성 이력은 보존한다.
