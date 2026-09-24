# AWS 계정과 IAM 준비 가이드

> **최신 상태 (2026-09-25):** IAM 사용자 콘솔·CloudShell 사용 및 스택 삭제/리소스 정리 재확인을 완료했다. 아래 9월 24일 내용은 당시 기록이며, 현재 판정은 [최종 점검 결과](../evidence/final-audit-2026-09-25.md)를 기준으로 확인한다.

> **2026-09-24 권한 변경:** 기존의 서울 전체 EC2 변경 정책은 사용하지 않는다. [배포 권한 경계](deployment-permissions.md)를 먼저 확인하고, 두 정책을 검증·적용한 뒤 진행한다. AWS 적용·실제 배포 검증 전에는 완료로 표시하지 않는다.

> 2026-08-17에 계정 소유자가 기존 AWS 계정 사용 가능과 단기 배포 비용 가능성을 확인했다. Console 방식으로 보안 설정을 직접 수행한 뒤 배포한다. 비밀번호, Access Key, Secret Key, MFA 코드, `.pem`은 채팅이나 GitHub에 올리지 않는다.

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

### 실제 콘솔에서 MFA 등록 확인

2026-09-24 최초 확인 때는 루트 MFA 미등록, IAM 사용자 0명이었다. 이후 계정 소유자가 휴대폰 인증 앱으로 가상 MFA `my_phone` 등록을 완료했고, 보안 자격 증명 화면의 MFA 1개 및 등록 성공 알림을 확인했다. 로그인 완료와 MFA 등록 완료는 별도 단계다.

1. IAM → 대시보드 → **MFA 추가**를 선택한다. 새 탭에서 **MFA 디바이스 할당** 화면이 열릴 수 있다.
2. 계정 소유자가 디바이스 이름과 인증 방식을 선택하고 등록을 직접 완료한다.
3. IAM 대시보드를 새로 고쳐 루트 MFA 경고가 사라졌는지 확인한다.
4. IAM은 글로벌 서비스다. EC2·CloudFormation으로 이동할 때 서울 리전인지 별도로 확인한다. 이번 로그인 직후 콘솔은 시드니였다.

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
3. **직접 정책 연결 → 정책 생성**을 선택한다. 새 탭의 **Editor type → JSON**에서 기존 예시 전체를 선택해 `infra/deployer-policy.json` 내용으로 교체한다. **다음**에서 이름을 `B61DeployerPolicy`로 지정하고 생성한다.
   - 2026-09-24 현재 콘솔에서 정책 생성 성공 확인.
   - 원래 사용자 생성 탭으로 돌아와 **정책 새로 고침** 후 `B61DeployerPolicy`를 검색·선택한다.
   - 사용자 지정 암호와 최초 로그인 시 암호 변경을 선택하면 `IAMUserChangePassword`도 검토 화면에 자동 추가된다.
4. infra/ec2-deployment-policy.json으로 B61Ec2DeploymentPolicy도 생성하고 두 정책을 선택한다. AWS에 저장된 기존 B61DeployerPolicy는 수정본으로 교체해야 한다. 두 정책이 검증된 뒤 사용자를 생성한다.
5. 사용자의 MFA도 설정한다.
6. IAM 사용자용 로그인 URL로 다시 로그인한다.

이 정책은 AdministratorAccess가 아니다. CloudFormation과 B6-1에 필요한 EC2 네트워크·인스턴스 작업만 허용하고 서울 리전 밖의 EC2 작업을 거부한다. Console에서 템플릿을 읽고 public Amazon Linux 2023 AMI 값을 가져오는 권한, Access Key 없이 자동 검증을 실행할 CloudShell 최소 권한도 포함한다. CloudShell 파일 upload/download 권한은 포함하지 않는다.

### 정책의 한계

조회 권한과 생성 전 ID 와일드카드, 비용 상한 및 태그 업데이트 제한은 [배포 권한 경계](deployment-permissions.md)에 명시했다. 신규 생성 시에도 리소스 유형·요청 태그·CloudFormation 경유 조건을 적용한다.

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

- [x] 기존 AWS 계정 사용 가능 확인 (2026-08-17, 계정 소유자 응답)
- [ ] Plan과 크레딧 만료일 확인
- [x] 루트 MFA (2026-09-24, 가상 MFA `my_phone` 등록을 콘솔에서 확인)
- [x] `b6-1-learner` IAM 사용자 생성 및 콘솔 접근 설정 (2026-09-24)
- [ ] IAM 사용자 MFA
- [ ] AdministratorAccess가 없음을 확인
- [x] 제한 정책 2개 연결: `B61DeployerPolicyRestricted`, `B61Ec2DeploymentPolicy`; 기존 광범위 `B61DeployerPolicy` 분리 (2026-09-24)
- [ ] 예산·사용 알림
- [x] 서울 리전 선택 및 배포 확인 (`ap-northeast-2`)
- [x] 서울 리전 `b6-1-key` 생성 (private key 다운로드는 확인되지 않음)
- [ ] 비밀정보가 Git과 채팅에 없음을 확인

## 실제 실행 메모 (2026-09-24)

- 루트 가상 MFA `my_phone` 등록을 완료했다.
- `b6-1-learner` 사용자를 생성하고 콘솔 로그인용 임시 암호를 확인했다. 첫 로그인 시 암호 변경이 필요하다.
- `b6-1-key`는 서울 리전에 생성했지만 이 PC의 다운로드 폴더에서 `.pem` 파일을 확인하지 못했다. EC2 배포에는 영향이 없고, SSH가 필요하면 새 Key Pair를 만들어 안전한 위치에 즉시 보관해야 한다.
- 정책 편집 화면의 기존 버전 교체는 레거시 파서 오류가 있어, 새 고객 관리형 정책 2개를 CloudShell에서 생성·검증한 뒤 사용자에게 연결했다. 기존 광범위 `B61DeployerPolicy`는 분리했고 IAM 시뮬레이션에서 리전 조건을 포함한 배포·조회 권한과 S3/IAM 권한 거부를 확인했다.

## 실습 종료 상태 (2026-09-24 20:48 KST)

스택과 b6-1-key 키페어는 증거 수집 후 삭제했다. 루트 MFA와 b6-1-learner 및 정책은 유지했다. IAM 비밀번호를 사용자가 직접 설정·확인하지 못해 실습은 root 세션으로 실행됐으며, 과제의 IAM 사용자/Role 전용 실행 제약은 미충족이다. 다시 배포할 경우 사용자가 비밀번호를 직접 설정하고 IAM 로그인 및 키페어 보관을 먼저 확인한다.
