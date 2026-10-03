# 삭제 권한 보정안

IAM 삭제 실행 중 시작 템플릿 삭제와 키페어 삭제 권한이 빠져 있음을 확인했다. 현재 EC2 terminated, EBS/ENI 없음, 네트워크 삭제 완료. 시작 템플릿과 키페어가 남아 있다.

infra/iam-cleanup-exact-resources-2026-10-03.json은 서울의 정확한 시작 템플릿 1개·키페어 1개 삭제 및 EIP/NAT/스냅샷/ALB/RDS 조회만 추가한다. AdministratorAccess나 IAM 변경 권한을 학습자에게 부여하지 않는다.

정책 관리 권한이 있는 세션에서 b6-1-learner에 B61CleanupExactResources20261003 인라인 정책으로 연결한다. 이후 IAM으로 스택 삭제를 재시도하고 키페어를 삭제한다. 다른 계정 자원은 삭제하지 않는다.

## 적용 완료 — 2026-10-03 19:11 KST

사용자 승인 후 루트 준비 세션에서 B61CleanupExactResources20261003 연결 완료. GetUserPolicy 원문 일치 확인. 정확한 LT/키 삭제와 서울 잔여 조회 5개 모두 allowed, 다른 키 삭제와 IAM PutUserPolicy implicitDeny 확인. 증거42 JPG/TXT. 리소스 삭제는 이 준비 세션에서 수행하지 않았다. IAM 재로그인 후 실제 삭제·잔여 조회를 이어간다.
