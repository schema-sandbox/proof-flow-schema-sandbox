# Base images are digest-pinned so rebuilds are reproducible; Dependabot keeps
# them current.
FROM node:22-bookworm-slim@sha256:d649c27dae7ba0137b3cef5dd75baa422c08dc3d9e3fc0c23dfb172dc3cc6436 AS web-build

WORKDIR /src
COPY apps/web/package.json apps/web/package-lock.json ./apps/web/
RUN npm ci --prefix apps/web
COPY apps/web ./apps/web
RUN npm run build --prefix apps/web

FROM python:3.12-slim@sha256:9e869b0816f5537709825b49e62dc86d1c2691eff19b05c1d4dc3a07992cc052

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/apps/api \
    PROOFFLOW_WORKSPACE=/data/workspaces \
    PROOFFLOW_PLUGIN_ROOT=/data/plugins

WORKDIR /app
COPY pyproject.toml README.md requirements.txt ./
COPY apps/api ./apps/api
RUN pip install --no-cache-dir .
COPY schemas ./schemas
COPY prototype ./prototype
COPY --from=web-build /src/apps/web/dist ./apps/web/dist

RUN useradd --create-home --uid 10001 proofflow \
    && mkdir -p /data/workspaces /data/plugins \
    && chown -R proofflow:proofflow /app /data
USER proofflow

VOLUME ["/data"]
EXPOSE 8000
CMD ["uvicorn", "schemamath_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
