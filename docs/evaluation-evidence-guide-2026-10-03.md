# B6-1 평가 항목별 설명과 증거 안내

기준: 저장소 QUEST.md의 학습 목표·최종 결과물·제약 사항. 별도의 점수표는 제공되지 않았으므로 아래는 과제 항목 대응표이며 공식 배점표가 아니다.

현재 상태: 2026-10-03 19:17 KST IAM으로 남은 삭제 완료. 스택 DELETE_COMPLETE, EC2 terminated, EBS/EIP/NAT/키페어/LT/ALB/RDS/스냅샷 0개, 해당 VPC/서브넷/SG/RT/IGW/ENI 없음. 증거43~47. 과거 실패 이력37·40과 루트 준비 이력42는 보존한다.

## 발표 순서와 보여 줄 자료

증거 경로의 기준은 evidence/2026-10-03/이다. JPG는 실제 화면이고 TXT는 원본 출력/화면 상태다. 번호는 evidence/README.md에 연결된다.

| 과제 항목 | 설명할 이야기 | 보여 줄 증거 | 판정과 주의점 |
|---|---|---|---|
| 실제 웹 배포 URL | “서울 EC2에서 Docker Nginx로 웹사이트를 배포했고 인터넷에서 사이트와 /health 응답을 확인했습니다. 실습 정리를 위해 이후 인스턴스를 종료했습니다.” | 30-current-browser-home.jpg, 12-external-health-200.txt, 14-stack-update-complete.jpg | 과거 실행 URL http://52.79.115.167. 종료 후에는 서비스 URL이 동작한다고 소개하지 않음 |
| VPC/서브넷/라우팅 구성 설명 | “VPC 10.0.0.0/16 안에 퍼블릭 서브넷 10.0.1.0/24를 두고 기본 경로를 IGW에 연결했습니다.” | docs/architecture.svg, 27-iam-network-health.jpg/TXT, 18-network-ebs-reaudit.txt | 서울. IGW 연결·서브넷 경로로 외부 통신 설명 |
| EC2 배포와 실행 환경 | “Amazon Linux 2023, t3.micro 1대, 암호화 gp3 8GiB에서 Docker 서비스를 실행했습니다.” | 26-iam-resources.jpg/TXT, 29-current-ssh-docker.txt | 실제 서버 앱 커밋 6bc1076c4311cc2685b483ca326be8bc7e5f4bb1. 인프라 템플릿은 제한 IAM에 맞춰 수정됨 |
| 웹 서비스 동작 검증 | “외부 HTTP200과 SSH 내부 /health 및 Docker healthy를 함께 확인했습니다.” | 30-current-browser-home.jpg, 27-iam-network-health.txt, 29-current-ssh-docker.txt | 실제 출력으로 확인. 13 JPG는 PC SSH 출력을 CloudShell에 표시한 캡처 |
| IAM 사용자 사용 | “스택 생성·업데이트·서비스 조회·Billing 조회·정리 실행은 b6-1-learner로 진행했습니다. 준비 과정의 루트 사용은 별도 기록했습니다.” | 23-iam-policy-key-dryrun.jpg/TXT, 14-stack-update-complete.jpg, 32-iam-bills-success.jpg, 37-stack-delete-events.jpg, docs/iam-execution-2026-10-03.md | 루트 금지 규정과 준비 이력 사이 차이는 남음. IAM 전용 전 과정이라고 주장하지 않음 |
| 키페어 1개와 안전 보관 | “키페어 b6-1-key 1개를 사용했고 개인 키는 저장소 밖에 보관했습니다. 기존 생성은 루트였으며 IAM 생성 권한은 dry-run으로 확인했습니다.” | 02-keypair-created.jpg, 23-iam-policy-key-dryrun.txt, 26-iam-resources.txt | dry-run은 실제 생성 증거가 아님. IAM 키페어 삭제 완료(43·44), 과거 권한 거부는40 |
| HTTP·SSH 최소 포트 | “HTTP80은 인터넷 전체, SSH22는 개인 IPv4 /32만 허용했습니다. 모든 포트 공개 규칙은 없습니다.” | 27-iam-network-health.txt, 09-iam-ec2-security-group.jpg/TXT, 18-network-ebs-reaudit.txt | 공개 제출용 SSH 주소는 가림 처리 후 설명 |
| 프리 티어·비용 관리 | “micro 1대와 EBS8GiB로 구성하고 별도 EIP/NAT/ALB/RDS는 템플릿에서 만들지 않았습니다. IAM으로 무료 플랜·크레딧·청구 화면을 확인했습니다.” | 24-iam-freetier.jpg, 25-iam-credits.jpg, 32-iam-bills-success.jpg, 33-iam-invoices-status.jpg | 잔여 크레딧119.97, 누적 사용0.03. 10월 예상0.00은 최종 금액 확정이 아님. 발행 문서0건 |
| 실습 후 종료·삭제 추적 | “삭제 전에 증거 필요성을 판단하고 스택 확인창과 리소스별 삭제 이벤트를 저장했습니다.” | 34-stack-before-delete.jpg, 35-stack-delete-confirm.jpg, 36-stack-delete-progress.jpg, 37-stack-delete-events.jpg, 38-cleanup-resource-audit.jpg/TXT | EC2 terminated, EBS/ENI 없음, VPC/서브넷/IGW/SG/RT 삭제. LT 권한 보정 후 IAM DELETE_COMPLETE(43·44), 활성 스택0개(45) |
| Elastic IP·NAT·ALB·RDS·스냅샷 잔여 조회 | “EIP/NAT/ALB/RDS는 생성하지 않았으며, 정리 후 서울 계정 목록도 0개임을 확인했습니다.” | infra/cloudformation.yml, 38-cleanup-resource-audit.txt | 템플릿 미생성과 실제 계정 잔여 없음은 구분. 권한 보정 후 실제 잔여 조회 완료(44), 과거 조회 거부는38 |
| 종료 후 Billing 확인 권장 | “전체 정리 후 IAM Bills와 Billing 홈을 재확인했습니다. 청구 데이터 반영 지연을 고려해 다음 날에도 확인할 예정입니다.” | 46-iam-billing-after-cleanup.jpg/TXT, 47-iam-billing-home-after-cleanup.jpg/TXT | 전체 정리 후 조회 완료. 후속 확인 예정 2026-10-04 19:30 KST(자동 일정 미설정) |
| README와 아키텍처 | “README에 실행 당시 URL, 아키텍처, 비용 방침과 정리 상태를 함께 기록했습니다.” | README.md, docs/architecture.svg, docs/cleanup-checklist.md, evidence/README.md | 실제 현재 상태를 표시하고 원격 게시 여부 구분 |
| 트러블슈팅 최소1건 | “IAM 조건 때문에 시작 템플릿 사용·네트워크 태그 갱신에 실패했고 대상 리소스로 범위를 좁혀 해결했습니다. Billing 조회 의존성도 보정했습니다.” | docs/troubleshooting.md, 04~08, 14, 31~33 | 증상→원인→검증→조치→결과→재발 방지 순서. 삭제 권한 누락은 37·40으로 별도 기록 |

## 정리 증거를 선택한 근거

| 단계 | 스크린샷 필요 여부 | 이유·현재 파일 |
|---|---|---|
| 삭제 전 스택·확인창 | 필요 | IAM 수행자와 삭제 대상 확인: 34·35 |
| 삭제 진행·리소스별 이벤트 | 필요 | EC2 종료, 경로 해제, IGW 분리와 각 자원 삭제 과정 증명: 36·37 |
| EC2/EBS/ENI 잔여 상태 | 필요 | 과금 대상 종료·볼륨 삭제 검증: 38 |
| 키페어 삭제 | 필요 | 스택 밖 자원이라 별도 전/후 필요. 전 화면39·실패40·성공43·잔여 없음44 확보 |
| 미생성 EIP/NAT/ALB/RDS | 잔여 없음 화면 필요 | 생성하지 않았다면 해제 스샷은 해당 없음. 조회 성공 및 잔여0개44 |
| Billing | 필요(과제 권장) | 비용 조회 상태·시점 기록. 일부 정리 후41, 전체 정리 후46·47 확보 |

원본 증거를 고쳐 실제와 다른 실행자로 만들지 않는다. 발표용 이미지는 계정 ID·개인 IP 가림본을 별도로 만들고 원본과 해시를 보존한다. 별도 평가 점수표가 제공되면 그 표와 다시 대조한다.

## 최종 정리 증거

43: 실제 IAM 삭제 요청·키페어 삭제 성공. 44: 스택 DELETE_COMPLETE 및 모든 대상 잔여 조회. 45: 활성 스택0개. 46: 전체 삭제 후 Bills(19:17:54 KST, 10월 예상USD0.00/데이터 없음). 47: 전체 삭제 후 Billing 홈. 현재 권한 보정은 적용 완료이며 남은 AWS 실습 리소스 삭제 작업은 없다. 로컬 PEM과 IAM 사용자·정책은 보존했다.
