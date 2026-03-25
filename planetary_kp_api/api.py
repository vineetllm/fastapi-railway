from __future__ import annotations

import os
from functools import lru_cache

from fastapi import FastAPI, HTTPException

from planetary_kp_api.schemas import KpMappingRequest, KpMappingResponse
from planetary_kp_api.services.kp_mapping import KpMappingService, PLANET_ORDER


def _default_ephe_path() -> str:
    env_value = os.getenv("EPHE_PATH")
    if env_value:
        return env_value
    if os.path.exists("C:/ephe"):
        return "C:/ephe"
    return "./ephe"


def create_app() -> FastAPI:
    app = FastAPI(title="Planetary KP Mapping API", version="1.1.0")

    @lru_cache(maxsize=1)
    def get_service() -> KpMappingService:
        kp_mapping_file = os.getenv("KP_MAPPING_FILE", "kp_mapping_all.xlsx")
        ephe_path = _default_ephe_path()
        return KpMappingService(
            kp_mapping_path=kp_mapping_file,
            ephe_path=ephe_path,
        )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/planets")
    def available_planets() -> dict[str, list[str]]:
        return {"planets": PLANET_ORDER}

    @app.post("/api/planetary-kp-mapping", response_model=KpMappingResponse)
    def planetary_kp_mapping(payload: KpMappingRequest) -> KpMappingResponse:
        try:
            service = get_service()
            meta, data = service.generate(
                local_date=payload.date,
                local_time=payload.time,
                latitude=payload.latitude,
                longitude=payload.longitude,
                timezone_offset=payload.timezone_offset,
                ayanamsa=payload.ayanamsa,
                planets=payload.planets,
            )
            return KpMappingResponse(meta=meta, data=data)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Failed to generate KP mapping: {exc}") from exc

    return app


app = create_app()
