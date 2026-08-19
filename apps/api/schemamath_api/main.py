from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, Response
from fastapi.staticfiles import StaticFiles

from . import __version__
from . import api as api_module
from .auth import APIKeyAuthMiddleware
from .config import Settings
from .service import SchemaMathService


def _resolve_ui_dirs() -> tuple[Path | None, Path | None]:
    """Locate the HTTP frontend bundles across source and wheel layouts.

    When installed from a source checkout the static directories live next to
    the repository root.  When installed as a wheel they may be shipped under
    ``schemamath_api/_ui`` as package data.  Either layout failing to resolve
    is reported as ``None`` so the API can degrade gracefully instead of
    importing a non-existent package path.
    """
    source_root = Path(__file__).resolve().parents[3]
    source_prototype = source_root / "prototype"
    source_web = source_root / "apps" / "web" / "dist"
    prototype: Path | None = None
    web_dist: Path | None = None

    from importlib.resources import files as _package_files

    packaged_root: Path | None = None
    try:
        packaged_root = Path(_package_files("schemamath_api").joinpath("_ui"))
    except (ImportError, TypeError, FileNotFoundError):
        packaged_root = None
    if source_prototype.is_dir():
        prototype = source_prototype
    elif packaged_root is not None and (packaged_root / "prototype").is_dir():
        prototype = packaged_root / "prototype"
    if source_web.is_dir():
        web_dist = source_web
    elif packaged_root is not None and (packaged_root / "web_dist").is_dir():
        web_dist = packaged_root / "web_dist"
    return prototype, web_dist


def create_app(workspace_root: Path | None = None, plugin_root: Path | None = None) -> FastAPI:
    settings = Settings.from_environment(workspace_root, plugin_root)
    service = SchemaMathService(settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        for env_key in ("PROOFFLOW_HOST", "SCHEMAMATH_HOST", "HOST"):
            val = os.environ.get(env_key)
            if val:
                settings.validate_host_security(val)
        yield

    app = FastAPI(
        title="ProofFlow Schema Sandbox Local API",
        version=__version__,
        description=(
            "Local-first experimental research workspace. It does not promise "
            "solutions and does not automatically label results as solved."
        ),
        lifespan=lifespan,
    )
    app.state.settings = settings
    app.state.service = service

    if settings.auth_enabled:
        app.add_middleware(
            APIKeyAuthMiddleware,
            secret_key=settings.secret_key or "",
            valid_api_keys=settings.api_keys,
        )

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

    @app.middleware("http")
    async def loopback_security_guard(request, call_next):
        # When auth is disabled (local mode), fail closed on any non-loopback client request
        if not settings.auth_enabled:
            client_host = request.client.host if request.client else None
            if client_host and client_host not in {"127.0.0.1", "::1", "localhost", "testclient"}:
                return Response(
                    content=(
                        b"Forbidden: Unauthenticated remote access is disabled. "
                        b"Set PROOFFLOW_SECRET_KEY and PROOFFLOW_API_KEYS to enable authenticated remote access."
                    ),
                    status_code=403,
                    media_type="text/plain",
                )
        return await call_next(request)

    @app.middleware("http")
    async def security_headers(request, call_next):
        response = await call_next(request)
        if response.headers.get("content-type", "").startswith("text/html"):
            response.headers.setdefault(
                "Content-Security-Policy",
                "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: blob:; font-src 'self' data:; connect-src 'self'; "
                "worker-src 'self' blob:; object-src 'none'; base-uri 'self'; "
                "frame-ancestors 'none'",
            )
        return response

    app.dependency_overrides[api_module.get_service] = lambda: service
    app.include_router(api_module.router)

    prototype_path, web_dist_path = _resolve_ui_dirs()

    if prototype_path is not None:
        app.mount("/prototype", StaticFiles(directory=prototype_path, html=True), name="prototype")
    if web_dist_path is not None:
        app.mount("/app", StaticFiles(directory=web_dist_path, html=True), name="web")

    if not web_dist_path and not prototype_path:
        @app.get("/", include_in_schema=False)
        def root_unbundled() -> Response:
            body = (
                b"ProofFlow API is running. "
                b"The HTTP frontend bundle is not present in this installation; "
                b"see README 'Running the frontend'."
            )
            return Response(content=body, media_type="text/plain")

        return app

    @app.get("/health")
    def health() -> dict[str, str]:
        return {
            "status": "ok",
            "version": __version__,
            "environment": settings.environment,
            "auth_enabled": str(settings.auth_enabled).lower(),
        }

    @app.get("/", include_in_schema=False)
    def root() -> RedirectResponse:
        return RedirectResponse(url="/prototype/" if prototype_path is not None else "/app/")

    return app


app = create_app()
