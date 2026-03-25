from __future__ import annotations

from datetime import date as dt_date
from datetime import time as dt_time
from typing import Any, Literal

from pydantic import BaseModel, Field

DEFAULT_PLANETS = [
    "Asc",
    "Sun",
    "Moon",
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
    "Rahu",
    "Ketu",
]


class KpMappingRequest(BaseModel):
    date: dt_date = Field(..., description="Local date")
    time: dt_time = Field(default=dt_time(9, 15), description="Local time")
    latitude: float = Field(default=19.076)
    longitude: float = Field(default=72.8777)
    timezone_offset: float = Field(default=5.5, description="Hours offset from UTC, e.g. 5.5")
    ayanamsa: Literal["Lahiri", "Krishnamurti", "Raman"] = "Lahiri"
    planets: list[str] = Field(default_factory=lambda: DEFAULT_PLANETS.copy())


class KpMappingResponse(BaseModel):
    meta: dict[str, Any]
    data: list[dict[str, Any]]

