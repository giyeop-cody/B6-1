# ISSUE-005: Console 배포와 public AMI 조회에 필요한 IAM 권한이 빠져 있다

- 상태: 코드 수정·자동 검사 완료, PR 대기
- 발견일: 2026-08-17
- 우선순위: 높음
- 원격 GitHub Issue: [#5](https://github.com/giyeop-cody/B6-1/issues/5)

## 현상

실제 AWS 배포 직전에 `infra/deployer-policy.json`을 Console 실행 순서와 다시 대조했다. 기존 정책에는 다음 Action이 없었다.

- CloudFormation Stack 목록·템플릿 요약·resource 상세 읽기
- 동적 참조가 사용하는 Amazon Linux 2023 public SSM parameter 읽기
- Access Key 없이 검증하기 위한 CloudShell 세션 Action

이 상태로 Console 배포를 시작하면 `AccessDenied`가 발생할 수 있다.

## 먼저 만든 실패 검사

`scripts/validate_project.py`에 필요한 Action과 SSM resource 범위 검사를 먼저 추가했다. 정책 수정 전에는 누락 목록과 함께 의도대로 실패했다.

## 해결

- 필요한 CloudFormation 읽기 Action 추가
- SSM 읽기를 AL2023 public AMI parameter 하나로 제한
- CloudShell 세션 생성·시작·자격 증명 전달 Action 추가
- CloudShell 파일 upload/download Action은 제외
- 기존 서울 리전 조건과 EC2 외부 리전 Deny 유지

## 완료 조건

- [x] 정책 수정 전 자동 검사가 누락을 탐지
- [x] 정책 수정 후 정적 검사 PASS
- [x] AdministratorAccess와 전체 `Action: "*"` 없음
- [x] 선택지와 트레이드오프 기록
- [ ] GitHub PR 검토·main 병합
- [ ] 실제 IAM Policy 생성 화면 확인
- [ ] 실제 Stack 생성에서 AccessDenied가 없는지 확인
