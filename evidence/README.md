# 실제 배포 증거 보관 규칙

현재 AWS 계정이 없으므로 실제 증거는 아직 없다. 아래 이름은 배포 후 직접 캡처할 파일의 규칙이다.

| 번호 | 파일명 | 반드시 보여야 하는 것 | 상태 |
|---:|---|---|---|
| 01 | `01-stack-create-complete.png` | 서울 리전, Stack 이름, CREATE_COMPLETE | PENDING |
| 02 | `02-vpc-subnet.png` | VPC·Public Subnet CIDR과 연결 | PENDING |
| 03 | `03-route-igw.png` | `0.0.0.0/0 → igw-*` | PENDING |
| 04 | `04-security-group.png` | HTTP 80 전체, SSH 22 개인 `/32` | PENDING |
| 05 | `05-ec2-running.png` | EC2 running, 타입, Public IP | PENDING |
| 06 | `06-browser-home.png` | 외부 네트워크에서 열린 B6-1 사이트 | PENDING |
| 07 | `07-health-200.png` | 외부 `/health` HTTP 200과 OK | PENDING |
| 08 | `08-docker-healthy.png` | `docker ps`와 healthy | PENDING |
| 09 | `09-stack-delete-complete.png` | Stack 삭제 완료 | PENDING |
| 10 | `10-ec2-clean.png` | 인스턴스 종료 또는 없음 | PENDING |
| 11 | `11-resource-clean.png` | EBS·EIP·NAT·ELB·RDS 잔여 없음 | PENDING |
| 12 | `12-billing-check.png` | Billing 확인 시각과 결과 | PENDING |

## 보안 편집 규칙

공개 저장소에 넣기 전에 다음을 가린다.

- AWS Account ID 전체
- 이메일과 사용자 실명
- 홈 공인 IP
- Key Pair private key
- 세션·Access Key·Secret Key
- 결제수단과 주소

Public IP는 과제 배포 URL로 공개할 값만 README에 기록한다. SSH 개인 IP는 이미지에서 가린다.
