# B6-1 트러블슈팅 기록

## 2026-10-03: IAM 사용자에게 키페어 생성 권한 없음

| 항목 | 실제 기록 |
|---|---|
| 증상 | b6-1-learner에서 EC2 CreateKeyPair dry-run이 UnauthorizedOperation 반환 |
| 원인 가설 | 기존 제한 배포 정책은 키 준비 작업을 포함하지 않음 |
| 검증 | 오류에 ec2:CreateKeyPair를 허용하는 identity-based policy가 없다고 명시됨. 관리자 세션에서 실제 연결 정책 3개를 조회 |
| 조치 | 권한을 확대하지 않고 관리자 준비 단계에서 서울 b6-1-key 생성 |
| 결과 | 16:56 KST 생성 완료 화면 및 개인 키 파일 존재 확인. IAM 세션에서 DescribeKeyPairs로 동일 키 확인 |
| 재발 방지 | IAM 전환 전에 키페어와 개인 키 보관 상태를 함께 확인. 생성 작업은 배포와 분리하고 실행 주체를 기록 |

이번 배포 성공 여부는 새 CloudFormation 상태와 실제 접속 결과로 별도 판정한다.

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

### 2026-10-03 시작 템플릿 사용 거부

- 증상: WebInstance RunInstances AccessDenied, CREATE_FAILED.
- 검증: 실제 시작 템플릿 태그에는 Project만 있고 기존 정책이 요구한 CloudFormation stack-name 태그가 없었다. 사전 시뮬레이션에 존재하지 않는 태그를 가정한 것이 오류였다.
- 조치: 정확한 이번 시작 템플릿 ARN에만 서울·CloudFormation 경유·Project 조건의 RunInstances를 허용하는 인라인 정책 적용.
- 재검증: 실제 태그로 허용 및 직접 호출/다른 템플릿 거부 확인. 이후 IAM 재배포에서 실제 EC2 생성 성공.
- 증거: 04, 05, 08, 09, 14. 재발 방지: Describe API로 확인한 태그만 권한 시뮬레이션에 사용한다.

### 2026-10-03 기존 네트워크 태그 갱신 거부

- 증상: UpdateStack 중 IGW·라우팅 테이블·보안 그룹 CreateTags 거부, UPDATE_FAILED.
- 원인: 생성 시에만 태그를 허용한 정책으로 CloudFormation 업데이트의 기존 리소스 태그 갱신을 처리하지 못했다.
- 검증: 세 리소스 실제 Project=b6-1 및 stack-name=b6-1-learning 확인.
- 조치: 정확한 세 ARN에만 서울·CloudFormation 경유·기존 소유 태그 조건으로 CreateTags 허용. 삭제나 리소스 재생성은 하지 않았다.
- 결과: IAM으로 재시도한 스택 UPDATE_COMPLETE, 외부 HTTP 200, Docker healthy 확인.
- 증거: 06~10, 12~14. 재발 방지: 생성과 기존 리소스 업데이트를 각각 검증하고 생성 전용 태그 조건을 갱신 작업에 가정하지 않는다.

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
