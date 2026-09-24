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

기록 2에 실제 AWS 배포 준비 과정의 정책 오류와 해결을 추가했다.

---

## 기록 2: IAM 정책 교체의 레거시 파서 오류

- 상태: 해결 및 재검증 완료
- 발생일: 2026-09-24
- 영향: 제한 정책 교체 전까지 사용자를 통한 배포 전환을 진행할 수 없었음

| 단계 | 실제 기록 |
|---|---|
| 증상 | IAM 콘솔에서 기존 `B61DeployerPolicy` 정책 버전을 제한 JSON으로 교체하려 할 때 `The policy failed legacy parsing` 오류가 표시됨 |
| 가설 | 콘솔의 기존 정책 버전 편집 경로가 새 조건·리소스 제한 문장을 처리하지 못하는지 확인해야 함 |
| 검증 | 같은 JSON을 CloudShell의 IAM Access Analyzer로 검증한 결과 두 정책 모두 findings `[]`; 콘솔 편집 경로에서만 저장 실패 |
| 조치 | `B61DeployerPolicyRestricted`와 `B61Ec2DeploymentPolicy`를 CloudShell에서 새 고객 관리형 정책으로 생성하고 `b6-1-learner`에 연결한 뒤 기존 광범위 `B61DeployerPolicy`를 분리 |
| 결과 | 연결 정책은 제한 정책 2개와 `IAMUserChangePassword`만 남음. 서울 리전 조건 시뮬레이션에서 CloudFormation 생성·EC2 조회는 허용되고 S3 전체 조회·IAM Access Key 생성은 거부됨 |
| 재발 방지 | 기존 버전 편집에 의존하지 않고 새 정책 생성 → Access Analyzer 검증 → 사용자 연결 → 기존 정책 분리 순서로 적용 |

최초 CloudFormation Stack 생성은 정책 교체 전에 루트 Console의 CloudShell에서 수행했고, 이 기록은 그 뒤 최소권한 사용자 전환 과정의 문제 해결을 설명한다.

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

## 기록 3: SSH 증거 수집 실패 후 EC2 Instance Connect 재검증

- 증상: 기존 b6-1-key.pem을 로컬에서 찾지 못했고 이전 Instance Connect 접속 시도에서도 인증이 실패해 서버 내부 증거를 수집하지 못했다.
- 가설: 접속 소스가 보안 그룹 /32에 포함되지 않거나 일회성 키·OS 사용자·키 선택이 실제 접속과 일치하지 않았을 수 있다. 이전 인증 실패의 단일 원인은 확정하지 않았다.
- 검증: 배포 인스턴스의 AZ ap-northeast-2a, 사용자 ec2-user, 현재 CloudShell 소스를 확인했다.
- 조치: 임시 RSA 키를 생성해 Instance Connect로 공개 키를 주입하고 CloudShell IP /32만 일시 허용했다. SSH에서 IdentitiesOnly=yes와 해당 개인 키를 명시했다. 종료 trap으로 임시 규칙을 회수했다.
- 결과: 2026-09-24 20:45 KST 접속 성공. docker ps에서 b6-1-web:latest healthy, localhost HTTP 200, example.com outbound HTTP 200 확인. [실제 화면](../evidence/08-docker-healthy.jpg). 임시 규칙 제거 후 원래 SSH /32만 남은 것을 확인했다.
- 재발 방지: 사용자가 직접 키를 보관하고 최초 배포 직후 SSH를 검증한다. IAM 전용 세션과 필요한 최소 권한을 미리 확인한다. 키 주입 성공만으로 SSH 접속 성공을 판단하지 않는다.

이후 사용자 요청으로 스택을 삭제했으며 재접속할 대상은 남아 있지 않다.
