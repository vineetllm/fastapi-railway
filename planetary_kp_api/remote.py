from __future__ import annotations

from datetime import date, time
from typing import Any

import requests

from planetary_kp_api.schemas import DEFAULT_PLANETS


def generate_kp_mapping_remote(
    *,
    base_url: str,
    date_value: date,
    time_value: time = time(9, 15),
    latitude: float = 19.076,
    longitude: float = 72.8777,
    timezone_offset: float = 5.5,
    ayanamsa: str = "Lahiri",
    planets: list[str] | None = None,
    timeout: float = 120.0,
) -> dict[str, Any]:
    """Generate KP mapping by calling the deployed HTTP API."""
    payload = {
        "date": date_value.isoformat(),
        "time": time_value.strftime("%H:%M:%S"),
        "latitude": latitude,
        "longitude": longitude,
        "timezone_offset": timezone_offset,
        "ayanamsa": ayanamsa,
        "planets": planets or DEFAULT_PLANETS.copy(),
    }
    url = f"{base_url.rstrip('/')}/api/planetary-kp-mapping"
    response = requests.post(url, json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json()
