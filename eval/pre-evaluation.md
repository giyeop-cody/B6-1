# B6-1 사전평가

- 평가일: 2026-08-15
- 평가 성격: 저장소 정적 자체 검사
- 실제 AWS 평가: 미실시

## 판정 기준

`PASS`는 현재 환경에서 실제 확인한 것만 사용한다. 기존 AWS 계정은 사용할 수 있지만 IAM·MFA·Budget·Key Pair는 미확인이며, Docker daemon과 외부 URL이 필요한 항목은 `PENDING` 또는 `SKIP`으로 둔다.

| 평가 항목 | 상태 | 근거 |
|---|---:|---|
| 정적 웹사이트 | PASS | `site/index.html`, CSS, JS |
| Nginx `/health` 설정 | PASS | `nginx/default.conf` 정적 검사 |
| Dockerfile과 HEALTHCHECK | PASS | Dockerfile 정적 검사 |
| Docker build/run | SKIP | 현재 환경에 Docker 없음 |
| VPC·Subnet·IGW·Route 코드 | PASS | CloudFormation 리소스 9개 정적 검사 |
| HTTP 80 전체·SSH 22 개인 IP 코드 | PASS | Security Group과 공개 SSH 거부 Rule 검사 |
| EC2·EBS·IMDSv2 코드 | PASS | t3.micro, 8GiB 암호화 gp3, IMDSv2 |
| IAM 최소권한 정책 구조 | PASS | 관리자 wildcard Allow 없음, Console·SSM·CloudShell Action 제한, 서울 외 EC2 Deny |
| AWS ValidateTemplate | PENDING | IAM 사용자와 실제 정책 연결 미확인 |
| Stack CREATE_COMPLETE | PENDING | 실제 Stack 생성 전 |
| 외부 사이트와 `/health` 200 | PENDING | 실제 Stack 생성 전 |
| Docker 컨테이너 healthy | PENDING | 실제 EC2 없음 |
| 아키텍처 다이어그램 | PASS | `docs/architecture.svg` 파싱 성공 |
| 트러블슈팅 보고서 | PARTIAL | 개발환경 문제 1건, 실제 AWS 사례 필요 |
| 정리 체크리스트 | PASS | 절차 문서 존재 |
| 실제 리소스 삭제·Billing | PENDING | 실제 Stack 생성·삭제 전 |
| HTTPS 보너스 | PENDING | 도메인 없음 |
| Docker 보너스 | PARTIAL | 코드 완료, 실제 실행 증거 필요 |

## 자동 검사 결과

```text
required_files=13 PASS
cloudformation_resources=9 PASS
security_group=http80_public+ssh22_parameterized PASS
ebs=8GiB_gp3_encrypted_delete_on_termination PASS
iam=no_allow_wildcard+seoul_deny_guard PASS
B6-1 STATIC VALIDATION: ALL PASS
SHELL SYNTAX: PASS
SECRET SCAN: PASS
LOCAL DOCKER TEST: SKIP (Docker not installed)
B6-1 STATIC CHECKS: ALL PASS
```

마지막 문구는 **정적 검사 전체 PASS**라는 의미이며 Docker나 AWS 실증 PASS가 아니다.

## 현재 판정

**구현 진행 중 — 로컬 코드와 인프라 설계 완료, 실제 AWS 실증 차단 상태**

Codyssey 제출 가능 상태가 아니다. 계정 준비 후 배포·증거·삭제·외부 동료평가를 완료해야 한다.
