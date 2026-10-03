# B6-1 배포와 검증 가이드

> **최신 상태 (2026-09-25):** IAM 사용자 콘솔·CloudShell 사용 및 스택 삭제/리소스 정리 재확인을 완료했다. 아래 9월 24일 내용은 당시 기록이며, 현재 판정은 [최종 점검 결과](../evidence/final-audit-2026-09-25.md)를 기준으로 확인한다.

> **2026-09-24 권한 변경:** 기존의 서울 전체 EC2 변경 정책은 사용하지 않는다. [배포 권한 경계](deployment-permissions.md)를 먼저 확인하고, 두 정책을 검증·적용한 뒤 진행한다. AWS 적용·실제 배포 검증 전에는 완료로 표시하지 않는다.

## 0. 현재 진행 상태

2026-09-24 실제 배포를 완료했다. 서울 리전 `ap-northeast-2`에서 CloudShell을 통해 `b6-1-learning` CloudFormation 스택을 생성했고 `CREATE_COMPLETE`를 확인했다.

- Stack ARN: `arn:aws:cloudformation:ap-northeast-2:000000000000:stack/b6-1-learning/35f77ae0-b803-11f1-b574-0ac887d3ca55`
- Website: [http://13.125.21.155](http://13.125.21.155)
- Health: [http://13.125.21.155/health](http://13.125.21.155/health) → `HTTP 200 OK`
- EC2: `i-093226b9e4314ad26` (`t3.micro`, `running`)
- CloudFormation 이벤트에 `Received SUCCESS signal`이 남아 EC2 내부 Docker/Nginx `/health` 검사가 통과했다.
- 외부 홈페이지 응답도 `HTTP 200`이며 제목 `인터넷에서 내 서버까지.`를 확인했다.
- CLI 검증 결과를 [evidence/aws-verification.txt](../evidence/aws-verification.txt)에 저장했다.

CloudShell에서 `B61DeployerPolicyRestricted`와 `B61Ec2DeploymentPolicy`를 생성·검증하고 `b6-1-learner`에 연결했으며, 기존 광범위 `B61DeployerPolicy`는 분리했다. 실제 Stack 생성은 `b6-1-learner` IAM 사용자 세션에서 수행했다.

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

## 3. CloudShell 배포 (제한 정책의 기본 경로)

최신 로컬 수정본을 먼저 검토·동기화한다. 원격 저장소가 예전 상태라면 clone 결과로 배포하지 않는다. CloudShell에서 검토한 `cloudformation.yml`을 저장한 뒤 `scripts/deploy-stack.sh b6-1-key <내공인IPv4/32>`를 실행한다. 이 스크립트는 첫 실행에는 `create-stack`, 같은 이름의 스택이 있으면 검토한 템플릿으로 `update-stack`을 사용하므로 변경 세트·S3 업로드 권한을 요구하지 않는다. 실행 역할은 지정하지 않는다.

### 콘솔 업로드 경로 (추가 권한 검토가 필요한 대안)

아래 업로드 방식은 S3 템플릿 저장 권한이 필요할 수 있다. 현재 제한 정책에는 S3 권한을 넣지 않았으므로 기본 경로는 위 CloudShell 방식이다.


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

1. `docs/architecture.pdf`
2. CloudFormation `CREATE_COMPLETE` 또는 `UPDATE_COMPLETE`
3. VPC와 Public Subnet
4. `0.0.0.0/0 → IGW` Route
5. Security Group 80 전체/22 개인 IP
6. EC2 Running과 Public IP
7. 브라우저 사이트 화면 (`evidence/06-browser-home.jpg`)
8. 외부 `/health` 200
9. `docker ps`와 healthy (SSH 검증 후 추가)
10. Stack 삭제 완료
11. Billing/리소스 정리 확인

## 9. 실습 종료

증거를 확보한 즉시 [`cleanup-checklist.md`](cleanup-checklist.md)를 따라 Stack과 별도 Key Pair를 삭제한다. EC2를 단순히 Stop한 것으로 끝내지 않는다.

## 권한 적용 및 실제 실행 상태 (2026-09-24)

- 로컬 제어 정책과 EC2 정책은 Access Analyzer 검증 및 시뮬레이션을 통과했다.
- 콘솔의 기존 정책 버전 교체는 레거시 파서 오류가 있어 새 고객 관리형 정책으로 우회했다. `B61DeployerPolicyRestricted`와 `B61Ec2DeploymentPolicy`는 Access Analyzer에서 오류·경고 0건으로 검증됐다.
- `b6-1-learner`에는 위 두 정책과 `IAMUserChangePassword`만 연결되어 있고 기존 광범위 `B61DeployerPolicy`는 분리되어 있다.
- 조건을 포함한 IAM 시뮬레이션에서 서울 리전 CloudFormation 생성과 EC2 조회는 허용되고, S3 전체 조회와 IAM Access Key 생성은 거부됐다.
- `b6-1-learner` IAM 사용자 세션의 CloudShell에서 실제 Stack을 생성했다. Stack은 `CREATE_COMPLETE`, 외부 사이트와 `/health`는 각각 `HTTP 200`이었다.

## 과제 원문 대조 (2026-09-24 중간 기록 — 아래 최종 결과로 갱신됨)

- 아키텍처 제출 규격: `docs/architecture.pdf`를 추가했고, SVG 원본도 유지한다.
- 외부 접속 증빙: README에 B 방식(`/health`) URL을 기록했고 CloudShell에서 `HTTP 200`과 `OK`를 확인했다. 화면 캡처는 아직 추가하지 않았다.
- 트러블슈팅 보고서: IAM 정책 레거시 파서 오류와 검증·조치·재발방지를 이 문서의 `docs/troubleshooting.md`에 기록했다.
- 네트워크: VPC, Public Subnet, IGW, `0.0.0.0/0 → IGW`, HTTP 80 공개, SSH 22 개인 IP 제한을 확인했다.
- 컴퓨트: EC2 `t3.micro`, Amazon Linux 2023, 암호화 8GiB gp3, IMDSv2, Docker Nginx를 사용한다. CloudFormation ResourceSignal은 내부 `/health`를 통과했다.
- 아웃바운드: 템플릿 UserData에 `https://example.com` 확인을 추가했다. 기존 실행분은 업데이트 배포 후 이 검사를 다시 확인해야 한다.
- SSH: Key Pair 리소스는 존재하지만 `.pem` 다운로드가 확인되지 않아 실제 SSH 세션 증거는 미수집 상태다.
- 정리: Stack은 현재 실행 중이다. 제출·증거 수집 후 `docs/cleanup-checklist.md`에 따라 EC2, EBS, IGW, VPC와 Key Pair를 확인하고 삭제한다.

### 과제 제약에 따른 실행 주체 및 업데이트 주의

배포 전 `aws sts get-caller-identity --query Arn --output text`로 실습 사용자 또는 Role 세션인지 확인한다. 배포 스크립트는 root ARN이면 중단한다. 제한된 IAM으로 배포·검증·정리 증거를 남긴다.

UserData 수정 및 UPDATE_COMPLETE는 새 명령 실행의 증거가 아니다. 기존 EC2에서 SSH로 `curl -i http://localhost`, `curl -fsS https://example.com`, `docker ps`를 직접 실행해 결과를 남긴다. SSH 개인 키가 없으면 기존 키를 다시 다운로드할 수 없으므로 안전한 접속 복구 방법을 결정해야 한다.

원문 외부 접속 증거 최소 수량은 1장이다. Docker 보너스에는 docker ps와 외부 접속 화면 2장 이상이 필요하다. 로컬 Docker 검사와 12종 추가 캡처는 프로젝트 권장 점검이며 원문의 필수 제출 수량이 아니다.

## 2026-09-24 최종 실행 결과

20:45 KST EC2 Instance Connect의 일회성 키로 ec2-user SSH 접속 성공, docker ps healthy 및 localhost HTTP 200 / example.com outbound HTTP 200 확인. 임시 CloudShell 소스 /32 규칙을 제거하고 원래 규칙을 확인했다.

사용자의 증거 수집·해제 요청에 따라 20:46 KST 스택을 삭제했다. DELETE_COMPLETE, EC2 terminated, 프로젝트 VPC/Subnet/RouteTable/SG/IGW 잔여 0 확인. 서울 EBS/EIP/Snapshot/NAT/ELB/RDS도 0이었다. 실습 키페어를 삭제했다. 상세 스크린샷 17장은 evidence/README.md 참고.

IAM 사용자 세션에서 배포·검증·정리를 완료했다. 기존 배포 IP는 이제 접속 대상으로 사용하지 않는다. 재실습할 때는 IAM 로그인·키 보관을 확인한 뒤 배포한다.
