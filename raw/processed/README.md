# Raw Inbox

Put new source files here as `.pdf`, `.txt`, or `.md`.

Example:

```text
raw/inbox/llm-quantization-paper.pdf
```

Then run:

```powershell
python scripts\ingest_raw.py
```

PDF text is extracted to `raw/extracted/<pdf-name>.txt`.
