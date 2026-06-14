# Local LLM Wiki Workbench

Local LLM Wiki Workbench is an executable source-code package that combines an agent harness, a Markdown-based LLM Wiki, an MCP Tool server, and a browser viewer.

A first-time user can clone this repository, add one source file, generate a merge request, create or update a Wiki page, and verify the result in the viewer within 30 minutes.

## What This Product Provides

- Harness: `RULES.md`, `harness/CONTEXT.md`, and `skills/wiki-curator/SKILL.md`
- LLM Wiki: `raw/`, `wiki/`, and `schema/`
- Visualization tools: `tools/mcp_server.py` and `tools/viewer.py`
- Browser viewer: `static/index.html`, `static/app.js`, `static/styles.css`
- Agent bridge: `scripts/wiki_agent.py` and `scripts/agent_watch.ps1`
- Demo proof: `demo/wiki-viewer-demo.png`

## Repository Layout

```text
local-llm-wiki-workbench/
  RULES.md
  README.md
  requirements.txt
  harness/
    CONTEXT.md
  skills/
    wiki-curator/
      SKILL.md
  raw/
    inbox/
    extracted/
    processed/
  wiki/
    ml/
    merge-queue/
  schema/
    wiki-page.schema.json
    raw-source.schema.json
  tools/
    mcp_server.py
    viewer.py
  scripts/
    ingest_raw.py
    wiki_agent.py
    agent_watch.ps1
    server.py
  static/
    index.html
    app.js
    styles.css
  demo/
    wiki-viewer-demo.png
```

## Install

Requirements:

- Python 3.10 or newer
- PowerShell or a compatible shell
- `pypdf` for PDF ingestion

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

If you only use `.md` or `.txt` raw sources, `pypdf` is not required at runtime. It is included because PDF ingestion is part of the default workflow.

## Start the Viewer

```powershell
python tools\viewer.py
```

Open:

```text
http://127.0.0.1:8765
```

The viewer shows:

- Left sidebar: Wiki page search and page list
- Center article view: selected Markdown Wiki page
- Right chat panel: Wiki Agent answer and source list

## MCP Tool Server

Run the MCP Tool server entrypoint:

```powershell
python tools\mcp_server.py
```

The server reads one JSON-RPC request from stdin and returns one JSON-RPC response on stdout. It supports the MCP tool flow:

- `tools/list`: list available tools
- `tools/call`: call one tool with arguments

Available tools:

- `list_pages(args={})`: returns Wiki page metadata.
- `search_pages(args={"query": "..."})`: searches title, slug, tags, and body.
- `get_page(args={"slug": "..."})`: returns one Markdown page.
- `ask_wiki(args={"question": "..."})`: returns a Wiki-grounded answer and sources.

Example:

```powershell
python -c "import json, subprocess, sys; req={'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':'search_pages','arguments':{'query':'KNN'}}}; p=subprocess.run([sys.executable,'tools/mcp_server.py'],input=json.dumps(req),text=True,capture_output=True,encoding='utf-8'); print(p.stdout)"
```

## Create Your First Wiki Page in 30 Minutes

### 1. Add one source file

Put a `.pdf`, `.md`, or `.txt` file in `raw/inbox`.

```powershell
Copy-Item "C:\path\to\your-source.pdf" raw\inbox\
```

For a quick text-only test:

```powershell
@"
# My First Topic

This source explains a concept I want to add to my local Wiki.
"@ | Set-Content raw\inbox\my-first-topic.md -Encoding UTF8
```

### 2. Generate a merge request

```powershell
python scripts\ingest_raw.py --file my-first-topic.md
```

The script creates:

```text
wiki/merge-queue/my-first-topic-merge-request.md
```

For PDFs, extracted text is also written to:

```text
raw/extracted/<source-name>.txt
```

### 3. Integrate the source into the Wiki

Open the generated merge request and decide whether to update an existing page or create a new one.

Minimal new page example:

```markdown
---
title: My First Topic
slug: my-first-topic
tags: [example]
updated: 2026-06-14
---

# My First Topic

This page summarizes the first source added to the local Wiki.

## Sources

- `raw/inbox/my-first-topic.md`
```

Save it as:

```text
wiki/ml/my-first-topic.md
```

### 4. Verify in the viewer

Start the viewer:

```powershell
python tools\viewer.py
```

Open `http://127.0.0.1:8765`, search for `My First Topic`, and confirm the page appears.

### 5. Verify through the MCP Tool server

```powershell
python -c "import json, subprocess, sys; req={'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':'get_page','arguments':{'slug':'my-first-topic'}}}; p=subprocess.run([sys.executable,'tools/mcp_server.py'],input=json.dumps(req),text=True,capture_output=True,encoding='utf-8'); print(p.stdout)"
```

## Raw Source Integration Policy

Raw source files are local user materials. The repository keeps the folder structure, but `.gitignore` excludes files under:

- `raw/inbox/`
- `raw/extracted/`
- `raw/processed/`
- generated `wiki/merge-queue/*.md`

This prevents private source excerpts from being accidentally published. If you intentionally want to publish example sources, add sanitized sample files.

## Agent Harness

The harness is included for agents that maintain or extend the Wiki.

- `RULES.md`: operating rules and safety policy
- `harness/CONTEXT.md`: product context and workflow
- `skills/wiki-curator/SKILL.md`: skill instructions for source-to-Wiki integration

Agent permission model:

- Curator: read/search existing Wiki pages and propose merge targets.
- Reviewer: read/search and flag missing sources or conflicts.
- Chat Agent: read/search/answer only.
- No agent automatically rewrites Wiki pages without explicit user instruction.

## Agent and Watcher

Chat Agent:

```powershell
python scripts\wiki_agent.py "What is KNN?"
```

By default, the agent uses the fast MCP fallback path. This keeps the command responsive even when a local CLI model is installed.

Fallback verification:

```powershell
$env:WIKI_AGENT_DISABLE_CLI='1'
python scripts\wiki_agent.py "What is KNN?"
Remove-Item Env:\WIKI_AGENT_DISABLE_CLI
```

Optional CLI-backed answer generation:

```powershell
$env:WIKI_AGENT_CLI='codex exec --skip-git-repo-check --sandbox read-only "Read this UTF-8 prompt file and output only the final answer: {prompt_file}"'
$env:WIKI_AGENT_CLI_TIMEOUT='8'
python tools\viewer.py
```

If you want the agent to automatically use a locally installed `codex` command without setting `WIKI_AGENT_CLI`, opt in explicitly:

```powershell
$env:WIKI_AGENT_ENABLE_CODEX_CLI='1'
$env:WIKI_AGENT_CLI_TIMEOUT='8'
python scripts\wiki_agent.py "What is KNN?"
```

File watcher:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\agent_watch.ps1
```

Add a message:

```powershell
'What is regularization?' | Set-Content agent_messages\inbox\q1.txt -Encoding UTF8
```

Read the response:

```powershell
Get-Content agent_messages\outbox\q1.response.json -Raw
```

## Demo

The `demo/` folder contains a screenshot proving that the current Wiki renders in the browser viewer:

```text
demo/wiki-viewer-demo.png
```

## Validation Checklist

Run these before publishing:

```powershell
python -m py_compile scripts\ingest_raw.py scripts\server.py scripts\wiki_agent.py mcp\wiki_mcp_server.py tools\mcp_server.py tools\viewer.py
```

Check MCP tool listing:

```powershell
python -c "import json, subprocess, sys; req={'jsonrpc':'2.0','id':1,'method':'tools/list'}; p=subprocess.run([sys.executable,'tools/mcp_server.py'],input=json.dumps(req),text=True,capture_output=True,encoding='utf-8'); print(p.stdout)"
```

Check viewer:

```powershell
python tools\viewer.py
```

Then open:

```text
http://127.0.0.1:8765
```
