# B6-1 외부 동료평가 요청서

> 실제 동료가 직접 확인하고 작성한다. 구현자가 임의로 통과 표시하지 않는다.

## 평가자가 받을 자료

- GitHub 저장소 URL
- 배포 URL과 `/health` URL
- `README.md`
- `docs/architecture.svg`
- `docs/deployment-guide.md`
- `docs/troubleshooting.md`
- `docs/cleanup-checklist.md`
- `evidence/` 실제 증거
- Git commit·branch·PR·issue 기록

## 기능 확인

- [ ] 배포 URL이 외부 네트워크에서 열린다.
- [ ] `/health`가 HTTP 200과 `OK`를 반환한다.
- [ ] EC2 내부에서 Docker 컨테이너가 healthy다.
- [ ] 새로 만든 인프라의 구조를 학습자가 설명할 수 있다.

## 네트워크와 보안

- [ ] VPC와 Public Subnet의 역할을 설명한다.
- [ ] `0.0.0.0/0 → IGW` Route를 찾고 설명한다.
- [ ] HTTP 80과 SSH 22의 허용 대상이 다르다.
- [ ] SSH가 `0.0.0.0/0`에 열려 있지 않다.
- [ ] 루트나 AdministratorAccess로 일상 실습하지 않는다.
- [ ] 비밀정보가 저장소에 없다.

## 증거와 문제 해결

- [ ] 아키텍처 그림과 실제 AWS 구성이 일치한다.
- [ ] 실제 문제 1건의 증상→가설→검증→조치→결과가 있다.
- [ ] 명령어 출력과 스크린샷이 실제 배포 시점의 것이다.
- [ ] 비용과 리소스 정리 결과가 있다.

## 학습 설명 질문

1. Public Subnet이 Public이 되려면 무엇이 필요한가?
2. Security Group과 IAM의 차이는 무엇인가?
3. 브라우저 요청이 Nginx까지 가는 순서는 무엇인가?
4. EC2를 Stop만 하면 왜 정리가 끝난 것이 아닌가?
5. CloudFormation을 선택한 장단점은 무엇인가?
6. Docker를 사용하지 않는 방법과 비교하면 무엇이 달라지는가?

## 동료 의견

```text
평가자:
평가일:
확인한 배포 URL:
잘한 점:
보완할 점:
재현 결과:
최종 의견:
```

현재 외부 동료평가 상태: **PENDING**
