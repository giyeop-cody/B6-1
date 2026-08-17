# ADR-001: Docker Nginx와 CloudFormation을 선택한다

- 상태: 결정
- 날짜: 2026-08-15

## 문제

B6-1은 AWS 네트워크, 보안, IAM, EC2 배포, 외부 접속, 비용 정리를 함께 학습해야 한다. 현재 AWS 계정과 도메인은 없다.

## 비교한 선택지

| 선택지 | 장점 | 단점 | 결과 |
|---|---|---|---|
| Nginx 정적 사이트 | 가장 단순하고 `/health` 검증이 쉬움 | 서비스 기능이 단순함 | 채택 |
| B5-2 FastAPI 재사용 | 실제 CRUD를 배포할 수 있음 | DB·Python·영속성까지 범위가 커짐 | 보류 |
| AWS 콘솔만 사용 | 화면 학습이 쉬움 | 재현 가능한 코드가 없음 | 단독 사용 안 함 |
| AWS CLI만 사용 | 자동화하기 쉬움 | 초보자가 구조를 놓칠 수 있음 | 단독 사용 안 함 |
| CloudFormation + 콘솔 | 재현성과 화면 학습을 함께 확보 | YAML과 Stack 오류를 배워야 함 | 채택 |

## 결정

1. `site/`의 정적 페이지를 Nginx Docker 컨테이너로 제공한다.
2. `GET /health`는 `200 OK`와 `OK`를 반환한다.
3. CloudFormation이 VPC, Public Subnet, Internet Gateway, Route Table, Security Group, EC2를 생성한다.
4. HTTP 80은 전체 인터넷에 열고 SSH 22는 사용자가 입력한 개인 IP `/32`에만 연다.
5. 모든 리소스는 서울 리전에서 만들고 공통 태그를 붙인다.
6. 도메인이 없으므로 HTTPS는 후속 작업으로 남기고, 필수와 Docker 보너스를 먼저 검증한다.

## 결과와 위험

- 장점: Stack 하나로 생성·삭제할 수 있고 네트워크 흐름이 코드에 남는다.
- 위험: User Data에서 GitHub clone이나 Docker build가 실패할 수 있다.
- 대응: `cloud-init-output.log`, `docker ps`, `docker logs`, 로컬 `curl`을 순서대로 확인하는 문서를 제공한다.
- 비용 위험: Stack을 지워도 별도로 만든 Key Pair는 남는다. 종료 체크리스트에서 Stack, EC2, EBS, Elastic IP, Key Pair, Billing을 각각 확인한다.
