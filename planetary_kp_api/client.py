from __future__ import annotations

import os
from datetime import date, time

from planetary_kp_api.schemas import DEFAULT_PLANETS
from planetary_kp_api.services.kp_mapping import KpMappingService, PLANET_ORDER


def _default_ephe_path() -> str:
    env_value = os.getenv("EPHE_PATH")
    if env_value:
        return env_value
    if os.path.exists("C:/ephe"):
        return "C:/ephe"
    return "./ephe"


def generate_kp_mapping(
    *,
    date_value: date,
    time_value: time = time(9, 15),
    latitude: float = 19.076,
    longitude: float = 72.8777,
    timezone_offset: float = 5.5,
    ayanamsa: str = "Lahiri",
    planets: list[str] | None = None,
    kp_mapping_file: str | None = None,
    ephe_path: str | None = None,
) -> dict:
    """Generate the planetary KP mapping table directly in Python (no HTTP call)."""
    service = KpMappingService(
        kp_mapping_path=kp_mapping_file or os.getenv("KP_MAPPING_FILE"),
        ephe_path=ephe_path or _default_ephe_path(),
    )
    meta, data = service.generate(
        local_date=date_value,
        local_time=time_value,
        latitude=latitude,
        longitude=longitude,
        timezone_offset=timezone_offset,
        ayanamsa=ayanamsa,
        planets=planets or DEFAULT_PLANETS.copy(),
    )
    return {"meta": meta, "data": data}


__all__ = ["generate_kp_mapping", "PLANET_ORDER"]
