# B6-1 개발 기록

## 2026-08-15 — 범위 결정

- AWS 계정 없음 확인
- Nginx 정적 사이트와 Docker 선택
- CloudFormation + 콘솔 검증 선택
- 도메인이 없어 HTTPS 후속 처리 결정
- 실제 확인하지 않은 배포 증거는 작성하지 않기로 결정

## 2026-08-15 — 학습과 이슈 기록

- VPC부터 Nginx까지 요청 흐름을 중학교 졸업 수준의 표현으로 정리
- 구현 전 선택지의 장단점 기록
- AWS 계정 부재와 Docker/AWS CLI 부재를 이슈로 기록

## 2026-08-15 — 웹 서비스

- 외부 리소스 없는 반응형 정적 사이트 구현
- Nginx `/health` 200 응답 구현
- Docker healthcheck 구현
- 로컬 Docker 자동 검사 스크립트 작성
- 현재 환경에는 Docker가 없어 실제 build/run은 미실행

## 2026-08-15 — 인프라

- VPC, Public Subnet, IGW, Route Table, Security Group, EC2 CloudFormation 작성
- SSH 전체 공개를 거부하는 Rule 추가
- Amazon Linux 2023, t3.micro, 암호화 8GiB gp3, IMDSv2 적용
- User Data에서 저장소 clone → build → run → health → cfn-signal 흐름 구현
- IAM 배포 정책에서 AdministratorAccess를 사용하지 않고 서울 리전으로 제한

## 2026-08-15 — 보안과 문서

- `.pem`, `.key`, `.env`, `.aws` Git 추적 차단
- 단순 비밀정보 검사 스크립트 추가
- 신규 AWS Free Plan이 예전 12개월 방식과 다를 수 있음을 공식 자료로 확인
- 계정·IAM·배포·검증·삭제·증거 수집 순서 문서화

## 2026-08-17 — 계정 경로와 IAM 배포 전 점검

- 계정 소유자가 기존 AWS 계정 사용 가능과 단기 비용 가능성을 확인
- 비밀 키를 공유하지 않는 AWS Console + CloudShell 검증 경로 선택
- 기존 최소권한 정책에 Console 목록·템플릿 요약과 SSM public AMI 읽기 권한이 빠진 문제 발견
- GitHub Issue #5로 기록하고 실패하는 자동 검사를 먼저 추가
- 서울 리전 조건을 유지하며 필요한 Action만 보완
- CloudShell 파일 upload/download 권한은 제외

## 2026-08-25 — 병합 기록 동기화와 문서 정합성 점검

- ISSUE-005에 PR #6의 main 병합 완료 상태를 반영
- 과제 정보 표의 학습 시간(40시간) 표기가 README와 같은 값인지 확인
- 학습 노트에 헷갈렸던 두 보안 장치 구분과 직접 설치 비교 정리
- 증거 보관 규칙에 명령 출력 텍스트 원본 항목 추가

## 남은 작업

- IAM 사용자 MFA, Plan·크레딧·Budget 실제 화면 확인
- Docker PC에서 로컬 이미지 실증
- SSH private key 확보 후 실제 SSH/Docker 화면 증거
- 외부 접속 증거 이미지 추가 수집
- Stack 삭제와 Billing 확인

## 2026-09-24 — 실제 배포 및 과제 기준 점검

- 서울 리전 `b6-1-learning` Stack `CREATE_COMPLETE` 및 업데이트 `UPDATE_COMPLETE` 확인
- 외부 홈페이지 `HTTP 200`, `/health` `HTTP 200 OK` 확인
- 아키텍처 제출용 `docs/architecture.pdf` 추가
- 외부 사이트 화면 `evidence/06-browser-home.jpg` 저장
- IAM 정책 레거시 파서 오류를 새 고객 관리형 정책 2개 생성으로 해결하고 기존 광범위 정책 분리
- UserData에 EC2 아웃바운드 확인 명령을 추가하고 Stack 업데이트
- Key Pair private key가 로컬에 없어 SSH 세션 증거는 미수집; 임시 Instance Connect 검증 시 인증이 거부되어 임시 SG 규칙은 즉시 제거
- Stack과 과금 리소스는 아직 실행 중이며 cleanup checklist와 Billing 확인이 남아 있음

### 최종 원문 대조 보정

- 원격 main 6bc1076 기준으로 Git 이력을 연결하고 `git pull --ff-only origin main`: Already up to date. 로컬 수정은 보존했으며 원격 push는 미실행.
- 루트 실행 이력을 과제 제약 불일치로 명시하고 배포 스크립트에 root 차단 추가. IAM 로그인 전환 후 실제 제한 권한 배포 검증 필요.
- 필수 증거는 외부 접속 1장, Docker 보너스는 docker ps 및 외부 접속 2장 이상으로 보정.
- PDF를 UTF-8 텍스트로 읽던 검사 오류와 분리 정책 이전의 오래된 검사 조건 수정. 정적 검사 15개 필수 파일 및 9개 CloudFormation 리소스 ALL PASS. git diff --check 통과.

### 2026-09-24 증거 보관 및 실습 종료

사용자가 증거 전체 스크린샷 보관 후 리소스 해제를 요청했다. 스크린샷 17장 저장. EC2 Instance Connect 일회성 공개 키와 CloudShell /32 제한 규칙을 이용해 SSH 접속 성공, docker ps healthy / localhost 200 / example.com 아웃바운드 200 확인. 임시 규칙 제거 확인.

20:46:09 KST 스택 삭제 요청, 20:46:59 KST DELETE_COMPLETE 및 9개 리소스 삭제 확인. 20:48:03 KST 실습 키페어 삭제와 서울 비종료 인스턴스 0 확인. EBS/EIP/Snapshot/NAT/ELB/RDS 0 확인. Billing은 0달러 표시이나 집계 중이고 크레딧 100달러 표시. IAM 전용 실행 조건은 루트 사용으로 미충족이다.

## 2026-09-25 — IAM 접근 증거 보완

06:55 KST 현재 b6-1-learner IAM 콘솔 로그인, STS 사용자 ARN, 서울 비종료 EC2 0을 실제로 확인했다. 공개용 캡처에서 계정 번호를 제외했다. 기존 root 실행 이력은 유지하고 IAM 콘솔 접근과 과거 배포 실행 주체를 구분해 문서를 보정했다.

### 2026-09-25 07:11 KST — IAM 세션 최종 점검

IAM 사용자 b6-1-learner로 스택 DELETE_COMPLETE, 서울 비종료 EC2/EBS 0, 프로젝트 VPC/Subnet/SG/RouteTable/IGW 0을 확인했다. CloudTrail, EIP, Snapshot, NAT, ELB, RDS, Cost Explorer 조회는 접근 거부됐다. 현재 결과와 과거 기록을 구분한 evidence/final-audit-2026-09-25.md를 추가했다.
