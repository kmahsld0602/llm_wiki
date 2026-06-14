# Agent Decision Journal

이 문서는 Wiki Tool 구현을 위해 Agent와 의사결정을 거친 과정을 정리한 기록이다.

## Round 1: Wiki 도메인 결정

초기 선택지는 특정 수업 도메인을 그대로 사용하는 방식과, 강의 주제와 연결되지만 독립적인 지식 도메인을 선택하는 방식이었다.

결정:

- 도메인은 Machine Learning으로 정한다.
- 이유는 머신러닝이 개념 변화가 빠르고, 새 source가 들어올 때 기존 지식과의 병합 판단이 중요하기 때문이다.
- Wiki의 목표는 단순 개념 요약이 아니라 page 단위의 지식 관리, 검색, 질문 응답, source 추적이다.

## Round 2: Wiki 저장 방식 결정

Wiki page를 데이터베이스에 저장할지 Markdown 파일로 저장할지 결정해야 했다.

결정:

- Wiki page는 `wiki/ml/*.md` Markdown 파일로 저장한다.
- 각 page는 front matter에 `title`, `slug`, `tags`, `updated`를 가진다.
- Markdown을 사용하면 사람이 직접 검토하고 수정하기 쉽고, raw source 병합 결과를 git diff로 확인하기 쉽다.

## Round 3: MCP Tool 구조 결정

GUI가 Markdown 파일을 직접 읽게 만들 수도 있었지만, 과제 요구사항에 맞게 Tool과 Agent 사이를 연결할 MCP 서버가 필요했다.

결정:

- `mcp/wiki_mcp_server.py`를 MCP Tool 서버로 구현한다.
- 서버는 stdin/stdout으로 JSON-RPC 요청을 받고 JSON 응답을 반환한다.
- 서버는 `tools/list`로 Tool 목록을 반환하고, `tools/call`로 개별 Tool을 실행한다.
- 제공 Tool은 `list_pages`, `search_pages`, `get_page`, `ask_wiki`로 정한다.
- GUI 서버는 Wiki 파일을 직접 읽지 않고 MCP Tool을 subprocess로 호출한다.

## Round 4: GUI 구성 결정

평가 기준에는 Wiki Pages를 어떤 방식으로 시각화할 것인지가 포함되어 있다.

결정:

- 화면은 3열 구조로 만든다.
- 왼쪽은 page explorer와 검색 영역으로 둔다.
- 중앙은 선택한 Markdown article view로 둔다.
- 오른쪽은 Wiki Agent chat 영역으로 둔다.
- 사용자는 직접 page를 탐색하거나, 질문을 통해 관련 page를 찾을 수 있다.

## Round 5: Agent 연결 방식 결정

외부 LLM API를 직접 호출하는 방식은 과제 범위와 운영 안정성 측면에서 부담이 있었다. 또한 사용자가 subprocess, loop, shell script 기반의 agent 실행을 요구했다.

결정:

- `scripts/wiki_agent.py`가 질문을 받아 MCP 검색 결과를 context로 구성한다.
- `WIKI_AGENT_CLI` 환경변수가 있으면 Codex CLI를 호출한다.
- Codex CLI가 없거나 실패하면 MCP 검색 기반 fallback answer를 반환한다.
- Agent는 기본적으로 read/search/answer 권한만 가진다.

## Round 6: 비동기 메시지 처리 결정

GUI 외부에서도 Agent를 실행할 수 있는 구조가 필요했다.

결정:

- `scripts/agent_watch.ps1`를 만든다.
- `agent_messages/inbox`에 질문 파일이 들어오면 watcher가 감지한다.
- watcher는 `scripts/wiki_agent.py`를 실행하고, 결과를 `agent_messages/outbox`에 JSON으로 저장한다.
- 처리된 메시지는 `agent_messages/processed`로 이동한다.

## Round 7: Raw Source 병합 방식 결정

raw PDF나 text source를 Wiki에 자동 반영할 수 있지만, Agent가 source를 잘못 해석해 기존 page를 손상시킬 위험이 있다.

결정:

- raw source는 `raw/inbox`에 넣는다.
- `scripts/ingest_raw.py`가 PDF 텍스트를 추출하고 merge request를 생성한다.
- 실제 Wiki page 병합은 사람이 검토한 뒤 수행한다.
- 각 Wiki page에는 `Sources` 섹션을 두어 원본 PDF와 추출 텍스트 경로를 남긴다.

## Round 8: Raw Source 반영 결과

`raw/inbox`의 머신러닝 강의자료를 Wiki에 반영했다.

생성 또는 갱신한 page:

- `wiki/ml/supervised-knn.md`
- `wiki/ml/regularization.md`
- `wiki/ml/unsupervised-clustering.md`
- `wiki/ml/dimensionality-reduction-pca.md`
- `wiki/ml/mlp.md`
- `wiki/ml/ensemble-learning.md`
- `wiki/ml/index.md`

추가 수정:

- `scripts/ingest_raw.py`가 PDF 표지의 공통 문구를 제목으로 잡아 merge request를 덮어쓰는 문제를 수정했다.
- 이제 merge request 파일명은 raw source 파일명 기반으로 생성된다.

## Round 9: 권한 제한 결정

Agent가 자동으로 Wiki 파일을 수정하면 평가와 검증이 어려워질 수 있다.

결정:

- Chat Agent는 읽기, 검색, 답변 생성까지만 수행한다.
- Curator와 Reviewer 역할도 read/search only 권한으로 정의한다.
- 실제 파일 수정과 최종 병합은 사람이 검토한 뒤 수행한다.

## 최종 설계 요약

- Wiki 저장소: Markdown files under `wiki/ml`
- MCP 서버: `mcp/wiki_mcp_server.py`
- GUI 서버: `scripts/server.py`
- Chat Agent: `scripts/wiki_agent.py`
- Watcher: `scripts/agent_watch.ps1`
- Raw ingest: `scripts/ingest_raw.py`
- MVP 이미지: `screenshots/mvp-gui.png`

## 제출 기준 반영 요약

- Wiki Pages 구현과 Serving은 Round 2, Round 3, Round 4의 결정으로 반영했다.
- 무엇을, 왜, 어떻게 만들 것인지는 Round 1, Round 2, Round 7의 결정으로 반영했다.
- Wiki Pages 시각화 방식은 Round 4에서 3열 GUI로 결정했다.
- 도구 활용에 필요한 기능은 Round 3, Round 5, Round 6, Round 7에서 결정했다.
- Tool과 AI Agent 사이의 MCP 서버는 Round 3과 Round 5에서 결정했다.
- LLM Wiki 챗봇 기능 Agent는 Round 5에서 결정했다.
- Agent 역할, 권한, 허용 기능은 Round 9에서 read/search/answer 중심으로 제한했다.
