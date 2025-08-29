from __future__ import annotations

"""Minimal HTTP backend for VulnScan-AI.

The backend exposes a single ``/scan`` endpoint that accepts a JSON payload
with a list of targets.  Each target is assessed using the common utilities
in :mod:`scanner`, and the raw outputs plus report paths are returned as JSON.

The implementation prefers FastAPI for its modern features.  If FastAPI is
not installed, running this module will emit a helpful message instead of
raising an ImportError so that the rest of the project remains usable.
"""

from typing import List

from scanner import assess_target

try:  # FastAPI is optional but recommended
    from fastapi import FastAPI
    from pydantic import BaseModel

    app = FastAPI(title="VulnScan-AI Backend")

    class ScanRequest(BaseModel):
        targets: List[str]

    class ScanResult(BaseModel):
        target: str
        scan_output: str
        exploit_output: str
        report: str

    @app.post("/scan", response_model=List[ScanResult])
    def scan(req: ScanRequest) -> List[ScanResult]:
        results: List[ScanResult] = []
        for target in req.targets:
            out = assess_target(target)
            results.append(
                ScanResult(
                    target=target,
                    scan_output=out["scan_output"],
                    exploit_output=out["exploit_output"],
                    report=str(out["report_path"]),
                )
            )
        return results

    def main() -> None:  # pragma: no cover - startup helper
        import uvicorn

        uvicorn.run(app, host="0.0.0.0", port=8000)
except ModuleNotFoundError:  # pragma: no cover - FastAPI optional
    app = None

    def main() -> None:  # pragma: no cover - startup helper
        print(
            "FastAPI and uvicorn are required for the backend. "
            "Install them with `pip install fastapi uvicorn`."
        )


if __name__ == "__main__":  # pragma: no cover - manual launch
    main()
