from __future__ import annotations

from pathlib import Path

from frames_pack.utils import help

if __name__ == "__main__":
    help(
        module_name="frames_pack",
        source_dir=Path(__file__).parent.absolute(),
        ignores={"__init__.py", "__main__.py"},
        ignore_docs=False,
    )
