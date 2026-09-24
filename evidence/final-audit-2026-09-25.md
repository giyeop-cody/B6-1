# 최종 AWS 확인 결과 — 2026-09-25

확인 시각: 07:11 KST (CloudShell UTC 2026-09-24T22:11:12.901905+00:00).
실행 환경: IAM 사용자 `b6-1-learner`, 서울 `ap-northeast-2`.

| 확인 항목 | 결과 | 증거 |
|---|---|---|
| IAM 콘솔·CloudShell 사용 | 사용자 ARN 확인 | 15-iam-sts-ec2-public.png |
| 배포 성공 | 과거 UPDATE_COMPLETE, 홈페이지 정상, HTTP 200 | 01, 06, 07 캡처 |
| Docker·SSH | healthy, localhost 200, outbound 200 | 08 캡처 |
| 프로젝트 스택 | DELETE_COMPLETE 재확인 | 17-final-audit-dom.txt |
| 서울 비종료 EC2 / EBS | 각각 0 | 17-final-audit-dom.txt |
| 프로젝트 VPC / Subnet / SG / Route Table / IGW | 각각 0 | 17-final-audit-dom.txt |
| 프로젝트 키페어 | 0 (07:08 KST 조회) | 16-cleanup-recheck-2026-09-25.txt |
| EIP / Snapshot / NAT / ALB·NLB / Classic ELB / RDS 인스턴스·클러스터 | root CloudShell 재조회 결과 모두 0 | 2026-09-25 root CloudShell 조회 |
| 최종 비용 | 2026-09 청구서에서 CloudFormation·Data Transfer·EC2·KMS·VPC가 각각 USD 0.00, 총 세금 USD 0.00 | 2026-09-25 Billing 화면 |
| 배포·검증·정리 실행 주체 | b6-1-learner IAM 사용자 | 15-iam-sts-ec2-public.png |

## 현재 상태

웹사이트는 배포·기능 검증 후 삭제됐다. 이번 점검에서도 프로젝트 스택과 위 리소스의 정리 상태를 확인했다. 중단할 EC2가 남아 있지 않아 신규 삭제 작업은 수행하지 않았다. 이전 IP는 현재 서비스 주소가 아니다.

IAM 사용자 `b6-1-learner`로 콘솔과 CloudShell을 사용해 배포·검증·정리를 수행했다. 현재 리소스 조회와 배포·정리 증거를 함께 보관한다.

## 남은 작업

- GitHub 원격 업로드. 로컬 커밋과 원격 push 성공을 구분한다.

## 검증 자료

- [실제 화면 텍스트](17-final-audit-dom.txt)
- [실행한 조회 명령 인수](17-final-audit-commands.json)
- [직전 스택·키페어 확인](16-cleanup-recheck-2026-09-25.txt)

화면 텍스트에는 최초 명령 입력 오류와 이후 정상 실행 결과가 함께 포함된다. 오류 이후 타임스탬프 아래 결과가 최종 검사 출력이다. ACCESS_DENIED는 0개나 정상 판정으로 치환하지 않았다.
