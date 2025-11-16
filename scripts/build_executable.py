"""Build a standalone advplate executable using PyInstaller."""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ENTRY = PROJECT_ROOT / "src" / "plateshapez" / "__main__.py"
DIST_DIR = PROJECT_ROOT / "dist"


def check_pyinstaller() -> None:
    """Ensure PyInstaller is available before attempting to build."""
    if shutil.which("pyinstaller") is None:
        raise SystemExit(
            "PyInstaller is not installed. Install it with: uv sync --group build"
        )


def build() -> None:
    """Invoke PyInstaller to create a onefile CLI executable."""
    check_pyinstaller()
    cmd = [
        "pyinstaller",
        "--name",
        "advplate",
        "--onefile",
        "--clean",
        "--console",
        "--collect-submodules",
        "plateshapez",
        "--copy-metadata",
        "plateshapez",
        str(SRC_ENTRY),
    ]
    env = os.environ.copy()
    env.setdefault("PYTHONPATH", str(PROJECT_ROOT / "src"))
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=PROJECT_ROOT, env=env)
    print(f"\nExecutable created in: {DIST_DIR}")


if __name__ == "__main__":
    try:
        build()
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode) from exc
