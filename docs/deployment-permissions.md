# B6-1 배포 권한 경계 (2026-09-24)

## 적용 상태

로컬 정책 수정과 Access Analyzer·시뮬레이션은 완료했다. AWS 콘솔에서 기존 정책 버전 교체가 레거시 파서 오류로 실패해, CloudShell에서 새 고객 관리형 정책을 생성·검증한 뒤 사용자에 연결했다. 실제 Stack 생성은 루트 Console 세션에서 완료했다.

## 정책 구분

- infra/deployer-policy.json → B61DeployerPolicy: 본인 계정, 서울, 정확히 b6-1-learning 스택 관리와 필요한 조회·CloudShell·공개 AMI 파라미터 조회.
- infra/ec2-deployment-policy.json → B61Ec2DeploymentPolicy: CloudFormation 경유 EC2 작업만 허용. 별도 실행 역할을 지정하지 않는다. aws:CalledViaFirst는 실행 역할 방식에서 전달되지 않는다.
- IAMUserChangePassword: 본인 암호 변경. IAM 관리·PassRole·Access Key 생성 권한은 부여하지 않는다.

## 대상 제한

1. 기존 리소스 변경·삭제와 VPC/Subnet/보안 그룹 참조는 Project=b6-1 및 AWS가 붙인 aws:cloudformation:stack-name=b6-1-learning 두 태그를 모두 요구한다. AWS 예약 태그는 사용자가 임의로 붙일 수 없다.
2. 새 리소스는 생성 시 Project=b6-1을 요구한다. 생성 대상과 부모 VPC의 권한 문장을 분리해 다른 VPC에 리소스를 만들지 못하게 한다.
3. CreateTags는 ec2:CreateAction이 있는 생성 작업에만 허용한다. 기존 리소스의 태그 추가·변경·삭제는 허용하지 않는다. 태그 변경을 포함한 스택 업데이트도 거부될 수 있다.
4. RunInstances는 인스턴스, EBS, 새 ENI, AMI, Key Pair, 기존 네트워크별로 분리한다. t3.micro, IMDSv2, 기본 테넌시, 암호화 gp3 8GiB 이하를 요구한다. Key Pair는 b6-1-key만 사용한다.
5. LaunchTags 시작 템플릿은 새 EBS와 ENI에도 생성 시 Project 태그를 전달하기 위한 것이다. 기존 ENI/볼륨을 임의로 연결하는 권한은 부여하지 않는다.
6. Key Pair 생성·삭제는 초기 관리자 준비 단계에서 별도로 수행한다. 학습 사용자에게 모든 키의 생성·삭제 권한을 주지 않는다.

## 남는 범위와 제한

- Describe 계열 일부는 리소스별 제한을 지원하지 않아 서울 리전의 다른 리소스 정보도 조회될 수 있다. 조회가 변경 권한을 뜻하지 않는다.
- 새 리소스 ID는 생성 전 결정되지 않으므로 해당 종류 ARN의 *를 사용하되 생성 조건을 붙인다. 기존 리소스 변경까지 Resource=*로 허용하는 것과 다르다.
- 이 정책은 인스턴스 개수나 총비용의 상한을 보장하지 않는다. 템플릿 1대 구성, 검토, Budget을 함께 사용한다.
- 보안 그룹 세부 포트는 검토한 템플릿(80 공개, SSH 개인 IPv4 /32)에 의해 정한다. IAM 자체가 모든 포트 조합을 제한하는 것은 아니다.
- 다른 정책을 추가하면 권한이 합쳐질 수 있다. 이 두 정책과 암호 변경 정책 외 관리자 정책을 연결하지 않는다.
- AccessDenied 발생 시 AdministratorAccess나 무조건적인 Resource=*로 우회하지 않는다. 실패 작업·대상·지원 조건을 확인하고 필요한 부분만 고친다.

## 배포 전 검증

- IAM Access Analyzer ValidatePolicy에서 오류와 보안 경고를 확인한다.
- IAM 시뮬레이터에서 프로젝트 태그+스택 태그+CloudFormation 경유인 종료 작업은 허용, 다른 태그/태그 없음/직접 호출/서울 외 호출은 거부되는지 확인한다.
- 생성 시 다른 VPC 사용, 기존 리소스 재태깅, 큰 인스턴스, 암호화하지 않은 볼륨도 거부되어야 한다.
- 시뮬레이터는 실제 CloudFormation 서비스 호출을 대체하지 않는다. 실제 스택 생성·삭제 검증을 별도로 기록한다.

## 공식 근거

- https://docs.aws.amazon.com/service-authorization/latest/reference/list_ec2.html
- https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-calledvia
- https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-resource-tags.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-ec2-launchtemplate-tagspecification.html

## 실제 배포와 차이

- 실제 Stack 생성: `b6-1-learning` / Seoul `ap-northeast-2` / `CREATE_COMPLETE`.
- 실제 권한: `b6-1-learner`에는 `B61DeployerPolicyRestricted`, `B61Ec2DeploymentPolicy`, `IAMUserChangePassword`만 연결되어 있고 기존 `B61DeployerPolicy`는 분리했다.
- 검증: 두 JSON 정책의 Access Analyzer finding은 각각 `[]`; 조건을 포함한 시뮬레이션에서 서울 CloudFormation 생성·EC2 조회는 허용되고 S3 전체 조회·IAM Access Key 생성은 거부됐다.
- 현재 리소스는 `Project=b6-1` 태그와 CloudFormation 스택으로 식별할 수 있지만, IAM 정책이 현재 변경 작업을 제한한다고 주장하지 않는다.
