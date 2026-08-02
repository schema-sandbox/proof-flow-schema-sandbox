from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from . import __version__
from . import api as api_module
from .config import Settings
from .service import SchemaMathService


def _build_token_middleware(token: str | None):
    """Gate the /api/* surface behind a shared Bearer/X-API-Key token.

    The token is optional. When unset the service behaves as before so the
    local web UI and existing clients keep working without configuration.
    Static assets, /health and the schema routes stay open.
    """

    async def dispatch(request, call_next):
        path = request.url.path
        if token is None or not path.startswith("/api/"):
            return await call_next(request)
        authorization = request.headers.get("Authorization", "")
        api_key = request.headers.get("X-API-Key", "")
        if authorization == f"Bearer {token}" or api_key == token:
            return await call_next(request)
        return JSONResponse(status_code=401, content={"detail": "missing or invalid API token"})

    return dispatch


def create_app(workspace_root: Path | None = None, plugin_root: Path | None = None) -> FastAPI:
    settings = Settings.from_environment(workspace_root, plugin_root)
    service = SchemaMathService(settings)

    app = FastAPI(
        title="ProofFlow Schema Sandbox Local API",
        version=__version__,
        description=(
            "Local-first experimental research workspace. It does not promise "
            "solutions and does not automatically label results as solved."
        ),
    )
    app.state.settings = settings
    app.state.service = service

    app.middleware("http")(_build_token_middleware(settings.api_token))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:5173",
            "http://localhost:5173",
            "http://127.0.0.1:8000",
            "http://localhost:8000",
        ],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.dependency_overrides[api_module.get_service] = lambda: service
    app.include_router(api_module.router)

    repository_root = Path(__file__).resolve().parents[3]
    prototype_path = repository_root / "prototype"
    web_dist_path = repository_root / "apps" / "web" / "dist"
    if prototype_path.exists():
        app.mount("/prototype", StaticFiles(directory=prototype_path, html=True), name="prototype")
    if web_dist_path.exists():
        app.mount("/app", StaticFiles(directory=web_dist_path, html=True), name="app")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {
            "status": "ok",
            "version": __version__,
            "workspace_root": str(settings.workspace_root),
        }

    @app.get("/", include_in_schema=False)
    def root() -> RedirectResponse:
        return RedirectResponse(url="/app/" if web_dist_path.exists() else "/prototype/")

    return app


app = create_app()
