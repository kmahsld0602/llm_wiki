# Merge Queue

`scripts/ingest_raw.py` creates merge request files in this directory.

After reviewing a merge request, run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\merge_raw_with_codex.ps1 wiki\merge-queue\<merge-request-file>.md
```

