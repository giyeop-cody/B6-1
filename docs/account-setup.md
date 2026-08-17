# AWS 계정과 IAM 준비 가이드

> 현재 프로젝트는 AWS 계정이 없어 실제 배포 전 단계다. 아래 작업은 계정 소유자가 직접 수행한다. 비밀번호, Access Key, Secret Key, MFA 코드, `.pem`은 채팅이나 GitHub에 올리지 않는다.

## 1. 2026년 신규 계정의 무료 사용 방식 확인

2025년 7월 15일 이후 신규 AWS 고객은 가입할 때 Free Plan 또는 Paid Plan을 선택한다. Free Plan은 최대 6개월 또는 크레딧 소진 시점까지이며, 신규 고객은 가입 크레딧과 추가 활동 크레딧을 받을 수 있다. 정확한 금액·만료일·사용 가능 서비스는 가입 후 계정 화면에서 확인해야 한다.

- AWS Free Tier FAQ: https://aws.amazon.com/free/free-tier-faqs/
- AWS Free Tier 약관: https://aws.amazon.com/free/terms/
- EC2 Free Tier 추적: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-free-tier-usage.html

“무료일 것”이라고 추측해서 만들지 말고 EC2 생성 화면의 **Free tier eligible**, Credits, Billing을 확인한다.

## 2. 계정 생성

1. https://aws.amazon.com/free/ 에서 계정을 만든다.
2. 학습 기간과 제한을 확인하고 Free Plan 또는 자신에게 맞는 Plan을 선택한다.
3. 본인 이메일과 결제수단을 직접 등록한다.
4. 루트 계정에 MFA를 즉시 설정한다.
5. 가능하면 계정 별칭(Account alias)을 만든다.

## 3. 루트 계정은 초기 준비에만 사용

루트로 하는 작업은 다음으로 제한한다.

- 최초 IAM 사용자 생성
- 루트 MFA 설정
- IAM 사용자의 Billing 접근 허용이 필요할 때 계정 설정 변경

완료 후 루트에서 로그아웃하고 일상 실습은 별도 IAM 사용자로 진행한다.

## 4. 실습용 IAM 사용자와 정책

예시 사용자 이름:

```text
b6-1-learner
```

1. IAM → Users → Create user
2. AWS Management Console 접근을 설정
3. `infra/deployer-policy.json` 내용으로 고객 관리형 정책을 만든다.
4. 해당 정책을 `b6-1-learner`에 연결한다.
5. 사용자의 MFA도 설정한다.
6. IAM 사용자용 로그인 URL로 다시 로그인한다.

이 정책은 AdministratorAccess가 아니다. CloudFormation과 B6-1에 필요한 EC2 네트워크·인스턴스 작업만 허용하고 서울 리전 밖의 EC2 작업을 거부한다.

### 정책의 한계

VPC·Subnet·EC2를 새로 만드는 일부 EC2 작업은 생성 전에는 리소스 ARN이 없어서 `Resource: "*"`가 필요하다. 대신 허용 Action을 과제 작업으로 한정하고 서울 리전 조건을 적용했다. 실제 조직 환경에서는 Permission Boundary와 별도 CloudFormation 실행 Role을 추가하는 것이 더 안전하다.

## 5. 비용 알림

계정 화면에서 다음을 설정하거나 확인한다.

- Free Tier/크레딧 잔액과 만료일
- AWS Budgets의 작은 월 예산
- 실제 지출과 예상 지출 알림 이메일
- Billing Preferences의 Free Tier 사용 알림

예산 알림은 리소스를 자동으로 중지하지 않는다. 알림을 받으면 직접 리소스를 확인하고 삭제해야 한다.

## 6. 서울 리전 Key Pair

1. 콘솔 오른쪽 위 리전을 **Asia Pacific (Seoul), `ap-northeast-2`**로 변경한다.
2. EC2 → Key Pairs → Create key pair
3. 이름: `b6-1-key`
4. RSA, `.pem` 선택
5. 다운로드한 파일을 Git 저장소 밖의 안전한 위치에 보관한다.

macOS/Linux:

```bash
chmod 400 /안전한/경로/b6-1-key.pem
```

Key Pair private key는 재다운로드할 수 없다고 생각하고 관리한다.

## 7. 준비 완료 체크

- [ ] AWS 계정 생성
- [ ] Plan과 크레딧 만료일 확인
- [ ] 루트 MFA
- [ ] `b6-1-learner` IAM 사용자
- [ ] IAM 사용자 MFA
- [ ] AdministratorAccess가 없음을 확인
- [ ] `infra/deployer-policy.json` 정책 연결
- [ ] 예산·사용 알림
- [ ] 서울 리전 선택
- [ ] 서울 리전 `b6-1-key` 생성
- [ ] 비밀정보가 Git과 채팅에 없음을 확인
