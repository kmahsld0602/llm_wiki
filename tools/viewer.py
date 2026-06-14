"""Browser viewer entrypoint.

Run:
    python tools/viewer.py
"""

from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT / "scripts" / "server.py"), run_name="__main__")
