# AWS 리소스 정리 체크리스트

> **최신 상태 (2026-09-25):** IAM 사용자 콘솔·CloudShell 사용 및 스택 삭제/리소스 정리 재확인을 완료했다. 아래 9월 24일 내용은 당시 기록이며, 현재 판정은 [최종 점검 결과](../evidence/final-audit-2026-09-25.md)를 기준으로 확인한다.

2026-09-24 사용자 요청으로 증거 수집 후 **정리 완료**했다. 대상은 서울 리전의 b6-1-learning 실습 스택과 b6-1-key 키페어다.

| 항목 | 결과 |
|---|---|
| 계정 마지막 4자리 | 4802 |
| 리전 | ap-northeast-2 |
| 삭제 요청 시각 | 2026-09-24 20:46:09 KST |
| 스택 완료 확인 | 2026-09-24 20:46:59 KST |
| 최종 잔여 확인 | 2026-09-24 20:48:03 KST |
| 실행 주체 | b6-1-learner IAM 사용자 |

## 스택과 과금 리소스

- [x] b6-1-learning: DELETE_COMPLETE, 구성 리소스 9개 모두 DELETE_COMPLETE
- [x] EC2 i-093226b9e4314ad26: terminated; 서울 비종료 인스턴스 0
- [x] EBS vol-087794825c782c6e5 삭제; 서울 EBS 0
- [x] 프로젝트 Security Group·Public Subnet·Route Table 잔여 0
- [x] 프로젝트 Internet Gateway·VPC 잔여 0
- [x] 서울 Elastic IP 0 (추가 해제 대상 없음)
- [x] 서울 비삭제 NAT Gateway 0
- [x] 서울 ALB/NLB 및 Classic ELB 0
- [x] 서울 RDS 인스턴스 및 DB Cluster 0
- [x] 서울 소유 EBS Snapshot 0
- [x] 사용 중인 인스턴스가 없음을 확인한 뒤 b6-1-key 삭제, 잔여 0
- [x] 이번 CloudShell 임시 SSH 키 및 이전 /tmp/b6eic 키 삭제
- [ ] 개인 PC의 기존 b6-1-key.pem: 이전 다운로드를 찾지 못해 존재·삭제 확인 불가

루트 MFA와 IAM 사용자·정책은 계정 설정으로 유지했다. 다른 리전 및 다른 프로젝트 전체의 무과금 여부를 보증하는 점검은 아니다.

## Billing

- [x] Billing Dashboard: 사용량 데이터 준비 중, 최대 24시간 안내 확인
- [x] 2026년 9월 Bills: 예상 USD 0.00 표시, 세부 사용량 데이터 없음
- [x] Credits: 잔여 USD 100.00 / 사용 USD 0.00 표시
- [x] 2026-09-25 16:48 KST EC2·EBS·Public IPv4 사용량과 크레딧 반영 재확인. [상세 증거](../evidence/billing-review-2026-09-25.md)

재확인 완료: **2026-09-25 16:48 KST**, 상세 사용량과 Free Tier 크레딧 반영을 확인했다. EC2 USD 0.02 + Public IPv4 USD 0.01, 상계 후 예상 USD 0.00이다. 월말 확정 청구액으로 표현하지 않는다.

## 증거

[증거 목록](../evidence/README.md)의 09–12c 스크린샷과 cleanup-session.txt에 결과를 보관했다. 웹사이트는 삭제 전 검증된 기록이며 삭제 후 기존 IP로 접속하지 않는다.
