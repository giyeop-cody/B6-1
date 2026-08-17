# AWS 리소스 정리 체크리스트

> 이 문서는 실제 삭제 후 날짜·결과를 기록한다. 기존 AWS 계정 사용은 확인했지만 아직 Stack을 만들지 않아 모든 삭제 항목은 미확인 상태다.

## 실습 정보

| 항목 | 실제 값 |
|---|---|
| AWS Account 마지막 4자리 | PENDING |
| 리전 | `ap-northeast-2` |
| Stack | `b6-1-learning` |
| 시작 시각 | PENDING |
| 삭제 시각 | PENDING |
| 확인자 | PENDING |

## 1. Stack 삭제

```bash
scripts/delete-stack.sh
```

- [ ] CloudFormation Stack이 `DELETE_COMPLETE` 후 목록에서 제거됨
- [ ] Stack 삭제 실패 이벤트가 없음

## 2. Stack에 포함된 리소스

- [ ] EC2 인스턴스가 `terminated`
- [ ] EC2에 연결됐던 8GiB EBS가 삭제됨
- [ ] Security Group이 삭제됨
- [ ] Public Subnet이 삭제됨
- [ ] Route Table이 삭제됨
- [ ] Internet Gateway가 분리·삭제됨
- [ ] VPC가 삭제됨

## 3. Stack 밖에서 별도로 만든 항목

- [ ] `b6-1-key` Key Pair가 더 필요하지 않으면 콘솔에서 삭제됨
- [ ] 로컬 `.pem`도 더 필요하지 않으면 안전하게 삭제됨
- [ ] Elastic IP가 생성되지 않았음을 확인함
- [ ] NAT Gateway가 생성되지 않았음을 확인함
- [ ] Load Balancer가 생성되지 않았음을 확인함
- [ ] RDS가 생성되지 않았음을 확인함
- [ ] 사용하지 않는 EBS Volume과 Snapshot이 없음을 확인함

## 4. 비용 확인

- [ ] Billing Dashboard에서 현재 비용 확인
- [ ] Credits 잔액 확인
- [ ] Cost Explorer 또는 Bills에서 EC2·EBS·Public IPv4 관련 항목 확인
- [ ] 24시간 뒤 청구 반영을 다시 확인할 일정 기록

다음 확인 날짜:

```text
PENDING
```

## 5. 삭제 증거

| 증거 | 파일 |
|---|---|
| Stack 삭제 완료 | `evidence/09-stack-delete-complete.png` |
| EC2 없음 또는 terminated | `evidence/10-ec2-clean.png` |
| EBS/EIP 등 잔여 자원 없음 | `evidence/11-resource-clean.png` |
| Billing 확인 | `evidence/12-billing-check.png` |

## 최종 선언

```text
[ ] 생성한 과금 가능 리소스를 모두 확인했고 불필요한 리소스를 삭제했다.
확인 시각: PENDING
```
