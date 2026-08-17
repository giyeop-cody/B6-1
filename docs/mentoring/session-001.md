# 학습 멘토 대화 기록 001

- 날짜: 2026-08-15
- 주제: 처음 AWS 배포를 어떤 크기로 시작할 것인가

## 학생 질문

“아직 AWS 계정도 없는데 VPC, Docker, HTTPS를 한 번에 모두 하면 되는가?”

## 멘토 답변

한꺼번에 성공시키려고 하지 말고 확인 가능한 층으로 나누는 것이 좋다.

1. 로컬 정적 페이지가 있는지 확인한다.
2. Docker에서 Nginx가 `/health`를 반환하는지 확인한다.
3. AWS 네트워크와 EC2를 만든다.
4. EC2 내부 `curl localhost/health`를 확인한다.
5. 외부에서 Public IP로 확인한다.
6. 도메인을 준비한 뒤 HTTPS를 추가한다.

HTTPS부터 시작하면 DNS, 인증서, 방화벽, Nginx 문제가 섞여 초보자가 원인을 나누기 어렵다.

## 학생 반론

“CloudFormation을 사용하면 AWS 화면을 배우지 못하지 않는가?”

## 멘토 답변

자동 생성 후 콘솔에서 다음 연결을 직접 찾으면 된다.

- EC2가 어느 VPC와 Subnet에 있는가
- Subnet Route Table의 기본 경로가 어디로 가는가
- Security Group이 80과 22를 누구에게 허용하는가
- EC2에 Public IPv4가 있는가

즉, CloudFormation은 반복 입력을 줄이는 도구이고 이해를 대신하는 도구가 아니다.

## 결정

- 구현은 CloudFormation으로 재현 가능하게 만든다.
- 검증은 AWS 콘솔 화면과 명령어를 모두 사용한다.
- 실제로 확인하지 않은 URL, 스크린샷, Billing 결과는 작성하지 않는다.
