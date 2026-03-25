from __future__ import annotations

import argparse
import os

import uvicorn


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Planetary KP Mapping FastAPI server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true")
    parser.add_argument("--log-level", default="info")
    parser.add_argument("--kp-mapping-file", default=None)
    parser.add_argument("--ephe-path", default=None)
    args = parser.parse_args()

    if args.kp_mapping_file:
        os.environ["KP_MAPPING_FILE"] = args.kp_mapping_file
    if args.ephe_path:
        os.environ["EPHE_PATH"] = args.ephe_path

    uvicorn.run(
        "planetary_kp_api.api:create_app",
        factory=True,
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level,
    )


if __name__ == "__main__":
    main()
