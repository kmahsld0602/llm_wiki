import argparse
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_INBOX = ROOT / "raw" / "inbox"
RAW_EXTRACTED = ROOT / "raw" / "extracted"
RAW_PROCESSED = ROOT / "raw" / "processed"
WIKI_DIR = ROOT / "wiki" / "ml"
MERGE_QUEUE = ROOT / "wiki" / "merge-queue"


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9가-힣]+", "-", text)
    return text.strip("-") or "raw-source"


def read_text_source(path):
    return path.read_text(encoding="utf-8")


def read_pdf_source(path):
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("PDF ingest requires pypdf. Install with: python -m pip install pypdf") from exc

    reader = PdfReader(str(path))
    chunks = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            chunks.append(f"\n\n--- page {index} ---\n{text.strip()}")

    extracted = "\n".join(chunks).strip()
    if not extracted:
        raise RuntimeError(f"No text could be extracted from PDF: {path.name}")

    RAW_EXTRACTED.mkdir(parents=True, exist_ok=True)
    extracted_path = RAW_EXTRACTED / f"{path.stem}.txt"
    extracted_path.write_text(extracted, encoding="utf-8")
    return extracted


def read_raw_source(path):
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return read_pdf_source(path)
    if suffix in {".txt", ".md"}:
        return read_text_source(path)
    raise RuntimeError(f"Unsupported raw source type: {path.suffix}")


def title_from_text(path, text):
    for line in text.splitlines():
        stripped = line.strip()
        normalized = stripped.lower()
        is_generic_heading = normalized == "machine learning" or normalized.endswith(" university")
        if not stripped or stripped.startswith("--- page") or is_generic_heading:
            continue
        if stripped.startswith("# "):
            return stripped[2:].strip()
        if re.match(r"^\d+\.\s+\S", stripped):
            return stripped[:80]
        if stripped:
            return stripped[:80]
    return path.stem.replace("-", " ").replace("_", " ").title()


def score(candidate_text, raw_text):
    tokens = re.findall(r"[a-zA-Z0-9가-힣-]+", raw_text.lower())
    tokens = [token for token in tokens if len(token) >= 3]
    haystack = candidate_text.lower()
    return sum(haystack.count(token) for token in set(tokens))


def candidate_pages(raw_text):
    ranked = []
    for path in sorted(WIKI_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        ranked.append((score(text, raw_text), path, text))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return ranked[:3]


def create_merge_request(raw_path):
    raw_text = read_raw_source(raw_path)
    title = title_from_text(raw_path, raw_text)
    raw_slug = slugify(title)
    candidates = candidate_pages(raw_text)

    MERGE_QUEUE.mkdir(parents=True, exist_ok=True)
    request_slug = slugify(raw_path.stem) or raw_slug
    request_path = MERGE_QUEUE / f"{request_slug}-merge-request.md"
    candidate_lines = "\n".join(
        f"- `{path.stem}` score={score_value} path=`wiki/ml/{path.name}`"
        for score_value, path, _ in candidates
    )
    top_target = candidates[0][1].stem if candidates else "new-page"
    excerpt = raw_text[:4000].strip()

    request = f"""---
title: Raw Source Merge Request - {title}
source: raw/inbox/{raw_path.name}
created: {date.today().isoformat()}
status: draft
suggested_target: {top_target}
---

# Raw Source Merge Request: {title}

## Suggested Target Pages

{candidate_lines or "- No candidate page found. Create a new page."}

## Merge Decision Needed

The agent must decide one of:

- `MERGE`: update an existing page under `wiki/ml`
- `CREATE`: create a new page under `wiki/ml`
- `REVIEW`: leave this request for human review if the source is unclear

## Agent Instructions

1. Read the raw source excerpt below.
2. Compare it with the suggested target pages.
3. Merge only information supported by the raw source.
4. Create a new page only when no current page fits.
5. Preserve front matter in existing pages.
6. Add a short change note to `wiki/log.md` if it exists.

## Raw Source Excerpt

```text
{excerpt}
```
"""
    request_path.write_text(request, encoding="utf-8")
    RAW_PROCESSED.mkdir(parents=True, exist_ok=True)
    shutil.copy2(raw_path, RAW_PROCESSED / raw_path.name)
    return request_path


def main():
    parser = argparse.ArgumentParser(description="Create merge requests from raw Wiki sources.")
    parser.add_argument("--file", help="Specific raw file under raw/inbox to ingest.")
    args = parser.parse_args()

    RAW_INBOX.mkdir(parents=True, exist_ok=True)
    supported = {".txt", ".md", ".pdf"}
    files = [RAW_INBOX / args.file] if args.file else sorted(
        path for path in RAW_INBOX.iterdir()
        if path.is_file() and path.suffix.lower() in supported
    )

    if not files:
        print(f"No .txt, .md, or .pdf files found in {RAW_INBOX}")
        return

    for raw_path in files:
        if not raw_path.exists():
            print(f"Missing file: {raw_path}")
            continue
        request_path = create_merge_request(raw_path)
        print(f"Created merge request: {request_path}")


if __name__ == "__main__":
    main()
