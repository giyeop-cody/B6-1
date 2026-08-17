# B6-1 트러블슈팅 기록

## 기록 1: 현재 개발 환경에 Docker와 AWS CLI가 없음

- 상태: 임시 조치 완료, 실제 환경 검사 대기
- 발생일: 2026-08-15
- 관련 이슈: `docs/issues/ISSUE-003-local-tools-missing.md`

| 항목 | 내용 |
|---|---|
| 증상 | `docker --version`, `aws --version`을 실행할 프로그램이 현재 검사 환경에 없음 |
| 첫 가설 | 프로젝트 파일이 잘못된 것이 아니라 실행 도구가 설치되지 않은 환경일 수 있음 |
| 검증 | `command -v docker`, `command -v aws` 결과가 비어 있고 Git·Python은 정상임을 확인 |
| 원인 | 현재 샌드박스에 Docker daemon과 AWS CLI가 제공되지 않음 |
| 조치 | 외부 도구 없이 YAML·JSON·Shell·파일 구조를 검사하는 `scripts/validate_project.py`를 먼저 만들고, 실제 Docker 검사는 Docker PC, AWS 검사는 CloudShell에서 수행하도록 분리 |
| 결과 | 정적 검사는 수행 가능해짐. Docker build와 AWS API 검증은 아직 실행하지 않았으므로 PASS로 기록하지 않음 |
| 재발 방지 | README 첫 단계에서 Docker와 AWS 계정 준비 여부를 확인하고, 도구가 없을 때 명확한 실패 메시지를 출력 |

이 기록은 개발 환경 문제다. 최종 과제 제출 전에는 실제 AWS 배포 과정에서 발생한 문제도 최소 1건 추가한다.

---

## AWS 문제 확인 순서

외부 접속이 실패하면 무작정 Security Group을 모두 열지 않고 다음 순서로 확인한다.

1. CloudFormation Events에서 실패한 Resource와 이유 확인
2. EC2가 `running`이고 상태 검사가 2/2인지 확인
3. EC2에 Public IPv4가 있는지 확인
4. Subnet Route Table에 `0.0.0.0/0 → IGW`가 있는지 확인
5. Security Group에 TCP 80이 있는지 확인
6. SSH 접속 후 `curl http://localhost/health`
7. `docker ps -a`
8. `docker logs b6-1-web`
9. `/var/log/cloud-init-output.log`

## 실제 AWS 트러블슈팅 추가 양식

> 아래 표는 실제 문제가 생긴 뒤 명령 출력과 시각을 넣는다. 미리 성공했다고 작성하지 않는다.

| 항목 | 실제 기록 |
|---|---|
| 발생 시각 | PENDING |
| 증상 | PENDING |
| 재현 명령/화면 | PENDING |
| 가설 | PENDING |
| 검증 결과 | PENDING |
| 근본 원인 | PENDING |
| 조치 | PENDING |
| 조치 후 재검증 | PENDING |
| 재발 방지 | PENDING |
