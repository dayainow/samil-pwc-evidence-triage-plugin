# Codex 플러그인 제출 템플릿

이 폴더는 “공개 자료로 검증 가능한 기업 문제”를 해결하는 Codex 플러그인을 만들기 위한 재사용 템플릿입니다.

한 기업을 선택하고, 공개 자료에서 실제 문제를 찾은 뒤, 그 문제를 좁은 업무 흐름으로 정의하고, Codex 플러그인으로 구현·검증·제출하는 전체 흐름을 담고 있습니다.

## 이 템플릿으로 할 수 있는 것

- Codex 플러그인 필수 구조를 바로 시작할 수 있습니다.
- `src/.codex-plugin/plugin.json` 기본 구조가 포함되어 있습니다.
- 공개 자료 기반 문제 분석용 `SKILL.md`가 들어 있습니다.
- 정상 케이스, 누락 케이스, 불일치 케이스 예시가 포함되어 있습니다.
- 간단한 실행 스크립트로 증빙 누락과 필드 불일치를 검증할 수 있습니다.
- 최종 제출 전 체크리스트를 따라 `submission.zip`을 준비할 수 있습니다.

## 폴더 구조

```text
codex-plugin-submission-template/
├── src/
│   ├── .codex-plugin/plugin.json
│   ├── .mcp.json
│   ├── skills/company-problem-review/SKILL.md
│   └── scripts/evidence_triage.py
├── examples/
│   ├── normal-case.json
│   ├── missing-case.json
│   └── inconsistent-case.json
├── references/
│   └── .gitkeep
├── logs/
│   └── .gitkeep
├── TEMPLATE_GUIDE.md
├── SUBMISSION_CHECKLIST.md
└── README.md
```

## 가장 쉬운 사용 방법

아래 흐름은 실제 제출물을 만들 때 사용한 방식입니다.

복잡하게 시작하지 말고, 먼저 공개 자료를 넣고 AI와 대화를 이어가면서 문제 정의 → 플러그인 설계 → 구현 → 검증 → `submission.zip` 생성까지 진행하면 됩니다.

### 1. 공개 자료 넣기

선택한 기업의 보고서, 공시, 공식 문서, 기사, 산업 자료를 `references/` 폴더에 넣습니다.

예시:

```text
references/
└── company_problem_report.pdf
```

주의할 점:

- 기업은 하나만 선택합니다.
- 공개 자료로 확인 가능한 문제만 사용합니다.
- 내부 자료, 비공개 정보, 출처 없는 숫자는 넣지 않습니다.

### 2. 시작 문장으로 대화 열기

새 Codex 세션에서 아래처럼 시작합니다.

```text
[기업명]을 선택했고, [문제 상황]을 Codex 플러그인으로 개선하려고 한다.
[업무 담당자]가 [업무 상황]에서 [자료 누락/불일치/반복 검토] 때문에 시간이 많이 걸리는 문제로 정리했다.
이제 이 문제를 실제 플러그인으로 구현하기 위해, 먼저 공개 자료 기준으로 문제 정의를 구체화하고, 어떤 사용자가 어떤 순간에 막히는지부터 좁혀보자.
```

### 3. 보고서 분석 요청하기

그다음 `references/`에 넣은 자료를 기준으로 분석을 요청합니다.

```text
보고서는 references 폴더에 넣어뒀어.
이 자료를 참고해서 플러그인 스펙으로 뺄 수 있게 분석해줘.
분석이 끝나면 거기서 멈춰줘.
이후 질문은 내가 순서대로 하나씩 직접 던질게.
```

### 4. 질문 시나리오로 문제 좁히기

아래 질문은 예시입니다. 선택한 기업과 문제에 맞게 표현을 바꿔서 하나씩 던지면 됩니다.

```text
[문제 정의]
1. 공개 자료에서 확인되는 핵심 문제는 무엇인가?
2. 이 문제를 실제 업무 실패 관점에서 한 문장으로 정의하면 어떻게 표현할 수 있을까?
3. 이 문제가 반복되면 시간, 비용, 품질, 리스크 측면에서 어떤 손실이 생기나?

[사용자와 상황]
4. 이 문제를 가장 직접적으로 겪는 1차 사용자는 누구인가?
5. 그 사용자는 어떤 업무 순간에 가장 자주 막히는가?
6. 사용자가 현재 반복해서 직접 확인하거나 처리하는 일은 무엇인가?

[업무 흐름과 병목]
7. 문제가 발생하는 업무 흐름을 단계별로 설명해줘.
8. 그 흐름에서 가장 시간이 많이 들거나 오류가 자주 나는 병목은 어디인가?
9. Codex 플러그인을 가장 먼저 적용하면 효과가 큰 단계는 어디인가?

[플러그인 설계]
10. 플러그인이 입력으로 받아야 할 자료는 무엇인가?
11. AI가 자동으로 탐지할 항목과 사람이 최종 판단할 항목을 나눠줘.
12. 출력은 체크리스트, 위험 플래그, 요약, 추가 질문 중 어떤 형태가 가장 적절한가?

[안전성과 검증]
13. 정보가 부족하거나 불명확할 때 플러그인은 어떻게 멈추거나 재질문해야 하나?
14. AI가 추측하거나 과도하게 판단하지 않도록 어떤 제한 규칙을 넣어야 하나?
15. 정상 케이스, 누락 케이스, 불일치 케이스에서 각각 어떤 출력이 나오면 성공인가?
```

### 5. 구현 요청하기

기획 답변이 충분히 쌓이면 아래 문장으로 실제 구현을 요청합니다.

```text
이제 앞에서 정의한 플러그인을 실제 제출물로 구현해줘.
현재 저장소 구조를 점검하고, plugin.json, SKILL.md, 실행 코드, 예시 케이스, README를 제출 요건에 맞게 보강해줘.
정상 케이스, 누락 케이스, 모순 케이스 검증을 실행하고 최종 submission.zip까지 만들어줘.
작업 중 수정한 파일과 검증 결과를 마지막에 정리해줘.
```

### 6. 마지막 확인하기

구현이 끝나면 아래 항목만 확인하면 됩니다.

```text
submission.zip
├── src/
│   ├── .codex-plugin/plugin.json
│   ├── skills/<skill-name>/SKILL.md
│   ├── .mcp.json
│   └── 실행 코드와 설정 파일
├── README.md
└── logs/
```

확인할 것:

- `src/.codex-plugin/plugin.json`이 있는가
- `SKILL.md` 또는 실행 코드가 있는가
- 정상/누락/모순 케이스를 실행했는가
- README에 문제, 사용자, 작동 방식, 검증 결과가 적혀 있는가
- logs 폴더에 원본 대화 로그가 들어 있는가
- 최종 파일명이 `submission.zip`인가

## 예시 실행

아래 명령으로 템플릿에 포함된 세 가지 케이스를 실행할 수 있습니다.

```bash
python3 src/scripts/evidence_triage.py examples/normal-case.json
python3 src/scripts/evidence_triage.py examples/missing-case.json
python3 src/scripts/evidence_triage.py examples/inconsistent-case.json
```

기대 결과는 다음과 같습니다.

- `normal-case.json`: `status: ok`
- `missing-case.json`: `status: missing_evidence`
- `inconsistent-case.json`: `status: needs_review`

JSON 파일 유효성은 아래처럼 확인합니다.

```bash
python3 -m json.tool src/.codex-plugin/plugin.json
python3 -m json.tool src/.mcp.json
```

Codex 플러그인 검증 도구를 사용할 수 있다면 아래 형식으로 추가 검증합니다.

```bash
python3 /path/to/plugin-creator/scripts/validate_plugin.py src
```

## 무엇을 바꿔야 하나요?

이 템플릿은 기본적으로 “증빙 패키지 검토” 예시를 담고 있습니다. 다른 기업이나 문제에 적용하려면 아래 항목을 바꾸면 됩니다.

- 선택한 기업명
- 공개 자료 출처
- 문제 정의
- 1차 사용자
- 사용자가 막히는 업무 순간
- 입력 자료
- 플러그인이 탐지할 누락·불일치 기준
- 출력 형식
- 검증 케이스

좋은 문제 정의 예시는 다음과 같습니다.

```text
[대상 사용자]가 [특정 업무]를 수행할 때, [업무 순간]에서 [자료 누락 또는 불일치] 때문에 막힌다. 이 플러그인은 [AI가 보조할 작업]을 수행하고, 최종 판단은 [사람의 역할]로 남긴다.
```

약한 문제 정의 예시는 다음과 같습니다.

```text
문서가 많아서 요약이 필요하다.
```

## 안전 원칙

- 공개 자료로 확인 가능한 문제만 다룹니다.
- 기업 내부 비공개 정보나 확인할 수 없는 경험담을 근거로 쓰지 않습니다.
- API 키, 비밀번호, 토큰 같은 비밀정보를 로그나 코드에 넣지 않습니다.
- AI가 최종 법률, 감사, 회계, 의료, 금융 판단을 내리게 하지 않습니다.
- 정보가 부족하면 추측하지 않고 `missing`, `unknown`, `blocked`, `needs_follow_up`으로 표시합니다.
- 데모 데이터는 익명화된 샘플을 사용합니다.

## 공개 GitHub에 올릴 때

공개 저장소에는 코드, 예시 케이스, 공개 출처, 포트폴리오용 README 중심으로 올리는 것이 좋습니다.

공개하지 않는 것이 좋은 항목:

- 원본 AI 대화 로그
- 대회 제출용 `submission.zip`
- 비공개 보고서
- API 키, 토큰, 비밀번호
- 개인 정보나 고객 정보
- 로컬 훅, 임시 파일, 숨김 설정 파일

## 최종 제출 전 확인

제출 전에는 [SUBMISSION_CHECKLIST.md](./SUBMISSION_CHECKLIST.md)를 기준으로 빠진 항목이 없는지 확인하세요.

템플릿을 실제 프로젝트로 바꾸는 자세한 순서는 [TEMPLATE_GUIDE.md](./TEMPLATE_GUIDE.md)에 정리되어 있습니다.
