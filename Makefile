.PHONY: run test schemas openapi demo release

run:
	./scripts/run_api.sh

test:
	./scripts/test.sh

schemas:
	PYTHONPATH=apps/api python scripts/export_runtime_schemas.py
	PYTHONPATH=apps/api python scripts/validate_schemas.py

openapi:
	PYTHONPATH=apps/api python scripts/export_openapi.py

demo:
	./scripts/create_demo.sh

release:
	PYTHONPATH=apps/api python scripts/build_release.py
