# 2026-10-03 재배포 작업 범위

최종 상태(17:50 KST 확인): IAM b6-1-learner의 재시도 `2c7c2b00-bf06-11f1-b5eb-063ed9ab78b9`가 UPDATE_COMPLETE. EC2 i-0c37f462250fceaba, 외부 URL http://52.79.115.167, 암호화 gp3 8GiB, Docker healthy, 외부 HTTP 200 및 서버 커밋 6bc1076c4311cc2685b483ca326be8bc7e5f4bb1 확인. 배포·증거 수집 범위는 완료했고 삭제·해제는 수행하지 않았다. 아래 진행 기록의 대기/실패는 각 시점의 상태다.

- 기준 커밋: `6bc1076` (첫 배포·증거 기록 커밋 `794afca` 직전).
- 작업 브랜치: `redeploy-evidence-2026-10-03`.
- 원래 다운로드 폴더와 원격 main은 변경하지 않았다.
- 이번 작업은 배포, 실제 검증, 새 증거 수집 및 누락 확인까지만 수행한다.
- 기존 성공 기록이나 스크린샷은 이번 실행의 성공 증거로 재사용하지 않는다.
- 삭제·해제는 증거 수집 완료를 확인하고 사용자가 별도로 명시적으로 요청한 뒤에만 수행한다. 가이드의 즉시 정리 안내보다 이번 사용자 지시를 우선한다.
- 현재 상태: 사용자가 암호를 재설정하고 IAM으로 로그인했다. STS 조회에서 `arn:aws:iam::[ACCOUNT_ID]:user/b6-1-learner`를 확인했다. 서울에 스택 `b6-1-learning`, 비종료 EC2 및 키페어가 없다. CreateKeyPair dry-run은 UnauthorizedOperation으로 거부됐다. 관리자 IAM/Role의 키페어 준비를 대기하며, 실제 리소스 생성은 아직 수행하지 않았다.
- 배포 전 비용 화면: 무료 플랜 계정 안내, 2026년 10월 누계 USD 0.00, 예산 미생성. 이번 배포 비용이나 최종 청구액을 의미하지 않는다.
- 무료 플랜 계정 메뉴에서 남은 크레딧 USD 119.97, 138일을 확인했다.
- CloudShell에 기준 커밋을 checkout하고 제한 정책 호환용 템플릿을 준비했다. AWS CloudFormation ValidateTemplate 통과. 이 검증은 생성 권한이나 실제 배포 성공을 의미하지 않는다.
- 변경: 앱 커밋 고정, SSH /32 강제, t3.micro만 허용, EBS/ENI 생성 시 Project 태그, standard CPU credits. IAM 정책의 확대·변경은 수행하지 않았다.
- 사전 검증 증거: `evidence/2026-10-03/01-predeployment-check.jpg`, `.txt`. 배포 성공 증거와 구분한다.
- 16:56 KST 관리자 세션에서 `b6-1-key` 생성 완료 화면 확인. 키 ID `key-019496eb4f525d687`, RSA. 기존 생성 완료를 확인했으므로 중복 생성하지 않았다. 개인 키는 `C:/Users/Win10/Downloads/b6-1-key.pem`에 존재하며 내용을 출력하거나 저장소에 복사하지 않았다. 생성 완료 화면은 `evidence/2026-10-03/02-keypair-created.jpg`.
- 관리자 세션에서 실습 사용자 연결 정책 3개와 인라인 정책 없음 확인. 실제 연결 정책 기준 시뮬레이션에서 서울 CloudFormation CreateStack, EC2 CreateVpc/CreateLaunchTemplate, RunInstances의 instance/volume/ENI/subnet/SG/launch-template/key/AMI 대상 모두 allowed, missing context 없음. 시뮬레이션은 실제 배포 성공을 대체하지 않는다.
- 다음 단계: `b6-1-learner`로 전환한 뒤 STS를 다시 확인하고, 준비된 CloudShell 템플릿으로 배포. 관리자 세션에서는 스택/EC2를 생성하지 않았다.
- IAM 재로그인 및 사용자 승인 후 실제 CreateStack 수행. 스택 ID의 마지막 부분은 `7bdf99c0-bf01-11f1-99f8-02e7e30b774b`. DisableRollback=true로 생성해 실패 시 자동 삭제하지 않도록 했다.
- 실제 결과: 네트워크와 LaunchTags 생성 완료, WebInstance는 RunInstances의 launch-template 권한 거부로 CREATE_FAILED. 스택은 CREATE_FAILED이며 사이트 배포 성공으로 판정하지 않는다.
- 원인: 실제 `lt-03da8c5fb9551abf8`에는 Project=b6-1 태그만 있다. 시뮬레이션에는 AWS 스택 태그가 있다고 가정했으나 실제 태그에 없어서 기존 UseOwnLaunchDependencies 조건이 충족되지 않았다.
- 제한 수정안 `infra/launch-template-use-policy.json`: 정확히 이번 시작 템플릿 ARN의 RunInstances만, 서울·CloudFormation 경유·Project 태그 조건으로 허용한다. 아직 AWS에 적용하지 않았다. 관리자 승인과 세션을 대기한다.
- 실패 증거는 `evidence/2026-10-03/04-launch-template-denied.jpg`와 `.txt`. 생성된 네트워크·시작 템플릿과 키페어는 보존 중이다. EC2는 생성되지 않았다.
- 사용자 승인 후 관리자 준비 세션에서 인라인 정책 `B61UseExactLaunchTemplate20261003`을 b6-1-learner에 추가했다. Access Analyzer findings `[]`, 저장된 정책 readback 일치 확인.
- 실제 시작 템플릿 태그로 재검증: actual-template allowed, direct-call implicitDeny, other-template implicitDeny. 스택 태그를 가정하지 않았다. 증거는 `05-policy-fix-verified.jpg`, `.txt`.
- 실제 스택 재시도는 아직 하지 않았다. IAM 재로그인 후 같은 스택을 보존한 채 업데이트하여 실패한 EC2 생성만 재시도할 예정이다. 스택 삭제나 리소스 해제는 하지 않았다.

## 배포 전 확인

- 관리자 준비 세션에서 제한 인라인 정책 `B61RetagExactNetwork20261003`을 적용했다. Access Analyzer findings `[]`, 정책 readback 일치. 실제 세 네트워크 리소스의 태그를 사용한 CreateTags 시뮬레이션은 allowed, CloudFormation 경유 없는 직접 변경은 implicitDeny.
- 실제 서브넷·보안 그룹·시작 템플릿 태그에 따른 RunInstances, t3.micro/IMDSv2/default tenancy 인스턴스, 암호화 gp3 8GiB 볼륨, Project 태그 ENI, b6-1-key, Amazon AL2023 이미지, 생성 시 태그와 UpdateStack까지 allowed 확인. 시뮬레이션은 실제 배포 완료 증거를 대체하지 않는다. `08-tag-policy-and-launch-audit.jpg`, `.txt`에 기록했다.

- IAM 세션에서 UpdateStack 재시도(op `eb7a6470-bf03-11f1-a7c8-064f9dca5c31`)했으나 `UPDATE_FAILED`. 기존 InternetGateway, PublicRouteTable, WebSecurityGroup의 `ec2:CreateTags` 권한이 생성 시에만 허용되어 갱신이 거부되었다. EC2는 아직 생성되지 않았다. 실패 증거는 `06-network-tag-update-denied.jpg`, `.txt`.
- 세 리소스의 실제 Project 및 CloudFormation stack-name 태그를 개별 Describe API로 확인했다. 모두 `b6-1`, `b6-1-learning`이다. 증거는 `07-network-tags-verified.jpg`, `.txt`.
- `infra/owned-network-tag-update-policy.json`에 정확히 세 ARN의 CreateTags만 서울·CloudFormation 경유·기존 소유 태그 조건으로 허용하는 정책을 준비했다. 아직 적용하지 않았다. 삭제·해제 작업은 수행하지 않았다.

- 루트가 아닌 IAM 사용자/Role 세션 확인.
- 서울 리전 `ap-northeast-2`, 계정의 프리 티어/크레딧 및 예산 확인.
- 기존 스택과 프로젝트 리소스 유무 확인. 기존 리소스를 삭제하지 않는다.
- micro 인스턴스 1대, Amazon Linux, 암호화 EBS 8GiB, HTTP 80 공개, SSH 22 개인 IP /32 확인.
- 현재 제한 IAM 정책과 과거 템플릿·스크립트의 호환성 검토. 광범위한 과거 정책을 그대로 적용하지 않는다.
- EC2가 원격 main 대신 검토한 배포 기준 코드를 사용하도록 고정한다.
- 키페어 1개와 개인 키의 안전한 보관 상태 확인.

## 이번 실행 증거 체크리스트

- [x] IAM 사용자/Role 접근 기록 (CloudShell STS ARN 확인)
- [x] 배포 커밋, 시각, 리전, 스택 및 리소스 목록
- [x] CloudFormation 생성/업데이트 완료
- [x] VPC, Public Subnet, IGW 및 기본 라우팅
- [x] HTTP 80 공개 및 SSH 22 /32 보안 그룹
- [x] EC2 running, 인스턴스 유형, Public IP, EBS 구성
- [x] 실제 브라우저 외부 접속 화면 (필수 외부 접속 증거 1장)
- [x] 외부 /health HTTP 200 및 OK
- [x] SSH, docker ps healthy 및 localhost 응답 (Docker 보너스)
- [x] 아키텍처, 배포 URL, 비용 관리 README
- [x] 실제 문제 발생 시 트러블슈팅 기록
- [x] 새 증거 파일 존재 및 내용 대조, 누락 확인

삭제 완료나 삭제 후 Billing 증거는 이번 수집 완료 판정에 포함하지 않는다. 해당 단계는 별도 요청 이후 진행한다.
