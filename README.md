# Planetary KP API (Installable Python Module)

This project is packaged so anyone can install and use it as:
- a Python module in code, and
- a runnable FastAPI server.

## Install (local project)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install .
```

Install from GitHub:

```powershell
pip install --upgrade --force-reinstall "git+https://github.com/vineetllm/fastapi-railway.git@main"
```

## Required runtime inputs

- KP mapping excel is bundled in the package by default (`planetary_kp_api/data/kp_mapping_all.xlsx`)
- Swiss ephemeris files are optional.
  Without ephemeris files, the package automatically falls back to Moshier mode (no separate install).
- Optional high-precision mode: set `EPHE_PATH` to a folder containing `.se1/.se2` files.
- Optional override: set `KP_MAPPING_FILE` to use your own mapping file

Example:

```powershell
$env:EPHE_PATH = "C:\ephe"  # optional
```

## Run as API server (after install)

```powershell
planetary-kp-api --host 0.0.0.0 --port 8000
```

Swagger UI:
- `http://127.0.0.1:8000/docs`

## Deploy on Railway

This repo is already configured with a `Procfile`:

```text
web: python -m planetary_kp_api --host 0.0.0.0
```

Railway injects `PORT`, and the app reads it automatically.
`nixpacks.toml` is included to install SQLite runtime (`libsqlite3-0`) required by `pyswisseph`.

### Steps

1. Push this folder to GitHub.
2. In Railway: `New Project` -> `Deploy from GitHub Repo`.
3. Select this repo/service.
4. Set variables in Railway service:
   - `EPHE_PATH=./ephe` (optional, only if you provide ephemeris files)
5. Optional: if using high-precision Swiss files, include `ephe/` directory in repo
6. Deploy.

Health check URL:
- `/health`

## Use directly in Python code

Recommended (remote call, no `pyswisseph` needed):

```python
from datetime import date, time
from planetary_kp_api import generate_kp_mapping_remote

result = generate_kp_mapping_remote(
    base_url="https://web-production-278cd.up.railway.app",
    date_value=date(2026, 3, 25),
    time_value=time(9, 15),
    latitude=19.076,
    longitude=72.8777,
    timezone_offset=5.5,
    ayanamsa="Lahiri",
)
```

Local generation (optional):

```powershell
pip install "planetary-kp-api[local]"
```

```python
from datetime import date, time
from planetary_kp_api import generate_kp_mapping

result = generate_kp_mapping(
    date_value=date(2026, 3, 25),
    time_value=time(9, 15),
    latitude=19.076,
    longitude=72.8777,
    timezone_offset=5.5,
    ayanamsa="Lahiri",
)
```

```python
from datetime import date, time
from planetary_kp_api import generate_kp_mapping

result = generate_kp_mapping(
    date_value=date(2026, 3, 25),
    time_value=time(9, 15),
    latitude=19.076,
    longitude=72.8777,
    timezone_offset=5.5,
    ayanamsa="Lahiri",
    ephe_path=r"C:\ephe",  # optional
)

print(result["meta"])
print(result["data"][:2])
```

## HTTP endpoint

- `POST /api/planetary-kp-mapping`
- `GET /api/planets`
- `GET /health`

Sample request body:

```json
{
  "date": "2026-03-25",
  "time": "09:15:00",
  "latitude": 19.076,
  "longitude": 72.8777,
  "timezone_offset": 5.5,
  "ayanamsa": "Lahiri",
  "planets": ["Asc", "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu"]
}
```

## Build distributable package

```powershell
python -m pip install build
python -m build
```

This creates:
- `dist/*.whl`
- `dist/*.tar.gz`

Anyone can install your wheel:

```powershell
pip install planetary_kp_api-0.1.0-py3-none-any.whl
```
