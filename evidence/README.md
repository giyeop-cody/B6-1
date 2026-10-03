최종 상태(19:17 KST): IAM으로 전체 실습 리소스 정리 완료, 최종 Billing 조회 완료. 최신 증거43~47. 아래 이전 미완료 상태는 실행 이력이다.

최신 정리 상태: 사용자 승인으로 IAM 삭제 실행. EC2/EBS/네트워크 정리 완료, LT·키페어 삭제 권한 거부로 전체 미완료. [평가 설명·증거 안내](../docs/evaluation-evidence-guide-2026-10-03.md). 아래 보류 문구는 삭제 승인 전 기록이다.

# 2026-10-03 재배포 증거

최신 IAM 재수집(18:25~18:42 KST): [검수용 결과](../docs/evidence-review-ready-2026-10-03.md). Billing 홈·프리 티어·크레딧 조회 성공. 세부 청구서 및 청구 문서도 IAM 조회 성공(32·33). 10월 예상 USD 0.00/상세 데이터 없음, 발행 문서 0건. 삭제·해제 보류.

배포·동작 증거는 확보했다. 전체 과제 규정과 비용/정리 증거까지 모두 완료한 것은 아니다. 상세 대조 결과는 [과제 검토](../docs/assignment-audit-2026-10-03.md)에 기록했다. 삭제·해제 및 삭제 후 Billing 확인은 별도 요청 전까지 수행하지 않는다.

외부 URL: http://52.79.115.167 · 서울 ap-northeast-2 · IAM 배포 사용자 b6-1-learner · 스택 b6-1-learning UPDATE_COMPLETE. 실제 앱 커밋은 6bc1076c4311cc2685b483ca326be8bc7e5f4bb1이다.

새 증거는 2026-10-03 폴더에 있다. JPG는 실제 캡처, TXT는 CLI/SSH 출력 또는 브라우저 DOM 기록이다. 13 JPG는 PC에서 SSH로 수집한 원본 출력을 CloudShell에 표시한 캡처다.

| 번호 | 파일 이름(확장자 제외) | 확인 내용 |
|---|---|---|
| 01 | 01-predeployment-check | IAM·리전·배포 전 확인 |
| 02 | 02-keypair-created | 키페어 생성 완료 |
| 03 | 03-deploy-review | 실행 전 검토 |
| 04 | 04-launch-template-denied | 시작 템플릿 권한 실패 |
| 05 | 05-policy-fix-verified | 시작 템플릿 권한 보정 |
| 06 | 06-network-tag-update-denied | 태그 갱신 권한 실패 |
| 07 | 07-network-tags-verified | 실제 소유 태그 |
| 08 | 08-tag-policy-and-launch-audit | 수정 적용 및 권한 검증 |
| 09 | 09-iam-ec2-security-group | IAM·EC2 running·micro·인바운드 전체 |
| 10 | 10-ebs-vpc-route | 암호화 gp3 8GiB·VPC·서브넷·IGW 경로 |
| 11 | 11-browser-home | 실제 외부 사이트 접속 |
| 12 | 12-external-health-200 | PC 외부 HTTP 200 OK(TXT) |
| 13 | 13-ssh-docker-healthy | 실제 SSH·커밋·Docker healthy·내부 HTTP 200 |
| 14 | 14-stack-update-complete | IAM·UPDATE_COMPLETE·외부 HTTP 200 |
| 15 | 15-os-docker-reaudit | SSH OS 명시 확인·Docker·커밋·HTTP(TXT) |
| 16 | 16-live-iam-resource-reaudit | IAM·스택 완료·실행 EC2 1대·AL2023 AMI·키페어 1개 |
| 17 | 17-billing-access-denied | IAM 비용 화면 접근 거부(비용 확인 성공 증거가 아님) |
| 18 | 18-network-ebs-reaudit | EBS·서브넷 경로 연결·전체 인바운드 재검증 |
| 19 | 19-billing-iam-access-enabled | 계정 IAM Billing 접근 활성화(TXT, 준비 기록) |
| 20 | 20-minimum-permissions-prepared | 제한 정책 적용과 허용/거부 검증(준비 기록) |
| 22 | 22-iam-billing-home | IAM 월간 비용·무료 플랜·예산 상태 |
| 23 | 23-iam-policy-key-dryrun | 실제 IAM ARN·연결 정책·스택 완료·키 생성 권한 dry-run |
| 24 | 24-iam-freetier | IAM 프리 티어 화면 |
| 25 | 25-iam-credits | IAM 잔여 크레딧 및 누적 사용 |
| 26 | 26-iam-resources | EC2·EBS·키페어 현재 상태 |
| 27 | 27-iam-network-health | 네트워크·SG·외부 HTTP200 |
| 28 | 28-iam-bills-limitation | 세부 청구서 접근 제한 |
| 29 | 29-current-ssh-docker | 실제 SSH OS·커밋·Docker healthy·내부 HTTP(TXT) |
| 30 | 30-current-browser-home | 새 외부 접속 화면 |
| 31 | 31-billing-readonly-fixed | 공식 Billing 읽기 정책 연결·권한 검증(준비 기록) |
| 32 | 32-iam-bills-success | IAM 세부 청구서 조회 성공·10월 예상 USD 0.00 |
| 33 | 33-iam-invoices-status | IAM 발행 문서 조회 성공·문서 0건 |

아키텍처: ../docs/architecture.svg. IAM 실행과 관리자 준비: ../docs/iam-execution-2026-10-03.md. 실패 원인과 수정: ../docs/troubleshooting.md. manifest.json은 파일 SHA-256과 크기를 기록한다.

필수 배포 URL·아키텍처·IAM 실행·README·외부 접속 및 Docker 증거를 대조했다. 정리 대상은 EC2·EBS·ENI·키페어·시작 템플릿·VPC·서브넷·SG·IGW·라우팅 테이블/연결이다. EIP·NAT·ALB·RDS는 이번 템플릿에서 생성하지 않았다.

로컬 원본 JPG에는 계정 ID 또는 SSH 개인 IP가 보일 수 있다. 공개 게시 전 가림 처리가 필요하며 이번 작업에서 원격 push는 수행하지 않았다. 개인 키·비밀번호·액세스 키는 저장하지 않았다.


| 정리 번호 | 파일 이름(확장자 제외) | 확인 내용 |
|---|---|---|
|34|34-stack-before-delete|IAM 삭제 전 스택|
|35|35-stack-delete-confirm|삭제 대상 확인창|
|36|36-stack-delete-progress|스택 삭제 진행|
|37|37-stack-delete-events|리소스별 삭제 및 LT 권한 거부|
|38|38-cleanup-resource-audit|EC2 terminated·EBS/ENI 없음·추가 조회 제한|
|39|39-key-before-delete|키페어 삭제 전|
|40|40-key-delete-denied|IAM 키페어 삭제 권한 거부|
|41|41-billing-after-ec2-termination|일부 정리 후 IAM Bills|

|42|42-cleanup-permissions-prepared|루트 준비: 정확한 삭제 정책 연결·readback·허용/거부 검증. 실제 IAM 삭제 증거 아님|

|43|43-iam-cleanup-retry-key-deleted|IAM 스택 삭제 재시도·키 삭제 성공|
|44|44-iam-cleanup-complete-audit|DELETE_COMPLETE·EC2 terminated·잔여 자원 조회0개|
|45|45-iam-active-stacks-empty|활성 스택0개|
|46|46-iam-billing-after-cleanup|전체 정리 후 IAM Bills|
|47|47-iam-billing-home-after-cleanup|전체 정리 후 IAM Billing 홈|
