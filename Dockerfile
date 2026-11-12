# Base images are digest-pinned so rebuilds are reproducible; Dependabot keeps
# them current.
FROM node:22-bookworm-slim@sha256:d649c27dae7ba0137b3cef5dd75baa422c08dc3d9e3fc0c23dfb172dc3cc6436 AS web-build

WORKDIR /src
COPY apps/web/package.json apps/web/package-lock.json ./apps/web/
RUN npm ci --prefix apps/web
COPY apps/web ./apps/web
RUN npm run build --prefix apps/web

FROM python:3.15-slim@sha256:65a65fc7b30b06cb6df4930fd4650697cb23f4c2698ab81fc87e4b031bc36928

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/apps/api \
    PROOFFLOW_ENV=production \
    PROOFFLOW_WORKSPACE=/data/workspaces \
    PROOFFLOW_PLUGIN_ROOT=/data/plugins

WORKDIR /app
COPY pyproject.toml README.md requirements.txt LICENSE THIRD_PARTY_NOTICES.md sbom.cyclonedx.json ./
COPY apps/api ./apps/api
RUN pip install --no-cache-dir .
COPY schemas ./schemas
COPY prototype ./prototype
COPY plugins ./plugins
COPY --from=web-build /src/apps/web/dist ./apps/web/dist

RUN useradd --create-home --uid 10001 proofflow \
    && mkdir -p /data/workspaces /data/plugins \
    && chown -R proofflow:proofflow /app /data
USER proofflow

VOLUME ["/data"]
EXPOSE 8000
CMD ["uvicorn", "schemamath_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
