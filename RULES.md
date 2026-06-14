# Agent Operating Rules

This repository is an executable LLM Wiki product. Agents working in this repository must follow these rules.

## Goals

- Keep the Wiki usable by a first-time user who clones the repository.
- Preserve source traceability from `raw/` files to `wiki/` pages.
- Prefer small, reviewable Markdown updates over automatic large rewrites.
- Keep the MCP Tool server, viewer, Wiki pages, and harness documentation in sync.

## Repository Roles

- `raw/`: source materials provided by the user.
- `wiki/`: curated Markdown Wiki pages.
- `schema/`: expected structure for Wiki pages and raw source metadata.
- `tools/`: executable entrypoints for MCP Tool access and the browser viewer.
- `scripts/`: implementation helpers used by the tools and workflow.
- `skills/`: agent skill instructions for maintaining and extending the Wiki.
- `demo/`: proof that the Wiki renders in the viewer.

## Agent Permissions

Agents may:

- Read `raw/`, `wiki/`, `schema/`, `README.md`, and documentation files.
- Create merge requests in `wiki/merge-queue`.
- Propose or make small Wiki edits when the user explicitly requests integration.
- Use MCP tools for page listing, search, page retrieval, and Wiki question answering.

Agents must not:

- Delete user-provided raw source files.
- Replace a Wiki page without preserving its front matter.
- Add unsupported claims without a source path in the page or merge request.
- Automatically publish private or sensitive user materials.

## Wiki Page Requirements

Every page in `wiki/ml` should include:

- YAML front matter with `title`, `slug`, `tags`, and `updated`.
- A clear heading matching the page concept.
- Short sections that explain what the concept is, why it matters, and how it is used.
- A `Sources` section when the page is based on raw source material.
- Related page links using `[[slug]]` when relevant.

## Raw Source Integration

1. Put source files in `raw/inbox`.
2. Run `python scripts/ingest_raw.py`.
3. Review the generated `wiki/merge-queue/*-merge-request.md`.
4. Merge supported information into an existing page or create a new page.
5. Verify in the viewer with `python tools/viewer.py`.

## Verification Checklist

- `python -m py_compile scripts/*.py mcp/*.py tools/*.py`
- `python tools/mcp_server.py` responds to `tools/list` and `tools/call`.
- `python tools/viewer.py` starts the viewer.
- A browser can open `http://127.0.0.1:8765`.
- The new or updated page appears in search.
