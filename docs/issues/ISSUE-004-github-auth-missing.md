# ISSUE-004: GitHub 인증이 없어 원격 Issue·Branch·PR을 만들 수 없다

- 상태: 인증 차단 해소, 원격 PR 진행 중
- 발견일: 2026-08-15
- 해결일: 2026-08-17
- 우선순위: 높음

## 현상

현재 환경에는 GitHub CLI가 설치되어 있지 않고 HTTPS Git 인증 정보도 없다.

```text
gh=NOT_INSTALLED
fatal: could not read Username for 'https://github.com'
```

## 영향

로컬에서는 기능별 branch와 commit을 만들었지만 다음 외부 작업을 아직 할 수 없다.

- GitHub Issue 생성
- 원격 branch push
- Pull Request 생성
- PR 검토 후 main 병합
- 원격 `learning`, `eval` branch 생성

## 현재 보존된 로컬 기록

- `learning`
- `feature/docker-nginx-site`
- `feature/cloudformation-infra`
- `security/credential-protection`
- `docs/deployment-runbook`
- `test/project-validation`
- `eval`
- `feature/b6-1-aws-foundation`

## 안전한 해결

GitHub 비밀번호나 토큰을 채팅·문서에 적지 않는다. 저장소 소유자가 자신의 환경에서 GitHub CLI 또는 안전한 Credential Manager로 로그인한 뒤 branch를 push하고 Issue·PR을 만든다.

## 완료 조건

- [ ] 구현 이슈가 GitHub에 생성됨
- [ ] `learning`, `eval`, 기능 branch가 원격에 존재함
- [ ] `feature/b6-1-aws-foundation` → `main` PR 생성
- [ ] 자동 검사 결과가 PR에 기록됨
- [ ] 검토 후 main 병합
