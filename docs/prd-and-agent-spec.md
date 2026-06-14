# PRD and Agent SPEC

## Product Goal

머신러닝 지식을 Markdown Wiki로 관리하고, MCP Tool과 Wiki Agent를 통해 사용자가 page를 검색, 조회, 질문할 수 있는 MVP를 구현한다.

이 프로젝트는 단순 문서 저장소가 아니라, raw source를 받아 Wiki page 후보로 정리하고, GUI와 Agent를 통해 지식 탐색을 돕는 도구를 목표로 한다.

## Users

- 머신러닝 강의자료를 정리하는 학습자
- 논문이나 강의 내용을 빠르게 찾아보고 비교하려는 사용자
- 변화가 빠른 ML 개념을 page 단위로 유지보수하려는 개발자

## Core Requirements

1. 사용자는 Wiki page 목록을 조회할 수 있어야 한다.
2. 사용자는 title, tag, body를 대상으로 Wiki page를 검색할 수 있어야 한다.
3. 사용자는 선택한 page 본문을 GUI에서 읽을 수 있어야 한다.
4. 사용자는 Wiki Agent에게 질문하고 관련 page 근거가 포함된 답변을 받을 수 있어야 한다.
5. GUI는 MCP Tool을 통해 Wiki 데이터를 가져와야 한다.
6. 채팅은 외부 API를 직접 호출하지 않고 subprocess 기반 CLI agent bridge로 동작해야 한다.
7. raw source는 `raw/inbox`에서 ingest되어 추출 텍스트와 merge request로 변환되어야 한다.
8. shell watcher는 메시지 파일을 감지해 agent를 실행하고 응답 파일을 저장해야 한다.

## Non-Goals

- 최신 논문을 자동으로 크롤링하는 기능
- 외부 LLM API와 직접 연동하는 기능
- 사용자 계정, 인증, 배포 서버 구축
- Agent가 사람 검토 없이 Wiki page를 자동 수정하는 기능

## Functional SPEC

### Wiki Page

각 page는 `wiki/ml` 아래의 Markdown 파일이다. 모든 page는 front matter로 `title`, `slug`, `tags`, `updated`를 가진다.

예시:

```yaml
---
title: K-Nearest Neighbors
slug: supervised-knn
tags: [supervised-learning, knn]
updated: 2026-06-14
---
```

### MCP Server

서버 파일: `mcp/wiki_mcp_server.py`

stdin/stdout 기반 JSON-RPC 인터페이스를 제공하며, MCP의 `tools/list`와 `tools/call` 흐름에 맞춰 Tool 목록 조회와 Tool 호출을 처리한다.

Tools:

- `list_pages(args={})`
  - 모든 Wiki page의 title, slug, tags, updated, path를 반환한다.
- `search_pages(args={"query": "..."})`
  - title, slug, tags, body를 대상으로 검색하고 관련 page 목록을 score와 함께 반환한다.
- `get_page(args={"slug": "..."})`
  - slug에 해당하는 page의 metadata와 body를 반환한다.
- `ask_wiki(args={"question": "..."})`
  - 질문과 관련된 page를 검색하고 answer와 source snippet을 반환한다.

지원 method:

- `tools/list`
  - 사용 가능한 Tool 이름 목록을 반환한다.
- `tools/call`
  - `params.name`으로 지정한 Tool을 `params.arguments`와 함께 실행한다.

예시 요청:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_page",
    "arguments": {
      "slug": "mlp"
    }
  }
}
```

### GUI

파일:

- `static/index.html`
- `static/app.js`
- `static/styles.css`

화면 구성:

- Sidebar: 검색 입력, page 목록
- Article: 선택된 Markdown page 본문
- Chat: 질문 입력, Agent 답변, source 표시

### HTTP Server

파일: `scripts/server.py`

역할:

- 정적 GUI 파일 서빙
- `/api/pages`로 page 목록 반환
- `/api/page/<slug>`로 page 본문 반환
- `/api/search`로 Wiki 검색 수행
- `/api/chat`으로 Wiki Agent 실행
- 내부적으로 MCP 서버를 subprocess로 호출

### CLI Agent Bridge

파일: `scripts/wiki_agent.py`

역할:

- 질문을 입력받는다.
- MCP Wiki Tool로 관련 page를 검색한다.
- 검색 결과를 prompt context로 구성한다.
- `WIKI_AGENT_CLI`가 설정되어 있으면 Codex CLI를 호출한다.
- CLI 호출이 실패하거나 설정이 없으면 MCP 검색 기반 fallback answer를 반환한다.

권한:

- 기본 동작은 read/search/answer이다.
- Wiki 파일을 직접 수정하지 않는다.

### Message Watcher

파일: `scripts/agent_watch.ps1`

역할:

- `agent_messages/inbox`의 `.txt` 또는 `.json` 메시지를 감지한다.
- `scripts/wiki_agent.py`를 실행한다.
- 응답을 `agent_messages/outbox/*.response.json`에 저장한다.
- 처리한 메시지를 `agent_messages/processed`로 이동한다.

### Raw Source Ingest

파일: `scripts/ingest_raw.py`

역할:

- `raw/inbox`의 `.pdf`, `.txt`, `.md` 파일을 읽는다.
- PDF는 `pypdf`로 텍스트를 추출해 `raw/extracted`에 저장한다.
- 관련 Wiki page 후보를 검색한다.
- `wiki/merge-queue`에 merge request Markdown을 생성한다.
- 처리한 raw source를 `raw/processed`에 복사한다.

## Agent SPEC

### Wiki Curator Agent

- Role: 새로운 source가 들어왔을 때 기존 page와의 연결 후보를 찾는다.
- Permission: read/search only
- Allowed functions: `list_pages`, `search_pages`, `get_page`
- Output: 관련 page, 병합 후보, 새 page 생성 필요 여부

### Wiki Reviewer Agent

- Role: source 설명, 출처 누락, 정의 충돌 가능성을 검토한다.
- Permission: read/search only
- Allowed functions: `search_pages`, `get_page`
- Output: review note, 수정 제안, human review 필요 여부

### Wiki Chat Agent

- Role: 사용자 질문을 Wiki page 근거와 연결하고 답변한다.
- Permission: read/search/answer only
- Allowed functions: `search_pages`, `get_page`, `ask_wiki`
- Output: 답변, 관련 page slug, 근거 snippet
- Model: 사용자의 Codex CLI profile 또는 `WIKI_AGENT_CLI` 설정을 따른다.

## Acceptance Criteria

- `python scripts\server.py`로 GUI가 실행된다.
- 브라우저에서 page 목록과 검색 결과가 표시된다.
- 선택한 page 본문이 중앙 article view에 표시된다.
- 오른쪽 chat panel에서 질문하면 agent 답변과 source가 표시된다.
- `mcp/wiki_mcp_server.py`의 Tool이 JSON-RPC 요청에 응답한다.
- `scripts/ingest_raw.py`가 raw source를 merge request로 변환한다.
- `scripts/agent_watch.ps1`가 inbox 메시지를 처리하고 outbox 응답을 생성한다.
- README에 MCP Tool, Agent 동작 방식, 실행 방법이 설명되어 있다.
- MVP GUI screenshot이 `screenshots/mvp-gui.png`에 포함되어 있다.

## Evaluation Criteria Mapping

### Wiki Pages의 구현과 Serving

- 구현 위치: `wiki/ml/*.md`
- Serving 위치: `scripts/server.py`, `static/index.html`, `static/app.js`, `static/styles.css`
- GUI는 MCP Tool을 통해 page 목록, 검색 결과, page 본문을 가져온다.

### 무엇을, 왜, 어떻게 만들 것인가

- 무엇을: Machine Learning Wiki, MCP Tool, Wiki Agent, raw source ingest workflow
- 왜: 머신러닝 지식은 source가 계속 추가되므로 검색, 병합, 추적 가능한 Wiki 구조가 필요하다.
- 어떻게: Markdown page와 `tools/list`, `tools/call`을 처리하는 MCP Tool 서버를 만들고, GUI와 Agent가 MCP 서버를 공통 인터페이스로 사용하게 했다.

### Wiki Pages 시각화 방식

- Sidebar: page explorer와 검색
- Article view: Markdown page 본문
- Chat panel: Wiki Agent 질문 응답과 source 표시
- MVP 이미지: `screenshots/mvp-gui.png`

### 도구 활용에 필요한 기능

- `list_pages`: page 목록 조회
- `search_pages`: Wiki 검색
- `get_page`: page 본문 조회
- `ask_wiki`: 질문 기반 관련 page와 답변 반환
- `ingest_raw.py`: raw source를 merge request로 변환
- `agent_watch.ps1`: 파일 기반 비동기 Agent 실행

### Tools and Agent

- MCP 서버: `mcp/wiki_mcp_server.py`
- HTTP GUI 서버: `scripts/server.py`
- Chat Agent: `scripts/wiki_agent.py`
- Watcher Agent 실행기: `scripts/agent_watch.ps1`
- Raw source 처리: `scripts/ingest_raw.py`

### Tool과 AI Agent 사이를 연결해 줄 MCP 서버

`scripts/wiki_agent.py`는 질문을 받으면 MCP Tool로 관련 Wiki page를 검색하고, 검색 결과를 context로 사용해 답변을 만든다. 따라서 MCP 서버는 Tool과 AI Agent 사이의 연결 계층이다.

### Tool이 필요한 이유

GUI와 Agent가 Wiki 파일을 각자 다른 방식으로 읽으면 결과가 달라질 수 있다. MCP Tool은 page 목록, 검색, 조회, 질문 응답을 하나의 인터페이스로 통일해 Wiki 지식을 일관되게 사용할 수 있게 한다.

### LLM Wiki 편집 혹은 챗봇 기능 Agent

MVP에는 Wiki Chat Agent가 포함되어 있다. 자동 편집 Agent는 안전을 위해 직접 파일 수정 권한을 갖지 않고, raw source를 merge request로 바꾼 뒤 사람이 검토해 병합하는 방식으로 설계했다.

### Agent 역할, 권한, 허용 기능

- Wiki Curator Agent: 새 source와 기존 page의 연결 후보를 찾는다. 권한은 read/search only.
- Wiki Reviewer Agent: source 설명, 출처 누락, 정의 충돌 가능성을 검토한다. 권한은 read/search only.
- Wiki Chat Agent: 사용자 질문에 대해 Wiki 근거 기반 답변을 제공한다. 권한은 read/search/answer only.
- 모든 Agent는 사람 검토 없이 Wiki 파일을 자동 수정하지 않는다.
