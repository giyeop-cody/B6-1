# B6-1 배포와 검증 가이드

## 0. 현재 진행 상태

2026-08-17에 계정 소유자가 기존 AWS 계정 사용 가능, Console 방식, 단기 비용 가능성을 확인했다. IAM·MFA·Budget·Key Pair 준비와 실제 배포는 아직 실행하지 않았다. 성공 URL과 스크린샷은 실제 확인 후에만 기록한다.

## 1. 로컬 Docker 확인

Docker가 있는 PC에서 저장소를 clone하고 실행한다.

```bash
git clone https://github.com/giyeop-cody/B6-1.git
cd B6-1
scripts/test-local.sh
```

성공 조건:

```text
LOCAL DOCKER TEST: ALL PASS
```

직접 확인:

```bash
curl http://localhost:8080/health
# OK
```

## 2. AWS 사전 준비

[`account-setup.md`](account-setup.md)를 따라 다음을 준비한다.

- 루트가 아닌 IAM 사용자
- 서울 리전
- 크레딧·예산 확인
- 서울 리전 Key Pair `b6-1-key`
- 현재 접속 중인 개인 인터넷의 공인 IPv4

공인 IP는 자신의 PC 터미널에서 확인한다.

```bash
curl -4 https://checkip.amazonaws.com
```

예를 들어 결과가 `203.0.113.10`이면 CloudFormation에는 다음처럼 입력한다.

```text
203.0.113.10/32
```

`0.0.0.0/0`은 SSH에 절대 사용하지 않는다. 휴대전화 테더링이나 공유기를 바꾸면 공인 IP가 달라질 수 있다.

## 3. CloudFormation 콘솔 배포

1. IAM 사용자로 로그인한다.
2. 리전을 **서울 `ap-northeast-2`**로 바꾼다.
3. CloudFormation → Stacks → Create stack
4. **With new resources** 선택
5. Upload a template file 선택
6. `infra/cloudformation.yml` 업로드
7. Stack name: `b6-1-learning`
8. Parameters:
   - `ProjectName`: `b6-1`
   - `KeyName`: `b6-1-key`
   - `AllowedSshCidr`: 내 공인 IP + `/32`
   - `InstanceType`: `t3.micro`
9. 변경 내용을 다시 확인하고 Stack을 만든다.
10. 상태가 `CREATE_COMPLETE`가 될 때까지 기다린다.

CloudFormation은 EC2 안에서 다음 작업이 끝난 뒤 성공 신호를 받는다.

- Docker와 Git 설치
- 이 저장소 clone
- Docker 이미지 build
- 컨테이너 실행
- 내부 `/health`가 `OK`인지 확인

따라서 `CREATE_COMPLETE`는 단순히 EC2만 켜졌다는 뜻이 아니라 내부 헬스체크까지 통과했다는 뜻이다.

## 4. 외부 접속 확인

Stack → Outputs에서 다음 값을 찾는다.

- `WebsiteURL`
- `HealthURL`
- `PublicIp`

브라우저:

```text
http://<PUBLIC_IP>
```

터미널:

```bash
curl -i http://<PUBLIC_IP>/health
```

성공 조건:

```text
HTTP/1.1 200 OK

OK
```

## 5. AWS 콘솔에서 구조 확인

### VPC

- CIDR: `10.0.0.0/16`
- DNS 지원과 DNS hostname 활성화

### Public Subnet

- CIDR: `10.0.1.0/24`
- Public IPv4 자동 할당 활성화
- EC2가 이 Subnet에 연결됨

### Route Table

- `10.0.0.0/16 → local`
- `0.0.0.0/0 → Internet Gateway`

### Security Group

- TCP 80: `0.0.0.0/0`
- TCP 22: 내 공인 IP `/32`
- 전체 포트 공개 규칙 없음

### EC2

- Instance type: `t3.micro`
- AMI: Amazon Linux 2023
- Public IPv4 존재
- 8GiB 암호화 gp3, 종료 시 삭제
- IMDSv2 필수

## 6. SSH와 Docker 확인

```bash
ssh -i /안전한/경로/b6-1-key.pem ec2-user@<PUBLIC_IP>
```

EC2 안에서:

```bash
sudo docker ps
sudo docker inspect --format '{{.State.Health.Status}}' b6-1-web
curl -i http://localhost/health
sudo docker logs b6-1-web
```

기대 결과:

- 컨테이너 `b6-1-web`가 `Up`
- Docker health가 `healthy`
- localhost `/health`가 200과 `OK`

## 7. 자동 AWS 검사

저장소를 AWS CloudShell에 clone한 뒤 실행한다.

```bash
scripts/aws-verify.sh b6-1-learning | tee evidence/aws-verification.txt
```

CloudShell은 현재 로그인한 IAM 세션을 사용하므로 Access Key를 저장소에 넣을 필요가 없다. `infra/deployer-policy.json`은 세션 생성과 자격 증명 전달에 필요한 CloudShell Action만 허용하며 파일 upload/download Action은 허용하지 않는다.

## 8. 필요한 증거

[`evidence/README.md`](../evidence/README.md)의 목록대로 실제 화면을 저장한다. 예시 이미지를 성공 증거로 사용하지 않는다.

최소 증거:

1. CloudFormation `CREATE_COMPLETE`
2. VPC와 Public Subnet
3. `0.0.0.0/0 → IGW` Route
4. Security Group 80 전체/22 개인 IP
5. EC2 Running과 Public IP
6. 브라우저 사이트 화면
7. 외부 `/health` 200
8. `docker ps`와 healthy
9. Stack 삭제 완료
10. Billing/리소스 정리 확인

## 9. 실습 종료

증거를 확보한 즉시 [`cleanup-checklist.md`](cleanup-checklist.md)를 따라 Stack과 별도 Key Pair를 삭제한다. EC2를 단순히 Stop한 것으로 끝내지 않는다.
