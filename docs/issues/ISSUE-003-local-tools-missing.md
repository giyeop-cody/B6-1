# ISSUE-003: 현재 검사 환경에 Docker와 AWS CLI가 없다

- 상태: 열림
- 발견일: 2026-08-15
- 우선순위: 중간

## 재현

```bash
docker --version
aws --version
```

현재 작업 환경에서는 두 명령을 찾을 수 없다.

## 영향

- Docker 이미지를 실제로 build/run하는 검사는 아직 할 수 없다.
- `aws cloudformation validate-template`과 실제 Stack 배포를 아직 할 수 없다.

## 임시 검증

외부 도구 없이 가능한 다음 검사부터 수행한다.

- HTML·Nginx·Dockerfile 파일 존재 및 핵심 설정 확인
- Python으로 CloudFormation YAML 문법과 필수 리소스 검사
- Shell 스크립트 `bash -n` 검사

## 현재 결과

- `scripts/check_all.sh`: 정적 검사 전체 PASS
- `cfn-lint infra/cloudformation.yml`: PASS
- Docker build/run: 현재 환경에 Docker가 없어 대기
- AWS API 검사: 계정이 없어 대기

## 최종 해결

- Docker가 있는 로컬 PC에서 `scripts/test-local.sh` 실행
- AWS CloudShell에서 AWS 검증 스크립트 실행

## 완료 조건

실제 Docker 빌드·헬스체크와 AWS Stack 검증 결과가 증거로 저장되어야 한다.
