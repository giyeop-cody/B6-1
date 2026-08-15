# B6-1 단계별 학습 기록

> 목표: 어려운 용어를 외우는 대신, 요청이 인터넷에서 웹 서버까지 가는 길을 한 단계씩 확인한다.

## 현재 상태

- AWS 계정: 아직 없음
- 선택한 배포물: Docker로 실행하는 Nginx 정적 사이트
- 인프라 방식: CloudFormation으로 생성하고 AWS 콘솔에서 직접 검증
- 리전: 서울 `ap-northeast-2`
- HTTPS: 사용할 도메인이 없어 HTTP와 Docker를 먼저 완료한 뒤 진행

## 1. 가장 먼저 알아야 할 낱말

| 낱말 | 쉬운 설명 | 이번 과제에서 하는 일 |
|---|---|---|
| AWS 리전 | 서버가 있는 큰 지역 | 서울 리전만 사용한다. |
| VPC | 우리 서버를 넣는 전용 네트워크 울타리 | `10.0.0.0/16` 한 개를 만든다. |
| Public Subnet | 인터넷으로 나갈 길이 있는 작은 구역 | EC2 한 대를 넣는다. |
| Internet Gateway | VPC와 인터넷을 연결하는 출입구 | VPC에 한 개 연결한다. |
| Route Table | 목적지에 따라 어느 길로 갈지 적은 표 | `0.0.0.0/0`을 Internet Gateway로 보낸다. |
| Security Group | 서버 앞의 방화벽 | HTTP 80은 모두, SSH 22는 내 IP만 허용한다. |
| EC2 | AWS에서 빌리는 가상 컴퓨터 | Docker와 Nginx를 실행한다. |
| IAM | 누가 어떤 AWS 작업을 할 수 있는지 정하는 규칙 | 루트 대신 별도 사용자를 사용한다. |
| CloudFormation | AWS 구성도를 코드로 적는 도구 | VPC부터 EC2까지 같은 방식으로 다시 만든다. |
| Docker | 앱과 실행 환경을 한 상자처럼 묶는 도구 | Nginx 사이트를 컨테이너로 실행한다. |

## 2. 요청이 이동하는 순서

```text
사용자 브라우저
  → 인터넷
  → Internet Gateway
  → Public Subnet의 Route Table
  → Security Group의 HTTP 80 검사
  → EC2의 80번 포트
  → Docker 컨테이너
  → Nginx
  → index.html 또는 /health 응답
```

어느 한 단계라도 빠지면 외부 접속이 실패한다. 그래서 문제가 생기면 위에서부터 한 단계씩 확인한다.

## 3. 선택한 구현 방법

### 선택: Nginx 정적 사이트 + Docker

장점:

- 프로그램 구조가 단순해 네트워크와 AWS 학습에 집중할 수 있다.
- `/health`가 항상 같은 `200 OK`를 반환하므로 배포 검증이 쉽다.
- Docker 보너스를 함께 연습할 수 있다.

단점:

- 데이터베이스나 로그인 같은 실제 서비스 기능은 없다.
- Docker를 사용하지 않는 Nginx 직접 설치보다 한 단계 더 배워야 한다.

### 선택: CloudFormation + 콘솔 검증

장점:

- 인프라 구성을 코드로 보관하고 다시 만들 수 있다.
- 삭제도 Stack 단위로 할 수 있어 리소스를 빠뜨릴 위험이 줄어든다.
- 콘솔 화면에서도 실제 VPC, Subnet, EC2, Security Group을 확인할 수 있다.

단점:

- YAML 문법과 오류 메시지를 읽어야 한다.
- 자동 생성만 하고 구조를 이해하지 못할 수 있으므로 각 리소스를 콘솔에서 다시 확인해야 한다.

## 4. 비용에 대해 배운 점

2025년 7월 15일 이후 만든 신규 AWS 계정은 예전의 단순한 “12개월 750시간” 설명과 다르다. 신규 사용자는 Free 또는 Paid Plan을 고르고, 최대 6개월 Free Plan 및 크레딧 방식이 적용될 수 있다. 계정 화면에서 현재 혜택과 만료일을 직접 확인해야 한다.

- 공식 FAQ: https://aws.amazon.com/free/free-tier-faqs/
- EC2 Free Tier 확인: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-free-tier-usage.html

이번 과제는 `t3.micro`, 8GiB `gp3`, EC2 한 대만 사용한다. 그래도 무료라고 단정하지 않고 Billing과 Credits를 확인하고, 실습 후 Stack을 삭제한다.

## 5. 앞으로의 학습 순서

1. AWS 계정 생성과 루트 MFA 설정
2. 루트에서 실습용 IAM 사용자 생성 후 루트 로그아웃
3. 비용 알림과 Credits 확인
4. SSH Key Pair 생성
5. CloudFormation Stack 생성
6. VPC부터 EC2까지 콘솔에서 연결 관계 확인
7. 브라우저와 `/health`로 외부 접속 확인
8. Docker 컨테이너 상태 확인
9. 일부러 한 가지 오류를 재현하고 원인·조치 기록
10. 증거를 저장한 뒤 Stack 삭제와 Billing 확인

## 6. 아직 배우거나 확인하지 못한 것

- 실제 AWS 계정 화면
- 실제 서울 리전 Free Tier/크레딧 표시
- 실제 EC2 Public IP
- 실제 SSH 접속
- 실제 외부 HTTP 응답
- 실제 리소스 삭제 결과와 Billing

확인하지 않은 내용을 성공했다고 기록하지 않는다.
