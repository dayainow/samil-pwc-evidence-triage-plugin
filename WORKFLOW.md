# AX 해커톤 플러그인 제작 워크플로

## 1. 문제 선정
- 공개 자료로 확인 가능한 문제를 하나 고릅니다.
- 기업의 공식 자료, 고객 지원 페이지, 뉴스, 리뷰, 규제 자료 등에서 근거를 찾습니다.
- 문제를 "누가 / 무엇을 / 왜 불편한지" 형태로 정리합니다.

## 2. 플러그인 설계
- 문제를 해결하는 Codex 워크플로를 한 개의 스킬로 구현합니다.
- 필요하면 MCP 서버나 외부 스크립트를 추가할 수 있습니다.
- 제출 형식에 맞춰 src/ 아래에 배치합니다.

## 3. 로그 수집
- 대회 배포 파일인 `log-hooks.zip`을 작업 폴더 루트에 압축 해제한 상태에서 진행합니다.
- Codex CLI가 훅 신뢰 여부를 물으면 승인합니다.
- 새 Codex 세션에서 시작 문장부터 다시 진행합니다.
- 대화 로그는 훅이 `logs/codex/<session_id>.jsonl` 형태로 자동 저장합니다.
- 자동 저장된 원본 로그는 편집, 발췌, 삭제하지 않습니다.
- 비밀정보를 넣지 않습니다.

## 4. 최종 제출 전 체크리스트
- src/.codex-plugin/plugin.json 존재
- src/skills/.../SKILL.md 존재
- src/.mcp.json 존재
- src/scripts/evidence_triage.py 실행 가능
- examples/normal-case.json 실행 결과 확인
- examples/missing-case.json 실행 결과 확인
- examples/inconsistent-case.json 실행 결과 확인
- README.md에 문제와 플러그인 개요 작성
- README.md에 공개 근거 URL 작성
- README.md에 제출 질문 5문항 대응 내용 작성
- logs/에 원본 대화 로그 존재
- submission.zip 생성
- submission.zip에서 `.DS_Store`, `tmp/`, `log-hooks.zip`, 루트 `.codex/`, 루트 `.claude/`, `tools/` 제외

## 5. 이번 제출의 진행 방식

1. 사용자는 시작 문장으로 대화를 시작합니다.
2. 사용자는 보고서 넣는 문장을 입력하고 공개 보고서 내용을 붙여 넣습니다.
3. Codex는 보고서 분석 후 질문 시나리오 순서대로 답합니다.
4. 질문 흐름은 문제 정의, 사용자와 상황, 업무 흐름과 병목, 플러그인 기능 설계, 구현 범위와 안전성, 검증과 완성도 순서로 진행합니다.
5. 마지막 질문까지 답한 뒤에는 "로그 종료 지점"을 명확히 안내하고, 그 이후 대화는 제출 로그에 섞지 않습니다.
