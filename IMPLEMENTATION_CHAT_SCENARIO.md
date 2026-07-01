# Implementation Chat Scenario

이 파일은 제출 로그에 넣을 두 번째 대화 흐름을 준비하기 위한 대본이다.
이 파일 자체는 제출 로그 원본이 아니다. 실제 제출 로그에는 사용자가 아래 시작 문장부터 Codex와 주고받은 대화 원문만 저장한다.

## 목적

앞선 기획 대화에서 정의한 삼일PwC 내부통제 검토 보조 플러그인을 실제 Codex 플러그인 제출물로 완성한다.

최종 목표:

- OpenAI Codex 공식 문서 기준으로 플러그인 구조 확인
- `src/.codex-plugin/plugin.json` 점검 및 보강
- `src/skills/.../SKILL.md` 점검 및 보강
- 실행 코드 또는 검증 코드 점검 및 보강
- 정상/누락/모순 케이스 샘플 정리
- README 제출 문서 정리
- 제출 질문 5문항에 대한 README 답변 구조 반영
- 검증 명령 실행
- `submission.zip` 생성

## 로그 시작 문장

```text
이제 앞에서 정의한 삼일PwC 내부통제 검토 보조 플러그인을 실제 제출물로 구현해보자.

플러그인을 만들 때는 아래 OpenAI Codex 공식 문서를 기준으로 구조와 스킬 작성 방식을 확인해줘.

- 플러그인 개요: https://developers.openai.com/codex/plugins
- 플러그인 만들기: https://developers.openai.com/codex/plugins/build
- 스킬 작성법: https://developers.openai.com/codex/skills

목표는 Codex 플러그인 제출 요건에 맞춰 src/.codex-plugin/plugin.json, src/skills/.../SKILL.md, src/.mcp.json, 실행 코드, 예시 케이스, README, logs 구조를 점검하고 부족한 부분을 보완한 뒤, 정상/누락/모순 케이스 검증까지 수행해서 최종 submission.zip을 만드는 거야.

작업하면서 어떤 파일을 왜 수정하는지 짧게 설명해주고, 마지막에는 검증 결과와 submission.zip 위치를 정리해줘.
```

## 공식 문서 기준

구현 로그에서는 플러그인을 만들기 전에 아래 공식 문서를 먼저 확인하도록 한다.

- `https://developers.openai.com/codex/plugins`
- `https://developers.openai.com/codex/plugins/build`
- `https://developers.openai.com/codex/skills`

Codex가 확인할 기준:

- 플러그인은 `.codex-plugin/plugin.json` 매니페스트를 포함해야 한다.
- 가장 단순한 플러그인도 적어도 하나의 스킬 또는 실행 구성 요소를 포함해야 한다.
- 스킬은 `SKILL.md`를 중심으로 작성하고, `name`과 `description`을 명확히 둔다.
- 스킬 설명은 언제 호출되어야 하는지, 어떤 입력을 기대하는지, 어떤 출력을 만들어야 하는지 분명해야 한다.
- MCP 설정이 있다면 `src/.mcp.json`과 plugin manifest의 관계가 어긋나지 않아야 한다.

## Codex 응답 원칙

- OpenAI Codex 공식 문서를 기준으로 플러그인 구조를 확인한다.
- 기획 설명만 하지 말고 실제 파일을 점검하고 수정한다.
- 현재 저장소의 기존 구조를 존중한다.
- `src/`를 플러그인 루트로 유지한다.
- 제출 규정상 필요한 파일을 임의로 빼지 않는다.
- AI가 최종 감사 판단을 하지 않는다는 안전 규칙을 스킬과 README에 반영한다.
- 검증은 정상 케이스, 누락 케이스, 모순 케이스로 실행한다.
- `submission.zip`에는 제출 대상 파일만 포함한다.
- 로그 원본을 편집하거나 요약본으로 대체하지 않는다.

## 구현 단계

### 1. 공식 문서 기준 확인

Codex가 확인할 것:

- Codex 플러그인 개요
- 플러그인 만들기 문서의 기본 구조
- 스킬 작성법의 `SKILL.md` 요구사항
- 현재 제출 구조가 공식 문서와 대회 규정을 동시에 만족하는지

사용자가 보낼 수 있는 확인 문장:

```text
먼저 OpenAI Codex 공식 문서를 기준으로 플러그인 구조와 스킬 작성 기준을 확인해줘.
```

### 2. 저장소 상태 점검

Codex가 확인할 것:

- 전체 파일 구조
- `src/.codex-plugin/plugin.json` 존재 여부
- `src/skills/.../SKILL.md` 존재 여부
- `src/.mcp.json` 존재 여부
- 실행 코드 존재 여부
- 예시 케이스 존재 여부
- README 존재 여부
- logs 폴더 존재 여부

사용자가 보낼 수 있는 확인 문장:

```text
먼저 현재 저장소 구조가 제출 요건에 맞는지 확인해줘.
```

### 3. 플러그인 매니페스트 보강

Codex가 확인할 것:

- 플러그인 이름
- 버전
- 설명
- author
- skills 경로
- mcpServers 경로
- interface metadata
- defaultPrompt
- capabilities
- 불필요하거나 검증에 맞지 않는 필드

사용자가 보낼 수 있는 확인 문장:

```text
plugin.json이 Codex 플러그인 제출물로 충분한지 보고, 부족하면 보강해줘.
```

### 4. 스킬 파일 보강

Codex가 확인할 것:

- 사용 시점
- 입력 자료 범위
- 검토 워크플로
- 출력 형식
- 안전 규칙
- blocked / needs_follow_up 처리
- 최종 판단 금지 규칙

사용자가 보낼 수 있는 확인 문장:

```text
SKILL.md가 우리가 정의한 누락 증빙 탐지와 불일치 경고 플러그인 역할을 잘 설명하는지 보고 보강해줘.
```

### 5. 실행 코드 및 예시 케이스 보강

Codex가 확인할 것:

- 실행 코드가 실제로 동작하는지
- 입력 JSON 구조가 명확한지
- 정상 케이스
- 누락 케이스
- 모순 케이스
- 출력에 checklist, risk flags, follow-up questions가 있는지

사용자가 보낼 수 있는 확인 문장:

```text
정상 케이스, 누락 케이스, 모순 케이스를 실행 가능한 예시로 만들고, 스크립트가 그 결과를 제대로 출력하게 해줘.
```

### 6. README 정리

Codex가 확인할 것:

- 문제 정의
- 공개 근거
- 대상 사용자
- 플러그인 기능
- 제출 질문 5문항 대응
- 실행 방법
- 검증 방법
- 안전성
- 제출 구조

README에는 아래 질문에 대한 답이 자연스럽게 들어가야 한다.

- 무엇을, 누가, 어떤 상황에서 쓰나요?
- 왜 이 문제를 선택했나요?
- 플러그인은 어떻게 작동하나요?
- AI를 어떻게 활용했나요?
- 어떻게 검증했나요?

사용자가 보낼 수 있는 확인 문장:

```text
README를 심사위원이 바로 이해할 수 있게 문제, 해결 방식, 사용 시나리오, AI 활용 방식, 검증 방법 중심으로 정리하고 제출 질문 5문항에 대한 답이 드러나게 해줘.
```

### 7. 검증 실행

Codex가 실행할 것:

```bash
python3 src/scripts/evidence_triage.py examples/normal-case.json
python3 src/scripts/evidence_triage.py examples/missing-case.json
python3 src/scripts/evidence_triage.py examples/inconsistent-case.json
python3 -m json.tool src/.codex-plugin/plugin.json
python3 -m json.tool src/.mcp.json
```

가능하면 플러그인 검증 스크립트도 실행한다. 단, 환경에 `yaml` 등 의존성이 없어 실패하면 실패 사유를 명확히 기록한다.

사용자가 보낼 수 있는 확인 문장:

```text
이제 검증 명령을 실행해서 정상, 누락, 모순 케이스가 기대대로 나오는지 확인해줘.
```

### 8. submission.zip 생성

Codex가 포함할 것:

```text
submission.zip
├── src/
│   ├── .codex-plugin/plugin.json
│   ├── skills/<name>/SKILL.md
│   ├── .mcp.json
│   └── scripts/...
├── examples/
├── README.md
├── WORKFLOW.md
├── CONVERSATION_FLOW.md
└── logs/
```

주의:

- `tmp/`는 원칙적으로 제외한다.
- `.DS_Store`는 제외한다.
- `log-hooks.zip`은 제출 zip에 넣지 않는다.
- 루트의 `.codex/`, `.claude/`, `tools/`는 로그 수집용 설치 파일이므로 제출 zip에는 넣지 않는다.
- 기존 `submission.zip`이 있으면 새로 만들기 전에 이름 충돌을 확인한다.
- 로그는 사용자가 제출용으로 저장한 원본 로그만 포함해야 한다.

사용자가 보낼 수 있는 확인 문장:

```text
검증까지 끝났으면 제출 규정에 맞게 submission.zip을 만들어줘.
```

## 한 번에 실행할 때 쓰는 문장

실제 제출 로그를 짧고 자연스럽게 만들고 싶다면 아래 문장 하나로 시작해도 된다.

```text
이제 앞에서 정의한 삼일PwC 내부통제 검토 보조 플러그인을 실제 제출물로 구현해보자. OpenAI Codex 공식 문서인 플러그인 개요(https://developers.openai.com/codex/plugins), 플러그인 만들기(https://developers.openai.com/codex/plugins/build), 스킬 작성법(https://developers.openai.com/codex/skills)을 기준으로 현재 저장소 구조를 점검하고, plugin.json, SKILL.md, 실행 코드, 예시 케이스, README를 제출 요건에 맞게 보강해줘. README에는 제출 질문 5문항인 '무엇을, 누가, 어떤 상황에서 쓰나요?', '왜 이 문제를 선택했나요?', '플러그인은 어떻게 작동하나요?', 'AI를 어떻게 활용했나요?', '어떻게 검증했나요?'에 대한 답이 드러나게 정리해줘. 이후 정상/누락/모순 케이스 검증을 실행하고 최종 submission.zip까지 만들어줘. 작업 중 수정한 파일과 검증 결과를 마지막에 정리해줘.
```

## 권장 단계형 실행 시나리오

제출 로그의 설득력을 높이려면 한 번에 끝내기보다 아래 순서대로 사용자가 직접 질문을 나눠 입력한다.

### 1. 공식 문서와 제출 요건 확인

```text
이제 앞에서 정의한 삼일PwC 내부통제 검토 보조 플러그인을 실제 제출물로 구현해보자. 먼저 OpenAI Codex 공식 문서인 플러그인 개요(https://developers.openai.com/codex/plugins), 플러그인 만들기(https://developers.openai.com/codex/plugins/build), 스킬 작성법(https://developers.openai.com/codex/skills)을 기준으로 플러그인 구조와 제출 요건을 확인해줘. 대회 제출 규정의 submission.zip 구조와 질문 5문항도 같이 기준으로 잡아줘.
```

### 2. 저장소 구조 점검

```text
현재 저장소 구조를 점검해서 제출 요건에 맞는지 확인해줘. 특히 src/.codex-plugin/plugin.json, src/skills/.../SKILL.md, src/.mcp.json, 실행 코드, 예시 케이스, README, logs 폴더가 제대로 준비되어 있는지 봐줘.
```

### 3. 플러그인 매니페스트 보강

```text
plugin.json이 Codex 플러그인 제출물로 충분한지 확인하고, 부족한 필드가 있으면 보강해줘. 플러그인 이름, 설명, skills 경로, mcpServers 경로, interface 정보, defaultPrompt, capabilities가 우리가 정의한 내부통제 증빙 검토 플러그인과 맞아야 해.
```

### 4. 스킬 파일 보강

```text
SKILL.md가 우리가 정의한 역할을 잘 수행하도록 보강해줘. 단순 요약이 아니라 누락 증빙 탐지, 불일치 경고, 체크리스트 생성, 추가 확인 질문 생성이 중심이어야 하고, AI가 최종 감사 판단을 하지 않는다는 안전 규칙도 명확히 넣어줘.
```

### 5. 실행 코드와 예시 케이스 정리

```text
실행 코드와 예시 케이스를 점검해줘. 정상 케이스, 누락 케이스, 모순 케이스가 각각 실행 가능해야 하고, 출력에는 checklist, risk_flags, follow_up_questions, review_note가 드러나야 해. 부족하면 코드나 예시 JSON을 보강해줘.
```

### 6. README와 제출 질문 5문항 정리

```text
README를 심사위원이 바로 이해할 수 있게 정리해줘. 문제 정의, 공개 근거, 대상 사용자, 플러그인 작동 방식, AI 활용 방식, 검증 방법이 들어가야 하고, 제출 질문 5문항인 '무엇을, 누가, 어떤 상황에서 쓰나요?', '왜 이 문제를 선택했나요?', '플러그인은 어떻게 작동하나요?', 'AI를 어떻게 활용했나요?', '어떻게 검증했나요?'에 대한 답이 자연스럽게 드러나게 해줘.
```

### 7. 테스트와 검증 실행

```text
이제 검증 명령을 실행해서 정상 케이스, 누락 케이스, 모순 케이스가 기대대로 나오는지 확인해줘. plugin.json과 .mcp.json의 JSON 유효성도 같이 확인하고, 가능하면 Codex 플러그인 검증 스크립트도 실행해줘. 실패하는 검증이 있으면 원인과 조치 여부를 정리해줘.
```

### 8. submission.zip 생성

```text
검증까지 끝났으면 제출 규정에 맞게 submission.zip을 만들어줘. zip 안에는 src/, README.md, logs/가 반드시 들어가야 하고, examples/와 보조 문서는 필요하면 포함해줘. 다만 .DS_Store, tmp/, log-hooks.zip, 루트 .codex/, 루트 .claude/, tools/는 제외해줘. 생성 후 zip 구조와 검증 결과를 마지막에 정리해줘.
```

### 9. 종료 확인

```text
여기까지가 구현 및 제출 패키징 로그에 포함할 대화 흐름의 종료 지점이야. 최종 산출물 위치와 남은 주의사항만 짧게 정리해줘.
```

## 로그 종료 문장

Codex가 `submission.zip` 생성과 검증 결과 정리를 마치면 아래 문장으로 종료한다.

```text
여기까지가 구현 및 제출 패키징 로그에 포함할 대화 흐름의 종료 지점입니다. 이후 수정이나 재패키징은 별도 로그로 분리하는 것이 안전합니다.
```
