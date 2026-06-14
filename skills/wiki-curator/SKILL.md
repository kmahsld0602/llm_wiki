# Wiki Curator Skill

Use this skill when integrating a new source into the LLM Wiki or reviewing a merge request.

## Objective

Convert raw source material into maintainable Wiki knowledge while preserving traceability.

## Inputs

- A raw source file in `raw/inbox`, or
- A merge request in `wiki/merge-queue`, or
- A user request to add or revise Wiki content.

## Process

1. Inspect the source title, filename, and extracted text.
2. Search existing Wiki pages using the MCP Tool server.
3. Choose one decision:
   - `MERGE`: update an existing page.
   - `CREATE`: create a new page.
   - `REVIEW`: leave for human review.
4. Preserve YAML front matter when editing existing pages.
5. Add or update a `Sources` section with raw and extracted paths.
6. Add related page links using `[[slug]]` where useful.
7. Verify the page can be listed and searched by the MCP server.

## Output Expectations

For a completed integration, the final state should include:

- One or more updated Markdown pages in `wiki/ml`.
- Source paths recorded in each affected page.
- Searchable title, slug, and tags.
- No unsupported claims beyond the source or existing Wiki context.

## Safety

Do not delete raw files. Do not overwrite a page wholesale unless the user explicitly asks for a rewrite. If the source is unclear, produce a merge request or review note instead of forcing a merge.
