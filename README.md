# pyaubo_sdk examples (AUBO robot arms)

Example code and notes for controlling AUBO robot arms (ARCS controller, e.g. AUBO i5 / C5) through the official SDK.

## Contents

| Path | What it is |
|---|---|
| `pyaubo.py` | Minimal Python example: connect + log in to an ARCS controller / simulator over RPC (port 30004) |
| `pyaubo_sdk文档.md` | Chinese API notes for `pyaubo_sdk` (motion, force control, IO, …) |
| `help` | `help(pyaubo_sdk)` dump — full Python API signatures (UTF-16 text) |
| `share/doc/error_code.md` | Controller error codes |
| `share/doc/rtde_recipe.md` | RTDE recipe fields |
| `share/example/python/` | Python examples (movej / movel / movec, IO, force control, scripts, …) |
| `share/example/c++/` | C++ examples |
| `share/example/aubo_script/` | AUBO script examples |

## Getting started

1. Install the `pyaubo_sdk` wheel that matches your controller version (from AUBO's SDK download / support).
2. Edit the IP, username and password in `pyaubo.py` (placeholders: `192.168.1.100`, `aubo`, `your_password`).
3. `python pyaubo.py`

⚠️ The examples can move the real arm. Try them on the ARCS simulator first, keep the speed low and keep a hand on the emergency stop.

## Notes

- The SDK and the examples are © AUBO Robotics. This repository only re-shares them for learning; all rights belong to AUBO.
- The connection defaults in `pyaubo.py` were replaced with placeholders.
