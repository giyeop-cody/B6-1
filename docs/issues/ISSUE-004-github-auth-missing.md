# ISSUE-004: GitHub 인증이 없어 원격 Issue·Branch·PR을 만들 수 없다

- 상태: 인증 차단 해소, PR [#2](https://github.com/giyeop-cody/B6-1/pull/2) 검토·병합 대기
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
- 원격 `learning` branch 생성

## 현재 보존된 로컬 기록

- `learning`
- `feature/docker-nginx-site`
- `feature/cloudformation-infra`
- `security/credential-protection`
- `docs/deployment-runbook`
- `test/project-validation`
- `feature/b6-1-aws-foundation`

## 해결

GitHub 비밀번호나 토큰을 코드·문서에 저장하지 않고 GitHub CLI Device Login으로 저장소 소유자 계정을 인증했다. 작업 완료 뒤 `gh auth logout`으로 환경의 인증을 제거한다.

## 완료 조건

- [x] 구현 이슈 #1이 GitHub에 생성됨
- [x] `learning`과 기능 branch가 원격에 존재함
- [x] `feature/b6-1-aws-foundation` → `main` PR #2 생성
- [x] 자동 검사 결과가 PR에 기록됨
- [ ] 검토 후 main 병합
