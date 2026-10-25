# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2.9,<3"]
# ///
"""agent-kit command line. Run ``uv run scripts/kit.py --help``.

Commands: list, detect, install, check. The code lives in ``scripts/agent_kit``.
"""

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))  # lets `uv run` find agent_kit from any directory

from agent_kit import KitCli, KitLayout  # noqa: E402  (needs the path above)

if __name__ == "__main__":
    raise SystemExit(KitCli(KitLayout(root=SCRIPTS_DIR.parent)).run())
