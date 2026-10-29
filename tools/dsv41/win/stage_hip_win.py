#!/usr/bin/env python3
"""Stage a self-built strata-dsv41.exe (tools\\dsv41\\win\\build_hip_win.bat) as a Windows HIP engine folder Strata can start.

    python tools\\dsv41\\win\\stage_hip_win.py --build BUILD_DIR --archs gfx1100 --out OUT
    set STRATA_DSV41_EXE=OUT\\strata-windows-x64-hip\\strata-dsv41.exe

The folder has the layout of the Windows AMD DeepSeek package (packaging/README.md, "Windows AMD"): strata-dsv41.exe with the HIP
runtime beside it, rocm/bin (hipBLAS / rocBLAS / hipBLASLt and their imports), the GEMM kernels and rocm/.kpack for these archs only,
the hipBLASLt tuning tables, the licenses and a BUILD.json that names "lib_dirs": ["rocm/bin"].  setup.py and strata launch put those
folders on the engine's PATH (strata_control/dsv41_engine.py lib_dirs).  It is tools/hip/package_windows.py with strata-dsv41.exe as
the program, so the two stay the same.

--rocm defaults to the ROCm of ROCM_VENV (default <repo>\\.rocm-win), the same one the build used.  Run it from a Visual Studio x64
prompt (or after vcvars64.bat): the Microsoft C++ runtime DLLs are copied from VCToolsRedistDir.

Used for an RX 7900 XTX (gfx1100) on Windows 11, ROCm 10.2.0a20260930, 2026-10-29: the folder is 392 MiB (133 MiB zipped) and
ds4_iq_test passes on the default (scalar) paths there.  The release feed has no package for this card (#4519).
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "hip"))
sys.path.insert(0, str(ROOT))
import package_windows as pw  # noqa: E402


def rocm_root() -> str:
    venv = Path(os.environ.get("ROCM_VENV") or ROOT / ".rocm-win")
    return subprocess.run([str(venv / "Scripts" / "rocm-sdk.exe"), "path", "--root"], capture_output=True, text=True, check=True).stdout.strip()


def main() -> int:
    args = sys.argv[1:]
    if "--rocm" not in args:
        args += ["--rocm", rocm_root()]
    if "--rocm-version" not in args:
        args += ["--rocm-version", "10.2.0a20260930"]          # tools\hip\build_windows.bat STRATA_ROCM_VERSION
    pw.PROGRAMS = ("strata-dsv41.exe",)
    sys.argv = [sys.argv[0], *args]
    return pw.main()


if __name__ == "__main__":
    sys.exit(main())
