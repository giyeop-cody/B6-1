# ADR-002: 비밀 키 없이 Console과 CloudShell로 배포한다

- 상태: 결정
- 날짜: 2026-08-17
- 관련 Issue: [#5](https://github.com/giyeop-cody/B6-1/issues/5)

## 문제

AWS 계정은 사용할 수 있지만 비밀번호, Access Key, Secret Key, MFA 코드, Key Pair private key를 채팅이나 저장소에 넣으면 안 된다. 동시에 실제 CloudFormation 배포와 자동 AWS 검증은 수행해야 한다.

## 비교한 선택지

| 선택지 | 장점 | 단점 | 결과 |
|---|---|---|---|
| 장기 Access Key + 로컬 AWS CLI | 자동화가 쉬움 | 키 전달·저장·폐기 위험이 큼 | 사용 안 함 |
| IAM Identity Center Device Login | 단기 자격 증명과 CLI 자동화에 좋음 | 현재 계정에 Identity Center 준비 여부가 확인되지 않음 | 이번에는 보류 |
| AWS Console + CloudShell | 비밀 키 공유 없이 Console 생성과 CLI 검증 가능 | 계정 소유자가 화면 작업을 직접 해야 하며 CloudShell 권한이 추가됨 | 채택 |
| 루트 계정으로 전체 배포 | 준비가 빠름 | 권한이 너무 크고 일상 사용 보안 원칙에 어긋남 | 사용 안 함 |

## 결정

1. 루트는 MFA, IAM 사용자, Billing 준비에만 사용한다.
2. 실제 Stack은 `b6-1-learner` IAM 사용자로 만든다.
3. Console에서 `infra/cloudformation.yml`을 업로드한다.
4. 자동 AWS 검사는 같은 Console 세션의 CloudShell에서 실행한다.
5. CloudShell에는 세션 생성·시작·자격 증명 전달 Action만 허용한다.
6. 파일 upload/download Action은 허용하지 않는다. 공개 GitHub 저장소를 clone해 검사하므로 필요하지 않다.
7. SSM 권한은 Amazon Linux 2023 public AMI parameter 하나의 읽기로 제한한다.

## 트레이드오프

- 장점: 장기 Access Key를 만들거나 전달하지 않고 실제 API 검사를 수행할 수 있다.
- 단점: Console과 CloudShell 두 화면을 오가야 하고 IAM 정책이 조금 길어진다.
- 보안 균형: `Resource: "*"`가 필요한 Console 목록·CloudShell 생성 Action이 있지만 허용 Action과 서울 리전 조건을 제한한다.
- 운영 한계: 조직 계정이라면 IAM Identity Center와 별도 CloudFormation 실행 Role이 더 적합할 수 있다.
