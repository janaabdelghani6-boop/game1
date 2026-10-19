from __future__ import annotations

import runpy
from pathlib import Path


def main() -> None:
    project_root = Path(__file__).resolve().parent
    hub_main = (
        project_root
        / "Ai maze"
        / "Ai maze - Copy - Copy - Copy - Copy"
        / "AI controlled game"
        / "main.py"
    )
    runpy.run_path(str(hub_main), run_name="__main__")


if __name__ == "__main__":
    main()