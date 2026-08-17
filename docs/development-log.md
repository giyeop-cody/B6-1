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

## 남은 작업

- AWS 계정 생성 및 안전 설정
- Docker PC에서 로컬 이미지 실증
- AWS `validate-template`
- Stack 생성과 외부 접속
- 실제 AWS 트러블슈팅 1건
- 증거 이미지
- 리소스 삭제와 Billing 확인
