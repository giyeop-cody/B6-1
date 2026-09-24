# 배포 검증 및 리소스 정리 증거

2026-09-24 20:43–20:48 KST에 실제 AWS 화면을 캡처했다. 아래 기존 스크린샷 **17장**의 공개용 사본과 9월 25일 IAM 증거 **1장**을 보관한다. CLI 검증 화면은 AWS CloudShell에서 실행한 실제 결과다.

| 파일 | 확인 내용 |
|---|---|
| [01-stack-create-complete.jpg](01-stack-create-complete.jpg) | 삭제 전 UPDATE_COMPLETE 및 구성 리소스 |
| [02-vpc-subnet.jpg](02-vpc-subnet.jpg) | VPC 및 Public Subnet |
| [03-route-igw.jpg](03-route-igw.jpg) | 기본 경로 및 IGW 연결 |
| [04-security-group.jpg](04-security-group.jpg) | HTTP 공개 및 SSH /32 제한 |
| [05-ec2-running.jpg](05-ec2-running.jpg) | EC2 running / t3.micro / 암호화 8GiB EBS |
| [06-browser-home.jpg](06-browser-home.jpg) | 외부 브라우저 접속 정상 |
| [07-health-200.jpg](07-health-200.jpg) | 외부 /health HTTP 200, OK |
| [08-docker-healthy.jpg](08-docker-healthy.jpg) | SSH ec2-user, Docker healthy, localhost 200, 아웃바운드 200 |
| [09-stack-delete-complete.jpg](09-stack-delete-complete.jpg) | 스택 및 9개 리소스 DELETE_COMPLETE |
| [10-ec2-clean.jpg](10-ec2-clean.jpg) | EC2 terminated |
| [11-resource-clean.jpg](11-resource-clean.jpg) | 서울 EBS/EIP/Snapshot/NAT/ELB/RDS 잔여 0 |
| [11b-network-clean.jpg](11b-network-clean.jpg) | 프로젝트 VPC/Subnet/SG/IGW 잔여 0 |
| [11c-keypair-clean.jpg](11c-keypair-clean.jpg) | 키페어 삭제 / Route Table 잔여 0 / 서울 비종료 EC2 0 |
| [12-billing-check.jpg](12-billing-check.jpg) | Billing 데이터 집계 중 안내 |
| [12b-bills.jpg](12b-bills.jpg) | 2026년 9월 예상 USD 0.00, 상세 데이터 없음 |
| [12c-credits.jpg](12c-credits.jpg) | 현재 표시 크레딧 USD 100.00 |
| [13-iam-policies.jpg](13-iam-policies.jpg) | 실습 IAM 연결 정책 |

## 판정과 한계

- 배포·외부 접속·SSH·Docker·내부 localhost·아웃바운드 검증 완료 후 사용자 요청으로 스택을 삭제했다. 기존 IP는 현재 서비스 주소가 아니며 재할당될 수 있다.
- CloudFormation 삭제 완료 및 해당 프로젝트 네트워크 잔여 0, 서울 비종료 EC2/EBS/EIP/NAT/ELB/RDS/스냅샷 0을 확인했다.
- IAM 사용자 콘솔·CloudShell 접근 및 서울 EC2 조회 증거를 보관한다. [확인 범위와 공개용 화면](iam-session-2026-09-25.md)을 참고한다.
- Billing은 집계 중이다. 표시된 0달러는 최종 사용 비용 확정이 아니다. 2026-09-25 20:48 KST 이후 Bills/Credits를 재확인한다. 자동 알림은 설정하지 않았다.
- 08 화면 상단에는 터미널 입력 오류가 함께 남아 있으나 하단에 실제 SSH 세션의 Docker healthy 및 두 HTTP 200 결과가 기록돼 있다.

## 공개용 로그

- [배포 결과](aws-verification.txt)
- [이번 정리 세션 화면 텍스트](cleanup-session.txt)

## 공개 범위

원본은 로컬에 보존한다. 공개용 이미지에는 계정 메뉴, 계정 ID, SSH 소스 IP, 크레딧 ID를 검은 사각형으로 가렸다. /32 제한과 검증 결과는 유지했다. 텍스트의 계정 ID는 000000000000, 계정 이름과 SSH 소스 IP는 명시적 표식으로 치환했다. 9월 24일 Billing 금액은 당시 실습 비용 확인 기록이다. 비밀번호·개인 키는 포함하지 않았다. screenshots.sha256은 원본 해시, public-screenshots.sha256은 공개용 파일 해시다.

## IAM 접근 보완 증거 (2026-09-25)

- [15-iam-sts-ec2-public.png](15-iam-sts-ec2-public.png): IAM 사용자 ARN, 서울 리전, 비종료 EC2 0
- [iam-session-2026-09-25.md](iam-session-2026-09-25.md): 시각·명령·확인 범위

## IAM 세션 최종 재확인

[2026-09-25 최종 점검 결과](final-audit-2026-09-25.md): 스택 삭제와 잔여 리소스를 IAM 세션에서 재확인했다. 조회 거부 항목과 기존 9월 24일 기록을 구분한다.

## Billing 최종 확인

- [18-billing-final-2026-09-25.png](18-billing-final-2026-09-25.png): 2026년 9월 청구서의 CloudFormation, Data Transfer, EC2, KMS, VPC가 모두 USD 0.00으로 표시됨
- [18-billing-final-2026-09-25.txt](18-billing-final-2026-09-25.txt): 청구서 화면 텍스트 원본(계정 식별 정보 제외)
