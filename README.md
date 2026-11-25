# pyaubo_sdk examples (AUBO robot arms)

Example code and notes for controlling AUBO robot arms (ARCS controller, e.g. AUBO i5 / C5) through the official SDK.

## Contents

| Path | What it is |
|---|---|
| `lib/` | Prebuilt `pyaubo_sdk` 0.26.0rc6 module (Linux x86_64, CPython 3.12) + its package METADATA |
| `pyaubo.py` | Minimal Python example: connect + log in to an ARCS controller / simulator over RPC (port 30004) |
| `pyaubo_sdk文档.md` | Chinese API notes for `pyaubo_sdk` (motion, force control, IO, …) |
| `help` | `help(pyaubo_sdk)` dump — full Python API signatures (UTF-16 text) |
| `share/doc/error_code.md` | Controller error codes |
| `share/doc/rtde_recipe.md` | RTDE recipe fields |
| `share/example/python/` | Python examples (movej / movel / movec, IO, force control, scripts, …) |
| `share/example/c++/` | C++ examples |
| `share/example/aubo_script/` | AUBO script examples |

## Getting started

1. Get `pyaubo_sdk`. This repo includes a prebuilt module in `lib/`:
   - `lib/pyaubo_sdk.cpython-312-x86_64-linux-gnu.so`: **pyaubo_sdk 0.26.0rc6, Linux x86_64, Python 3.12 only**. It only needs the standard C/C++ runtime (libstdc++, libc).
   - Install it into a virtual env:
     ```bash
     python3.12 -m venv venv && source venv/bin/activate
     cp lib/pyaubo_sdk.cpython-312-x86_64-linux-gnu.so "$(python -c 'import site;print(site.getsitepackages()[0])')/"
     python -c "import pyaubo_sdk; print('ok')"
     ```
   - On other Python versions or platforms (Windows, aarch64), use `pip install pyaubo-sdk` or get it from AUBO's SDK download page.
   - The client was tested here with ARCS controllers that report RPC interface 0.22.2 (AUBO i5 / C5).
2. Edit the IP, username and password in `pyaubo.py` (placeholders: `192.168.1.100`, `aubo`, `your_password`).
3. `python pyaubo.py`

⚠️ The examples can move the real arm. Try them on the ARCS simulator first, keep the speed low and keep a hand on the emergency stop.

## Notes

- The SDK, the prebuilt module and the examples are © AUBO Robotics (the package metadata declares the MIT licence; see `lib/pyaubo_sdk-0.26.0rc6.METADATA`). This repository only re-shares them for learning; all rights belong to AUBO.
- The connection defaults in `pyaubo.py` were replaced with placeholders.
