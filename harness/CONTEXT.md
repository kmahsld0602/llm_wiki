# Harness Context

The harness defines how an agent should operate this project.

## Product Summary

This project turns source materials into a local LLM Wiki. It includes:

- A Markdown Wiki under `wiki/`.
- Raw source ingestion under `raw/`.
- A JSON-RPC MCP Tool server under `tools/`.
- A browser viewer under `static/` served by `tools/viewer.py`.
- Agent rules and skills for safe Wiki maintenance.

## Default Workflow

For one new source:

1. Place the file in `raw/inbox`.
2. Run `python scripts/ingest_raw.py --file <filename>`.
3. Read the generated merge request in `wiki/merge-queue`.
4. Decide whether to merge into an existing page or create a new page.
5. Add source paths to the target Wiki page.
6. Run the viewer and verify the page appears.

## Decision Policy

- Prefer merging into an existing page when the source extends the same concept.
- Create a new page when the source introduces a separate concept.
- Leave a merge request for human review when the source is ambiguous.
- Keep raw source excerpts out of final pages unless the quotation is short and necessary.

## Tooling Contract

Agents should use `tools/mcp_server.py` for Wiki access. It supports:

- `tools/list`
- `tools/call` with `list_pages`
- `tools/call` with `search_pages`
- `tools/call` with `get_page`
- `tools/call` with `ask_wiki`
