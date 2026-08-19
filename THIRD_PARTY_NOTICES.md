# Third-Party Software Notices and Full Software Bill of Materials (SBOM)

This project, **ProofFlow Schema Sandbox** (`0.1.0-alpha.8`), incorporates third-party open-source software packages under various permissive open-source licenses (Apache-2.0, MIT, BSD-2-Clause, BSD-3-Clause, ISC, 0BSD, Python-2.0, MPL-2.0).

**Total Tracked Components:** 397 (Python Ecosystem: 27, NPM Ecosystem: 370)

A machine-readable CycloneDX 1.5 SBOM is also distributed in [`sbom.cyclonedx.json`](sbom.cyclonedx.json).

---

## 1. Python Runtime & Core Tooling Dependencies

| Package | Version | License | Upstream Repository |
|---|---|---|---|
| `anyio` | `4.8.0` | MIT | [https://github.com/agronholm/anyio](https://github.com/agronholm/anyio) |
| `attrs` | `25.1.0` | MIT | [https://github.com/python-attrs/attrs](https://github.com/python-attrs/attrs) |
| `certifi` | `2025.1.31` | MPL-2.0 | [https://github.com/certifi/python-certifi](https://github.com/certifi/python-certifi) |
| `click` | `8.1.8` | BSD-3-Clause | [https://github.com/pallets/click](https://github.com/pallets/click) |
| `fastapi` | `0.115.8` | MIT | [https://github.com/fastapi/fastapi](https://github.com/fastapi/fastapi) |
| `h11` | `0.14.0` | MIT | [https://github.com/python-hyper/h11](https://github.com/python-hyper/h11) |
| `httpcore` | `1.0.7` | BSD-3-Clause | [https://github.com/encode/httpcore](https://github.com/encode/httpcore) |
| `httpx` | `0.28.1` | BSD-3-Clause | [https://github.com/encode/httpx](https://github.com/encode/httpx) |
| `idna` | `3.10` | BSD-3-Clause | [https://github.com/kjd/idna](https://github.com/kjd/idna) |
| `iniconfig` | `2.0.0` | MIT | [https://github.com/pytest-dev/iniconfig](https://github.com/pytest-dev/iniconfig) |
| `jsonschema` | `4.23.0` | MIT | [https://github.com/python-jsonschema/jsonschema](https://github.com/python-jsonschema/jsonschema) |
| `jsonschema-specifications` | `2024.10.1` | MIT | [https://github.com/python-jsonschema/jsonschema-specifications](https://github.com/python-jsonschema/jsonschema-specifications) |
| `mpmath` | `1.3.0` | BSD-3-Clause | [https://github.com/mpmath/mpmath](https://github.com/mpmath/mpmath) |
| `packaging` | `24.2` | Apache-2.0 | [https://github.com/pypa/packaging](https://github.com/pypa/packaging) |
| `pluggy` | `1.5.0` | MIT | [https://github.com/pytest-dev/pluggy](https://github.com/pytest-dev/pluggy) |
| `pydantic` | `2.10.6` | MIT | [https://github.com/pydantic/pydantic](https://github.com/pydantic/pydantic) |
| `pydantic-core` | `2.27.2` | MIT | [https://github.com/pydantic/pydantic-core](https://github.com/pydantic/pydantic-core) |
| `pytest` | `8.3.4` | MIT | [https://github.com/pytest-dev/pytest](https://github.com/pytest-dev/pytest) |
| `python-multipart` | `0.0.20` | Apache-2.0 | [https://github.com/Kludex/python-multipart](https://github.com/Kludex/python-multipart) |
| `referencing` | `0.36.2` | MIT | [https://github.com/python-jsonschema/referencing](https://github.com/python-jsonschema/referencing) |
| `rpds-py` | `0.22.3` | MIT | [https://github.com/crate-py/rpds](https://github.com/crate-py/rpds) |
| `ruff` | `0.9.6` | MIT | [https://github.com/astral-sh/ruff](https://github.com/astral-sh/ruff) |
| `sniffio` | `1.3.1` | MIT | [https://github.com/python-trio/sniffio](https://github.com/python-trio/sniffio) |
| `starlette` | `0.45.3` | BSD-3-Clause | [https://github.com/encode/starlette](https://github.com/encode/starlette) |
| `sympy` | `1.13.3` | BSD-3-Clause | [https://github.com/sympy/sympy](https://github.com/sympy/sympy) |
| `typing-extensions` | `4.12.2` | Python-2.0 | [https://github.com/python/typing_extensions](https://github.com/python/typing_extensions) |
| `uvicorn` | `0.34.0` | BSD-3-Clause | [https://github.com/encode/uvicorn](https://github.com/encode/uvicorn) |

---

## 2. Web Frontend & Transitive NPM Dependencies

| Package | Version | License | NPM Registry |
|---|---|---|---|
| `@antfu/install-pkg` | `1.1.0` | MIT | [@antfu/install-pkg](https://www.npmjs.com/package/@antfu/install-pkg) |
| `@babel/code-frame` | `7.29.7` | MIT | [@babel/code-frame](https://www.npmjs.com/package/@babel/code-frame) |
| `@babel/compat-data` | `7.29.7` | MIT | [@babel/compat-data](https://www.npmjs.com/package/@babel/compat-data) |
| `@babel/core` | `7.29.7` | MIT | [@babel/core](https://www.npmjs.com/package/@babel/core) |
| `@babel/generator` | `7.29.7` | MIT | [@babel/generator](https://www.npmjs.com/package/@babel/generator) |
| `@babel/helper-compilation-targets` | `7.29.7` | MIT | [@babel/helper-compilation-targets](https://www.npmjs.com/package/@babel/helper-compilation-targets) |
| `@babel/helper-globals` | `7.29.7` | MIT | [@babel/helper-globals](https://www.npmjs.com/package/@babel/helper-globals) |
| `@babel/helper-module-imports` | `7.29.7` | MIT | [@babel/helper-module-imports](https://www.npmjs.com/package/@babel/helper-module-imports) |
| `@babel/helper-module-transforms` | `7.29.7` | MIT | [@babel/helper-module-transforms](https://www.npmjs.com/package/@babel/helper-module-transforms) |
| `@babel/helper-plugin-utils` | `7.29.7` | MIT | [@babel/helper-plugin-utils](https://www.npmjs.com/package/@babel/helper-plugin-utils) |
| `@babel/helper-string-parser` | `7.29.7` | MIT | [@babel/helper-string-parser](https://www.npmjs.com/package/@babel/helper-string-parser) |
| `@babel/helper-validator-identifier` | `7.29.7` | MIT | [@babel/helper-validator-identifier](https://www.npmjs.com/package/@babel/helper-validator-identifier) |
| `@babel/helper-validator-option` | `7.29.7` | MIT | [@babel/helper-validator-option](https://www.npmjs.com/package/@babel/helper-validator-option) |
| `@babel/helpers` | `7.29.7` | MIT | [@babel/helpers](https://www.npmjs.com/package/@babel/helpers) |
| `@babel/parser` | `7.29.7` | MIT | [@babel/parser](https://www.npmjs.com/package/@babel/parser) |
| `@babel/plugin-transform-react-jsx-self` | `7.29.7` | MIT | [@babel/plugin-transform-react-jsx-self](https://www.npmjs.com/package/@babel/plugin-transform-react-jsx-self) |
| `@babel/plugin-transform-react-jsx-source` | `7.29.7` | MIT | [@babel/plugin-transform-react-jsx-source](https://www.npmjs.com/package/@babel/plugin-transform-react-jsx-source) |
| `@babel/runtime` | `7.29.7` | MIT | [@babel/runtime](https://www.npmjs.com/package/@babel/runtime) |
| `@babel/template` | `7.29.7` | MIT | [@babel/template](https://www.npmjs.com/package/@babel/template) |
| `@babel/traverse` | `7.29.7` | MIT | [@babel/traverse](https://www.npmjs.com/package/@babel/traverse) |
| `@babel/types` | `7.29.7` | MIT | [@babel/types](https://www.npmjs.com/package/@babel/types) |
| `@braintree/sanitize-url` | `6.0.2` | MIT | [@braintree/sanitize-url](https://www.npmjs.com/package/@braintree/sanitize-url) |
| `@chevrotain/cst-dts-gen` | `11.0.3` | Apache-2.0 | [@chevrotain/cst-dts-gen](https://www.npmjs.com/package/@chevrotain/cst-dts-gen) |
| `@chevrotain/gast` | `11.0.3` | Apache-2.0 | [@chevrotain/gast](https://www.npmjs.com/package/@chevrotain/gast) |
| `@chevrotain/regexp-to-ast` | `11.0.3` | Apache-2.0 | [@chevrotain/regexp-to-ast](https://www.npmjs.com/package/@chevrotain/regexp-to-ast) |
| `@chevrotain/types` | `11.0.3` | Apache-2.0 | [@chevrotain/types](https://www.npmjs.com/package/@chevrotain/types) |
| `@chevrotain/utils` | `11.0.3` | Apache-2.0 | [@chevrotain/utils](https://www.npmjs.com/package/@chevrotain/utils) |
| `@esbuild/aix-ppc64` | `0.25.12` | MIT | [@esbuild/aix-ppc64](https://www.npmjs.com/package/@esbuild/aix-ppc64) |
| `@esbuild/android-arm` | `0.25.12` | MIT | [@esbuild/android-arm](https://www.npmjs.com/package/@esbuild/android-arm) |
| `@esbuild/android-arm64` | `0.25.12` | MIT | [@esbuild/android-arm64](https://www.npmjs.com/package/@esbuild/android-arm64) |
| `@esbuild/android-x64` | `0.25.12` | MIT | [@esbuild/android-x64](https://www.npmjs.com/package/@esbuild/android-x64) |
| `@esbuild/darwin-arm64` | `0.25.12` | MIT | [@esbuild/darwin-arm64](https://www.npmjs.com/package/@esbuild/darwin-arm64) |
| `@esbuild/darwin-x64` | `0.25.12` | MIT | [@esbuild/darwin-x64](https://www.npmjs.com/package/@esbuild/darwin-x64) |
| `@esbuild/freebsd-arm64` | `0.25.12` | MIT | [@esbuild/freebsd-arm64](https://www.npmjs.com/package/@esbuild/freebsd-arm64) |
| `@esbuild/freebsd-x64` | `0.25.12` | MIT | [@esbuild/freebsd-x64](https://www.npmjs.com/package/@esbuild/freebsd-x64) |
| `@esbuild/linux-arm` | `0.25.12` | MIT | [@esbuild/linux-arm](https://www.npmjs.com/package/@esbuild/linux-arm) |
| `@esbuild/linux-arm64` | `0.25.12` | MIT | [@esbuild/linux-arm64](https://www.npmjs.com/package/@esbuild/linux-arm64) |
| `@esbuild/linux-ia32` | `0.25.12` | MIT | [@esbuild/linux-ia32](https://www.npmjs.com/package/@esbuild/linux-ia32) |
| `@esbuild/linux-loong64` | `0.25.12` | MIT | [@esbuild/linux-loong64](https://www.npmjs.com/package/@esbuild/linux-loong64) |
| `@esbuild/linux-mips64el` | `0.25.12` | MIT | [@esbuild/linux-mips64el](https://www.npmjs.com/package/@esbuild/linux-mips64el) |
| `@esbuild/linux-ppc64` | `0.25.12` | MIT | [@esbuild/linux-ppc64](https://www.npmjs.com/package/@esbuild/linux-ppc64) |
| `@esbuild/linux-riscv64` | `0.25.12` | MIT | [@esbuild/linux-riscv64](https://www.npmjs.com/package/@esbuild/linux-riscv64) |
| `@esbuild/linux-s390x` | `0.25.12` | MIT | [@esbuild/linux-s390x](https://www.npmjs.com/package/@esbuild/linux-s390x) |
| `@esbuild/linux-x64` | `0.25.12` | MIT | [@esbuild/linux-x64](https://www.npmjs.com/package/@esbuild/linux-x64) |
| `@esbuild/netbsd-arm64` | `0.25.12` | MIT | [@esbuild/netbsd-arm64](https://www.npmjs.com/package/@esbuild/netbsd-arm64) |
| `@esbuild/netbsd-x64` | `0.25.12` | MIT | [@esbuild/netbsd-x64](https://www.npmjs.com/package/@esbuild/netbsd-x64) |
| `@esbuild/openbsd-arm64` | `0.25.12` | MIT | [@esbuild/openbsd-arm64](https://www.npmjs.com/package/@esbuild/openbsd-arm64) |
| `@esbuild/openbsd-x64` | `0.25.12` | MIT | [@esbuild/openbsd-x64](https://www.npmjs.com/package/@esbuild/openbsd-x64) |
| `@esbuild/openharmony-arm64` | `0.25.12` | MIT | [@esbuild/openharmony-arm64](https://www.npmjs.com/package/@esbuild/openharmony-arm64) |
| `@esbuild/sunos-x64` | `0.25.12` | MIT | [@esbuild/sunos-x64](https://www.npmjs.com/package/@esbuild/sunos-x64) |
| `@esbuild/win32-arm64` | `0.25.12` | MIT | [@esbuild/win32-arm64](https://www.npmjs.com/package/@esbuild/win32-arm64) |
| `@esbuild/win32-ia32` | `0.25.12` | MIT | [@esbuild/win32-ia32](https://www.npmjs.com/package/@esbuild/win32-ia32) |
| `@esbuild/win32-x64` | `0.25.12` | MIT | [@esbuild/win32-x64](https://www.npmjs.com/package/@esbuild/win32-x64) |
| `@excalidraw/excalidraw` | `0.18.1` | MIT | [@excalidraw/excalidraw](https://www.npmjs.com/package/@excalidraw/excalidraw) |
| `@excalidraw/excalidraw/@radix-ui/primitive` | `1.0.0` | MIT | [@excalidraw/excalidraw/@radix-ui/primitive](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/primitive) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs` | `1.0.2` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-context` | `1.0.0` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-context](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-context) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-direction` | `1.0.0` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-direction](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-direction) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-id` | `1.0.0` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-id](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-id) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-id/@radix-ui/react-use-layout-effect` | `1.0.0` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-id/@radix-ui/react-use-layout-effect](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-id/@radix-ui/react-use-layout-effect) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-presence` | `1.0.0` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-presence](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-presence) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-presence/@radix-ui/react-compose-refs` | `1.0.0` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-presence/@radix-ui/react-compose-refs](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-presence/@radix-ui/react-compose-refs) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-presence/@radix-ui/react-use-layout-effect` | `1.0.0` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-presence/@radix-ui/react-use-layout-effect](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-presence/@radix-ui/react-use-layout-effect) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-primitive` | `1.0.1` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-primitive](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-primitive) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-primitive/@radix-ui/react-slot` | `1.0.1` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-primitive/@radix-ui/react-slot](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-primitive/@radix-ui/react-slot) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-primitive/@radix-ui/react-slot/@radix-ui/react-compose-refs` | `1.0.0` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-primitive/@radix-ui/react-slot/@radix-ui/react-compose-refs](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-primitive/@radix-ui/react-slot/@radix-ui/react-compose-refs) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-roving-focus` | `1.0.2` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-roving-focus](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-roving-focus) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-roving-focus/@radix-ui/react-collection` | `1.0.1` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-roving-focus/@radix-ui/react-collection](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-roving-focus/@radix-ui/react-collection) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-roving-focus/@radix-ui/react-collection/@radix-ui/react-slot` | `1.0.1` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-roving-focus/@radix-ui/react-collection/@radix-ui/react-slot](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-roving-focus/@radix-ui/react-collection/@radix-ui/react-slot) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-roving-focus/@radix-ui/react-compose-refs` | `1.0.0` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-roving-focus/@radix-ui/react-compose-refs](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-roving-focus/@radix-ui/react-compose-refs) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-roving-focus/@radix-ui/react-use-callback-ref` | `1.0.0` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-roving-focus/@radix-ui/react-use-callback-ref](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-roving-focus/@radix-ui/react-use-callback-ref) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-use-controllable-state` | `1.0.0` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-use-controllable-state](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-use-controllable-state) |
| `@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-use-controllable-state/@radix-ui/react-use-callback-ref` | `1.0.0` | MIT | [@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-use-controllable-state/@radix-ui/react-use-callback-ref](https://www.npmjs.com/package/@excalidraw/excalidraw/@radix-ui/react-tabs/@radix-ui/react-use-controllable-state/@radix-ui/react-use-callback-ref) |
| `@excalidraw/laser-pointer` | `1.3.1` | MIT | [@excalidraw/laser-pointer](https://www.npmjs.com/package/@excalidraw/laser-pointer) |
| `@excalidraw/markdown-to-text` | `0.1.2` | MIT | [@excalidraw/markdown-to-text](https://www.npmjs.com/package/@excalidraw/markdown-to-text) |
| `@excalidraw/mermaid-to-excalidraw` | `2.2.2` | MIT | [@excalidraw/mermaid-to-excalidraw](https://www.npmjs.com/package/@excalidraw/mermaid-to-excalidraw) |
| `@excalidraw/mermaid-to-excalidraw/nanoid` | `5.1.16` | MIT | [@excalidraw/mermaid-to-excalidraw/nanoid](https://www.npmjs.com/package/@excalidraw/mermaid-to-excalidraw/nanoid) |
| `@excalidraw/random-username` | `1.1.0` | MIT | [@excalidraw/random-username](https://www.npmjs.com/package/@excalidraw/random-username) |
| `@floating-ui/core` | `1.8.0` | MIT | [@floating-ui/core](https://www.npmjs.com/package/@floating-ui/core) |
| `@floating-ui/dom` | `1.8.0` | MIT | [@floating-ui/dom](https://www.npmjs.com/package/@floating-ui/dom) |
| `@floating-ui/react-dom` | `2.1.9` | MIT | [@floating-ui/react-dom](https://www.npmjs.com/package/@floating-ui/react-dom) |
| `@floating-ui/utils` | `0.2.12` | MIT | [@floating-ui/utils](https://www.npmjs.com/package/@floating-ui/utils) |
| `@iconify/types` | `2.0.0` | MIT | [@iconify/types](https://www.npmjs.com/package/@iconify/types) |
| `@iconify/utils` | `3.1.4` | MIT | [@iconify/utils](https://www.npmjs.com/package/@iconify/utils) |
| `@jridgewell/gen-mapping` | `0.3.13` | MIT | [@jridgewell/gen-mapping](https://www.npmjs.com/package/@jridgewell/gen-mapping) |
| `@jridgewell/remapping` | `2.3.5` | MIT | [@jridgewell/remapping](https://www.npmjs.com/package/@jridgewell/remapping) |
| `@jridgewell/resolve-uri` | `3.1.2` | MIT | [@jridgewell/resolve-uri](https://www.npmjs.com/package/@jridgewell/resolve-uri) |
| `@jridgewell/sourcemap-codec` | `1.5.5` | MIT | [@jridgewell/sourcemap-codec](https://www.npmjs.com/package/@jridgewell/sourcemap-codec) |
| `@jridgewell/trace-mapping` | `0.3.31` | MIT | [@jridgewell/trace-mapping](https://www.npmjs.com/package/@jridgewell/trace-mapping) |
| `@mermaid-js/parser` | `0.6.3` | MIT | [@mermaid-js/parser](https://www.npmjs.com/package/@mermaid-js/parser) |
| `@radix-ui/primitive` | `1.1.1` | MIT | [@radix-ui/primitive](https://www.npmjs.com/package/@radix-ui/primitive) |
| `@radix-ui/react-arrow` | `1.1.2` | MIT | [@radix-ui/react-arrow](https://www.npmjs.com/package/@radix-ui/react-arrow) |
| `@radix-ui/react-compose-refs` | `1.1.1` | MIT | [@radix-ui/react-compose-refs](https://www.npmjs.com/package/@radix-ui/react-compose-refs) |
| `@radix-ui/react-context` | `1.1.1` | MIT | [@radix-ui/react-context](https://www.npmjs.com/package/@radix-ui/react-context) |
| `@radix-ui/react-dismissable-layer` | `1.1.5` | MIT | [@radix-ui/react-dismissable-layer](https://www.npmjs.com/package/@radix-ui/react-dismissable-layer) |
| `@radix-ui/react-focus-guards` | `1.1.1` | MIT | [@radix-ui/react-focus-guards](https://www.npmjs.com/package/@radix-ui/react-focus-guards) |
| `@radix-ui/react-focus-scope` | `1.1.2` | MIT | [@radix-ui/react-focus-scope](https://www.npmjs.com/package/@radix-ui/react-focus-scope) |
| `@radix-ui/react-id` | `1.1.0` | MIT | [@radix-ui/react-id](https://www.npmjs.com/package/@radix-ui/react-id) |
| `@radix-ui/react-popover` | `1.1.6` | MIT | [@radix-ui/react-popover](https://www.npmjs.com/package/@radix-ui/react-popover) |
| `@radix-ui/react-popper` | `1.2.2` | MIT | [@radix-ui/react-popper](https://www.npmjs.com/package/@radix-ui/react-popper) |
| `@radix-ui/react-portal` | `1.1.4` | MIT | [@radix-ui/react-portal](https://www.npmjs.com/package/@radix-ui/react-portal) |
| `@radix-ui/react-presence` | `1.1.2` | MIT | [@radix-ui/react-presence](https://www.npmjs.com/package/@radix-ui/react-presence) |
| `@radix-ui/react-primitive` | `2.0.2` | MIT | [@radix-ui/react-primitive](https://www.npmjs.com/package/@radix-ui/react-primitive) |
| `@radix-ui/react-slot` | `1.1.2` | MIT | [@radix-ui/react-slot](https://www.npmjs.com/package/@radix-ui/react-slot) |
| `@radix-ui/react-use-callback-ref` | `1.1.0` | MIT | [@radix-ui/react-use-callback-ref](https://www.npmjs.com/package/@radix-ui/react-use-callback-ref) |
| `@radix-ui/react-use-controllable-state` | `1.1.0` | MIT | [@radix-ui/react-use-controllable-state](https://www.npmjs.com/package/@radix-ui/react-use-controllable-state) |
| `@radix-ui/react-use-escape-keydown` | `1.1.0` | MIT | [@radix-ui/react-use-escape-keydown](https://www.npmjs.com/package/@radix-ui/react-use-escape-keydown) |
| `@radix-ui/react-use-layout-effect` | `1.1.0` | MIT | [@radix-ui/react-use-layout-effect](https://www.npmjs.com/package/@radix-ui/react-use-layout-effect) |
| `@radix-ui/react-use-rect` | `1.1.0` | MIT | [@radix-ui/react-use-rect](https://www.npmjs.com/package/@radix-ui/react-use-rect) |
| `@radix-ui/react-use-size` | `1.1.0` | MIT | [@radix-ui/react-use-size](https://www.npmjs.com/package/@radix-ui/react-use-size) |
| `@radix-ui/rect` | `1.1.0` | MIT | [@radix-ui/rect](https://www.npmjs.com/package/@radix-ui/rect) |
| `@rolldown/pluginutils` | `1.0.0-beta.27` | MIT | [@rolldown/pluginutils](https://www.npmjs.com/package/@rolldown/pluginutils) |
| `@rollup/rollup-android-arm-eabi` | `4.62.3` | MIT | [@rollup/rollup-android-arm-eabi](https://www.npmjs.com/package/@rollup/rollup-android-arm-eabi) |
| `@rollup/rollup-android-arm64` | `4.62.3` | MIT | [@rollup/rollup-android-arm64](https://www.npmjs.com/package/@rollup/rollup-android-arm64) |
| `@rollup/rollup-darwin-arm64` | `4.62.3` | MIT | [@rollup/rollup-darwin-arm64](https://www.npmjs.com/package/@rollup/rollup-darwin-arm64) |
| `@rollup/rollup-darwin-x64` | `4.62.3` | MIT | [@rollup/rollup-darwin-x64](https://www.npmjs.com/package/@rollup/rollup-darwin-x64) |
| `@rollup/rollup-freebsd-arm64` | `4.62.3` | MIT | [@rollup/rollup-freebsd-arm64](https://www.npmjs.com/package/@rollup/rollup-freebsd-arm64) |
| `@rollup/rollup-freebsd-x64` | `4.62.3` | MIT | [@rollup/rollup-freebsd-x64](https://www.npmjs.com/package/@rollup/rollup-freebsd-x64) |
| `@rollup/rollup-linux-arm-gnueabihf` | `4.62.3` | MIT | [@rollup/rollup-linux-arm-gnueabihf](https://www.npmjs.com/package/@rollup/rollup-linux-arm-gnueabihf) |
| `@rollup/rollup-linux-arm-musleabihf` | `4.62.3` | MIT | [@rollup/rollup-linux-arm-musleabihf](https://www.npmjs.com/package/@rollup/rollup-linux-arm-musleabihf) |
| `@rollup/rollup-linux-arm64-gnu` | `4.62.3` | MIT | [@rollup/rollup-linux-arm64-gnu](https://www.npmjs.com/package/@rollup/rollup-linux-arm64-gnu) |
| `@rollup/rollup-linux-arm64-musl` | `4.62.3` | MIT | [@rollup/rollup-linux-arm64-musl](https://www.npmjs.com/package/@rollup/rollup-linux-arm64-musl) |
| `@rollup/rollup-linux-loong64-gnu` | `4.62.3` | MIT | [@rollup/rollup-linux-loong64-gnu](https://www.npmjs.com/package/@rollup/rollup-linux-loong64-gnu) |
| `@rollup/rollup-linux-loong64-musl` | `4.62.3` | MIT | [@rollup/rollup-linux-loong64-musl](https://www.npmjs.com/package/@rollup/rollup-linux-loong64-musl) |
| `@rollup/rollup-linux-ppc64-gnu` | `4.62.3` | MIT | [@rollup/rollup-linux-ppc64-gnu](https://www.npmjs.com/package/@rollup/rollup-linux-ppc64-gnu) |
| `@rollup/rollup-linux-ppc64-musl` | `4.62.3` | MIT | [@rollup/rollup-linux-ppc64-musl](https://www.npmjs.com/package/@rollup/rollup-linux-ppc64-musl) |
| `@rollup/rollup-linux-riscv64-gnu` | `4.62.3` | MIT | [@rollup/rollup-linux-riscv64-gnu](https://www.npmjs.com/package/@rollup/rollup-linux-riscv64-gnu) |
| `@rollup/rollup-linux-riscv64-musl` | `4.62.3` | MIT | [@rollup/rollup-linux-riscv64-musl](https://www.npmjs.com/package/@rollup/rollup-linux-riscv64-musl) |
| `@rollup/rollup-linux-s390x-gnu` | `4.62.3` | MIT | [@rollup/rollup-linux-s390x-gnu](https://www.npmjs.com/package/@rollup/rollup-linux-s390x-gnu) |
| `@rollup/rollup-linux-x64-gnu` | `4.62.3` | MIT | [@rollup/rollup-linux-x64-gnu](https://www.npmjs.com/package/@rollup/rollup-linux-x64-gnu) |
| `@rollup/rollup-linux-x64-musl` | `4.62.3` | MIT | [@rollup/rollup-linux-x64-musl](https://www.npmjs.com/package/@rollup/rollup-linux-x64-musl) |
| `@rollup/rollup-openbsd-x64` | `4.62.3` | MIT | [@rollup/rollup-openbsd-x64](https://www.npmjs.com/package/@rollup/rollup-openbsd-x64) |
| `@rollup/rollup-openharmony-arm64` | `4.62.3` | MIT | [@rollup/rollup-openharmony-arm64](https://www.npmjs.com/package/@rollup/rollup-openharmony-arm64) |
| `@rollup/rollup-win32-arm64-msvc` | `4.62.3` | MIT | [@rollup/rollup-win32-arm64-msvc](https://www.npmjs.com/package/@rollup/rollup-win32-arm64-msvc) |
| `@rollup/rollup-win32-ia32-msvc` | `4.62.3` | MIT | [@rollup/rollup-win32-ia32-msvc](https://www.npmjs.com/package/@rollup/rollup-win32-ia32-msvc) |
| `@rollup/rollup-win32-x64-gnu` | `4.62.3` | MIT | [@rollup/rollup-win32-x64-gnu](https://www.npmjs.com/package/@rollup/rollup-win32-x64-gnu) |
| `@rollup/rollup-win32-x64-msvc` | `4.62.3` | MIT | [@rollup/rollup-win32-x64-msvc](https://www.npmjs.com/package/@rollup/rollup-win32-x64-msvc) |
| `@types/babel__core` | `7.20.5` | MIT | [@types/babel__core](https://www.npmjs.com/package/@types/babel__core) |
| `@types/babel__generator` | `7.27.0` | MIT | [@types/babel__generator](https://www.npmjs.com/package/@types/babel__generator) |
| `@types/babel__template` | `7.4.4` | MIT | [@types/babel__template](https://www.npmjs.com/package/@types/babel__template) |
| `@types/babel__traverse` | `7.28.0` | MIT | [@types/babel__traverse](https://www.npmjs.com/package/@types/babel__traverse) |
| `@types/d3` | `7.4.3` | MIT | [@types/d3](https://www.npmjs.com/package/@types/d3) |
| `@types/d3-array` | `3.2.2` | MIT | [@types/d3-array](https://www.npmjs.com/package/@types/d3-array) |
| `@types/d3-axis` | `3.0.6` | MIT | [@types/d3-axis](https://www.npmjs.com/package/@types/d3-axis) |
| `@types/d3-brush` | `3.0.6` | MIT | [@types/d3-brush](https://www.npmjs.com/package/@types/d3-brush) |
| `@types/d3-chord` | `3.0.6` | MIT | [@types/d3-chord](https://www.npmjs.com/package/@types/d3-chord) |
| `@types/d3-color` | `3.1.3` | MIT | [@types/d3-color](https://www.npmjs.com/package/@types/d3-color) |
| `@types/d3-contour` | `3.0.6` | MIT | [@types/d3-contour](https://www.npmjs.com/package/@types/d3-contour) |
| `@types/d3-delaunay` | `6.0.4` | MIT | [@types/d3-delaunay](https://www.npmjs.com/package/@types/d3-delaunay) |
| `@types/d3-dispatch` | `3.0.7` | MIT | [@types/d3-dispatch](https://www.npmjs.com/package/@types/d3-dispatch) |
| `@types/d3-drag` | `3.0.7` | MIT | [@types/d3-drag](https://www.npmjs.com/package/@types/d3-drag) |
| `@types/d3-dsv` | `3.0.7` | MIT | [@types/d3-dsv](https://www.npmjs.com/package/@types/d3-dsv) |
| `@types/d3-ease` | `3.0.2` | MIT | [@types/d3-ease](https://www.npmjs.com/package/@types/d3-ease) |
| `@types/d3-fetch` | `3.0.7` | MIT | [@types/d3-fetch](https://www.npmjs.com/package/@types/d3-fetch) |
| `@types/d3-force` | `3.0.10` | MIT | [@types/d3-force](https://www.npmjs.com/package/@types/d3-force) |
| `@types/d3-format` | `3.0.4` | MIT | [@types/d3-format](https://www.npmjs.com/package/@types/d3-format) |
| `@types/d3-geo` | `3.1.0` | MIT | [@types/d3-geo](https://www.npmjs.com/package/@types/d3-geo) |
| `@types/d3-hierarchy` | `3.1.7` | MIT | [@types/d3-hierarchy](https://www.npmjs.com/package/@types/d3-hierarchy) |
| `@types/d3-interpolate` | `3.0.4` | MIT | [@types/d3-interpolate](https://www.npmjs.com/package/@types/d3-interpolate) |
| `@types/d3-path` | `3.1.1` | MIT | [@types/d3-path](https://www.npmjs.com/package/@types/d3-path) |
| `@types/d3-polygon` | `3.0.2` | MIT | [@types/d3-polygon](https://www.npmjs.com/package/@types/d3-polygon) |
| `@types/d3-quadtree` | `3.0.6` | MIT | [@types/d3-quadtree](https://www.npmjs.com/package/@types/d3-quadtree) |
| `@types/d3-random` | `3.0.4` | MIT | [@types/d3-random](https://www.npmjs.com/package/@types/d3-random) |
| `@types/d3-scale` | `4.0.9` | MIT | [@types/d3-scale](https://www.npmjs.com/package/@types/d3-scale) |
| `@types/d3-scale-chromatic` | `3.1.0` | MIT | [@types/d3-scale-chromatic](https://www.npmjs.com/package/@types/d3-scale-chromatic) |
| `@types/d3-selection` | `3.0.11` | MIT | [@types/d3-selection](https://www.npmjs.com/package/@types/d3-selection) |
| `@types/d3-shape` | `3.1.8` | MIT | [@types/d3-shape](https://www.npmjs.com/package/@types/d3-shape) |
| `@types/d3-time` | `3.0.4` | MIT | [@types/d3-time](https://www.npmjs.com/package/@types/d3-time) |
| `@types/d3-time-format` | `4.0.3` | MIT | [@types/d3-time-format](https://www.npmjs.com/package/@types/d3-time-format) |
| `@types/d3-timer` | `3.0.2` | MIT | [@types/d3-timer](https://www.npmjs.com/package/@types/d3-timer) |
| `@types/d3-transition` | `3.0.9` | MIT | [@types/d3-transition](https://www.npmjs.com/package/@types/d3-transition) |
| `@types/d3-zoom` | `3.0.8` | MIT | [@types/d3-zoom](https://www.npmjs.com/package/@types/d3-zoom) |
| `@types/estree` | `1.0.9` | MIT | [@types/estree](https://www.npmjs.com/package/@types/estree) |
| `@types/geojson` | `7946.0.16` | MIT | [@types/geojson](https://www.npmjs.com/package/@types/geojson) |
| `@types/prop-types` | `15.7.15` | MIT | [@types/prop-types](https://www.npmjs.com/package/@types/prop-types) |
| `@types/react` | `18.3.31` | MIT | [@types/react](https://www.npmjs.com/package/@types/react) |
| `@types/react-dom` | `18.3.7` | MIT | [@types/react-dom](https://www.npmjs.com/package/@types/react-dom) |
| `@types/trusted-types` | `2.0.7` | MIT | [@types/trusted-types](https://www.npmjs.com/package/@types/trusted-types) |
| `@upsetjs/venn.js` | `2.0.0` | MIT | [@upsetjs/venn.js](https://www.npmjs.com/package/@upsetjs/venn.js) |
| `@vitejs/plugin-react` | `4.7.0` | MIT | [@vitejs/plugin-react](https://www.npmjs.com/package/@vitejs/plugin-react) |
| `@xyflow/react` | `12.11.2` | MIT | [@xyflow/react](https://www.npmjs.com/package/@xyflow/react) |
| `@xyflow/system` | `0.0.79` | MIT | [@xyflow/system](https://www.npmjs.com/package/@xyflow/system) |
| `anymatch` | `3.1.3` | ISC | [anymatch](https://www.npmjs.com/package/anymatch) |
| `aria-hidden` | `1.2.6` | MIT | [aria-hidden](https://www.npmjs.com/package/aria-hidden) |
| `baseline-browser-mapping` | `2.11.7` | Apache-2.0 | [baseline-browser-mapping](https://www.npmjs.com/package/baseline-browser-mapping) |
| `binary-extensions` | `2.3.0` | MIT | [binary-extensions](https://www.npmjs.com/package/binary-extensions) |
| `braces` | `3.0.3` | MIT | [braces](https://www.npmjs.com/package/braces) |
| `browser-fs-access` | `0.29.1` | Apache-2.0 | [browser-fs-access](https://www.npmjs.com/package/browser-fs-access) |
| `browserslist` | `4.28.7` | MIT | [browserslist](https://www.npmjs.com/package/browserslist) |
| `caniuse-lite` | `1.0.30001806` | CC-BY-4.0 | [caniuse-lite](https://www.npmjs.com/package/caniuse-lite) |
| `canvas-roundrect-polyfill` | `0.0.1` | MIT | [canvas-roundrect-polyfill](https://www.npmjs.com/package/canvas-roundrect-polyfill) |
| `chevrotain` | `11.0.3` | Apache-2.0 | [chevrotain](https://www.npmjs.com/package/chevrotain) |
| `chevrotain-allstar` | `0.3.1` | MIT | [chevrotain-allstar](https://www.npmjs.com/package/chevrotain-allstar) |
| `chokidar` | `3.6.0` | MIT | [chokidar](https://www.npmjs.com/package/chokidar) |
| `classcat` | `5.0.5` | MIT | [classcat](https://www.npmjs.com/package/classcat) |
| `clsx` | `1.1.1` | MIT | [clsx](https://www.npmjs.com/package/clsx) |
| `commander` | `8.3.0` | MIT | [commander](https://www.npmjs.com/package/commander) |
| `convert-source-map` | `2.0.0` | MIT | [convert-source-map](https://www.npmjs.com/package/convert-source-map) |
| `cose-base` | `1.0.3` | MIT | [cose-base](https://www.npmjs.com/package/cose-base) |
| `crc-32` | `0.3.0` | Apache-2.0 | [crc-32](https://www.npmjs.com/package/crc-32) |
| `cross-env` | `7.0.3` | MIT | [cross-env](https://www.npmjs.com/package/cross-env) |
| `cross-spawn` | `7.0.6` | MIT | [cross-spawn](https://www.npmjs.com/package/cross-spawn) |
| `csstype` | `3.2.3` | MIT | [csstype](https://www.npmjs.com/package/csstype) |
| `cytoscape` | `3.34.0` | MIT | [cytoscape](https://www.npmjs.com/package/cytoscape) |
| `cytoscape-cose-bilkent` | `4.1.0` | MIT | [cytoscape-cose-bilkent](https://www.npmjs.com/package/cytoscape-cose-bilkent) |
| `cytoscape-fcose` | `2.2.0` | MIT | [cytoscape-fcose](https://www.npmjs.com/package/cytoscape-fcose) |
| `cytoscape-fcose/cose-base` | `2.2.0` | MIT | [cytoscape-fcose/cose-base](https://www.npmjs.com/package/cytoscape-fcose/cose-base) |
| `cytoscape-fcose/layout-base` | `2.0.1` | MIT | [cytoscape-fcose/layout-base](https://www.npmjs.com/package/cytoscape-fcose/layout-base) |
| `d3` | `7.9.0` | ISC | [d3](https://www.npmjs.com/package/d3) |
| `d3-array` | `3.2.4` | ISC | [d3-array](https://www.npmjs.com/package/d3-array) |
| `d3-axis` | `3.0.0` | ISC | [d3-axis](https://www.npmjs.com/package/d3-axis) |
| `d3-brush` | `3.0.0` | ISC | [d3-brush](https://www.npmjs.com/package/d3-brush) |
| `d3-chord` | `3.0.1` | ISC | [d3-chord](https://www.npmjs.com/package/d3-chord) |
| `d3-color` | `3.1.0` | ISC | [d3-color](https://www.npmjs.com/package/d3-color) |
| `d3-contour` | `4.0.2` | ISC | [d3-contour](https://www.npmjs.com/package/d3-contour) |
| `d3-delaunay` | `6.0.4` | ISC | [d3-delaunay](https://www.npmjs.com/package/d3-delaunay) |
| `d3-dispatch` | `3.0.1` | ISC | [d3-dispatch](https://www.npmjs.com/package/d3-dispatch) |
| `d3-drag` | `3.0.0` | ISC | [d3-drag](https://www.npmjs.com/package/d3-drag) |
| `d3-dsv` | `3.0.1` | ISC | [d3-dsv](https://www.npmjs.com/package/d3-dsv) |
| `d3-dsv/commander` | `7.2.0` | MIT | [d3-dsv/commander](https://www.npmjs.com/package/d3-dsv/commander) |
| `d3-ease` | `3.0.1` | BSD-3-Clause | [d3-ease](https://www.npmjs.com/package/d3-ease) |
| `d3-fetch` | `3.0.1` | ISC | [d3-fetch](https://www.npmjs.com/package/d3-fetch) |
| `d3-force` | `3.0.0` | ISC | [d3-force](https://www.npmjs.com/package/d3-force) |
| `d3-format` | `3.1.2` | ISC | [d3-format](https://www.npmjs.com/package/d3-format) |
| `d3-geo` | `3.1.1` | ISC | [d3-geo](https://www.npmjs.com/package/d3-geo) |
| `d3-hierarchy` | `3.1.2` | ISC | [d3-hierarchy](https://www.npmjs.com/package/d3-hierarchy) |
| `d3-interpolate` | `3.0.1` | ISC | [d3-interpolate](https://www.npmjs.com/package/d3-interpolate) |
| `d3-path` | `3.1.0` | ISC | [d3-path](https://www.npmjs.com/package/d3-path) |
| `d3-polygon` | `3.0.1` | ISC | [d3-polygon](https://www.npmjs.com/package/d3-polygon) |
| `d3-quadtree` | `3.0.1` | ISC | [d3-quadtree](https://www.npmjs.com/package/d3-quadtree) |
| `d3-random` | `3.0.1` | ISC | [d3-random](https://www.npmjs.com/package/d3-random) |
| `d3-sankey` | `0.12.3` | BSD-3-Clause | [d3-sankey](https://www.npmjs.com/package/d3-sankey) |
| `d3-sankey/d3-array` | `2.12.1` | BSD-3-Clause | [d3-sankey/d3-array](https://www.npmjs.com/package/d3-sankey/d3-array) |
| `d3-sankey/d3-path` | `1.0.9` | BSD-3-Clause | [d3-sankey/d3-path](https://www.npmjs.com/package/d3-sankey/d3-path) |
| `d3-sankey/d3-shape` | `1.3.7` | BSD-3-Clause | [d3-sankey/d3-shape](https://www.npmjs.com/package/d3-sankey/d3-shape) |
| `d3-sankey/internmap` | `1.0.1` | ISC | [d3-sankey/internmap](https://www.npmjs.com/package/d3-sankey/internmap) |
| `d3-scale` | `4.0.2` | ISC | [d3-scale](https://www.npmjs.com/package/d3-scale) |
| `d3-scale-chromatic` | `3.1.0` | ISC | [d3-scale-chromatic](https://www.npmjs.com/package/d3-scale-chromatic) |
| `d3-selection` | `3.0.0` | ISC | [d3-selection](https://www.npmjs.com/package/d3-selection) |
| `d3-shape` | `3.2.0` | ISC | [d3-shape](https://www.npmjs.com/package/d3-shape) |
| `d3-time` | `3.1.0` | ISC | [d3-time](https://www.npmjs.com/package/d3-time) |
| `d3-time-format` | `4.1.0` | ISC | [d3-time-format](https://www.npmjs.com/package/d3-time-format) |
| `d3-timer` | `3.0.1` | ISC | [d3-timer](https://www.npmjs.com/package/d3-timer) |
| `d3-transition` | `3.0.1` | ISC | [d3-transition](https://www.npmjs.com/package/d3-transition) |
| `d3-zoom` | `3.0.0` | ISC | [d3-zoom](https://www.npmjs.com/package/d3-zoom) |
| `dagre-d3-es` | `7.0.14` | MIT | [dagre-d3-es](https://www.npmjs.com/package/dagre-d3-es) |
| `dayjs` | `1.11.21` | MIT | [dayjs](https://www.npmjs.com/package/dayjs) |
| `debug` | `4.4.3` | MIT | [debug](https://www.npmjs.com/package/debug) |
| `delaunator` | `5.1.0` | ISC | [delaunator](https://www.npmjs.com/package/delaunator) |
| `detect-node-es` | `1.1.0` | MIT | [detect-node-es](https://www.npmjs.com/package/detect-node-es) |
| `dompurify` | `3.4.14` | (MPL-2.0 OR Apache-2.0) | [dompurify](https://www.npmjs.com/package/dompurify) |
| `electron-to-chromium` | `1.5.398` | ISC | [electron-to-chromium](https://www.npmjs.com/package/electron-to-chromium) |
| `es-toolkit` | `1.50.0` | MIT | [es-toolkit](https://www.npmjs.com/package/es-toolkit) |
| `es6-promise-pool` | `2.5.0` | MIT | [es6-promise-pool](https://www.npmjs.com/package/es6-promise-pool) |
| `esbuild` | `0.25.12` | MIT | [esbuild](https://www.npmjs.com/package/esbuild) |
| `escalade` | `3.2.0` | MIT | [escalade](https://www.npmjs.com/package/escalade) |
| `fastdom` | `1.0.12` | MIT | [fastdom](https://www.npmjs.com/package/fastdom) |
| `fill-range` | `7.1.1` | MIT | [fill-range](https://www.npmjs.com/package/fill-range) |
| `fractional-indexing` | `3.2.0` | CC0-1.0 | [fractional-indexing](https://www.npmjs.com/package/fractional-indexing) |
| `fsevents` | `2.3.3` | MIT | [fsevents](https://www.npmjs.com/package/fsevents) |
| `fuzzy` | `0.1.3` | MIT | [fuzzy](https://www.npmjs.com/package/fuzzy) |
| `gensync` | `1.0.0-beta.2` | MIT | [gensync](https://www.npmjs.com/package/gensync) |
| `get-nonce` | `1.0.1` | MIT | [get-nonce](https://www.npmjs.com/package/get-nonce) |
| `glob-parent` | `5.1.2` | ISC | [glob-parent](https://www.npmjs.com/package/glob-parent) |
| `glur` | `1.1.2` | MIT | [glur](https://www.npmjs.com/package/glur) |
| `hachure-fill` | `0.5.2` | MIT | [hachure-fill](https://www.npmjs.com/package/hachure-fill) |
| `iconv-lite` | `0.6.3` | MIT | [iconv-lite](https://www.npmjs.com/package/iconv-lite) |
| `image-blob-reduce` | `3.0.1` | MIT | [image-blob-reduce](https://www.npmjs.com/package/image-blob-reduce) |
| `immutable` | `4.3.9` | MIT | [immutable](https://www.npmjs.com/package/immutable) |
| `import-meta-resolve` | `4.2.0` | MIT | [import-meta-resolve](https://www.npmjs.com/package/import-meta-resolve) |
| `inherits` | `2.0.4` | ISC | [inherits](https://www.npmjs.com/package/inherits) |
| `internmap` | `2.0.3` | ISC | [internmap](https://www.npmjs.com/package/internmap) |
| `is-binary-path` | `2.1.0` | MIT | [is-binary-path](https://www.npmjs.com/package/is-binary-path) |
| `is-extglob` | `2.1.1` | MIT | [is-extglob](https://www.npmjs.com/package/is-extglob) |
| `is-glob` | `4.0.3` | MIT | [is-glob](https://www.npmjs.com/package/is-glob) |
| `is-number` | `7.0.0` | MIT | [is-number](https://www.npmjs.com/package/is-number) |
| `isexe` | `2.0.0` | ISC | [isexe](https://www.npmjs.com/package/isexe) |
| `jotai` | `2.11.0` | MIT | [jotai](https://www.npmjs.com/package/jotai) |
| `jotai-scope` | `0.7.2` | MIT | [jotai-scope](https://www.npmjs.com/package/jotai-scope) |
| `js-tokens` | `4.0.0` | MIT | [js-tokens](https://www.npmjs.com/package/js-tokens) |
| `jsesc` | `3.1.0` | MIT | [jsesc](https://www.npmjs.com/package/jsesc) |
| `json5` | `2.2.3` | MIT | [json5](https://www.npmjs.com/package/json5) |
| `katex` | `0.16.47` | MIT | [katex](https://www.npmjs.com/package/katex) |
| `khroma` | `2.1.0` | MIT | [khroma](https://www.npmjs.com/package/khroma) |
| `langium` | `3.3.1` | MIT | [langium](https://www.npmjs.com/package/langium) |
| `layout-base` | `1.0.2` | MIT | [layout-base](https://www.npmjs.com/package/layout-base) |
| `lodash-es` | `4.18.1` | MIT | [lodash-es](https://www.npmjs.com/package/lodash-es) |
| `lodash.debounce` | `4.0.8` | MIT | [lodash.debounce](https://www.npmjs.com/package/lodash.debounce) |
| `lodash.throttle` | `4.1.1` | MIT | [lodash.throttle](https://www.npmjs.com/package/lodash.throttle) |
| `loose-envify` | `1.4.0` | MIT | [loose-envify](https://www.npmjs.com/package/loose-envify) |
| `lru-cache` | `5.1.1` | ISC | [lru-cache](https://www.npmjs.com/package/lru-cache) |
| `marked` | `16.4.2` | MIT | [marked](https://www.npmjs.com/package/marked) |
| `mermaid` | `11.17.0` | MIT | [mermaid](https://www.npmjs.com/package/mermaid) |
| `mermaid/@braintree/sanitize-url` | `7.1.2` | MIT | [mermaid/@braintree/sanitize-url](https://www.npmjs.com/package/mermaid/@braintree/sanitize-url) |
| `mermaid/@chevrotain/types` | `11.1.2` | Apache-2.0 | [mermaid/@chevrotain/types](https://www.npmjs.com/package/mermaid/@chevrotain/types) |
| `mermaid/@mermaid-js/parser` | `1.2.1` | MIT | [mermaid/@mermaid-js/parser](https://www.npmjs.com/package/mermaid/@mermaid-js/parser) |
| `mermaid/points-on-curve` | `0.2.0` | MIT | [mermaid/points-on-curve](https://www.npmjs.com/package/mermaid/points-on-curve) |
| `mermaid/roughjs` | `4.6.6` | MIT | [mermaid/roughjs](https://www.npmjs.com/package/mermaid/roughjs) |
| `ms` | `2.1.3` | MIT | [ms](https://www.npmjs.com/package/ms) |
| `multimath` | `2.0.0` | MIT | [multimath](https://www.npmjs.com/package/multimath) |
| `nanoid` | `3.3.18` | MIT | [nanoid](https://www.npmjs.com/package/nanoid) |
| `node-releases` | `2.0.51` | MIT | [node-releases](https://www.npmjs.com/package/node-releases) |
| `normalize-path` | `3.0.0` | MIT | [normalize-path](https://www.npmjs.com/package/normalize-path) |
| `object-assign` | `4.1.1` | MIT | [object-assign](https://www.npmjs.com/package/object-assign) |
| `open-color` | `1.9.1` | MIT | [open-color](https://www.npmjs.com/package/open-color) |
| `package-manager-detector` | `1.8.0` | MIT | [package-manager-detector](https://www.npmjs.com/package/package-manager-detector) |
| `pako` | `2.0.3` | (MIT AND Zlib) | [pako](https://www.npmjs.com/package/pako) |
| `path-data-parser` | `0.1.0` | MIT | [path-data-parser](https://www.npmjs.com/package/path-data-parser) |
| `path-key` | `3.1.1` | MIT | [path-key](https://www.npmjs.com/package/path-key) |
| `perfect-freehand` | `1.2.0` | MIT | [perfect-freehand](https://www.npmjs.com/package/perfect-freehand) |
| `pica` | `7.1.1` | MIT | [pica](https://www.npmjs.com/package/pica) |
| `picocolors` | `1.1.1` | ISC | [picocolors](https://www.npmjs.com/package/picocolors) |
| `picomatch` | `2.3.2` | MIT | [picomatch](https://www.npmjs.com/package/picomatch) |
| `png-chunk-text` | `1.0.0` | MIT | [png-chunk-text](https://www.npmjs.com/package/png-chunk-text) |
| `png-chunks-encode` | `1.0.0` | MIT | [png-chunks-encode](https://www.npmjs.com/package/png-chunks-encode) |
| `png-chunks-extract` | `1.0.0` | MIT | [png-chunks-extract](https://www.npmjs.com/package/png-chunks-extract) |
| `points-on-curve` | `1.0.1` | MIT | [points-on-curve](https://www.npmjs.com/package/points-on-curve) |
| `points-on-path` | `0.2.1` | MIT | [points-on-path](https://www.npmjs.com/package/points-on-path) |
| `points-on-path/points-on-curve` | `0.2.0` | MIT | [points-on-path/points-on-curve](https://www.npmjs.com/package/points-on-path/points-on-curve) |
| `postcss` | `8.5.25` | MIT | [postcss](https://www.npmjs.com/package/postcss) |
| `pwacompat` | `2.0.17` | Apache-2.0 | [pwacompat](https://www.npmjs.com/package/pwacompat) |
| `react` | `18.3.1` | MIT | [react](https://www.npmjs.com/package/react) |
| `react-dom` | `18.3.1` | MIT | [react-dom](https://www.npmjs.com/package/react-dom) |
| `react-refresh` | `0.17.0` | MIT | [react-refresh](https://www.npmjs.com/package/react-refresh) |
| `react-remove-scroll` | `2.7.2` | MIT | [react-remove-scroll](https://www.npmjs.com/package/react-remove-scroll) |
| `react-remove-scroll-bar` | `2.3.8` | MIT | [react-remove-scroll-bar](https://www.npmjs.com/package/react-remove-scroll-bar) |
| `react-style-singleton` | `2.2.3` | MIT | [react-style-singleton](https://www.npmjs.com/package/react-style-singleton) |
| `readdirp` | `3.6.0` | MIT | [readdirp](https://www.npmjs.com/package/readdirp) |
| `robust-predicates` | `3.0.3` | Unlicense | [robust-predicates](https://www.npmjs.com/package/robust-predicates) |
| `rollup` | `4.62.3` | MIT | [rollup](https://www.npmjs.com/package/rollup) |
| `roughjs` | `4.6.4` | MIT | [roughjs](https://www.npmjs.com/package/roughjs) |
| `roughjs/points-on-curve` | `0.2.0` | MIT | [roughjs/points-on-curve](https://www.npmjs.com/package/roughjs/points-on-curve) |
| `rw` | `1.3.3` | BSD-3-Clause | [rw](https://www.npmjs.com/package/rw) |
| `safer-buffer` | `2.1.2` | MIT | [safer-buffer](https://www.npmjs.com/package/safer-buffer) |
| `sass` | `1.51.0` | MIT | [sass](https://www.npmjs.com/package/sass) |
| `scheduler` | `0.23.2` | MIT | [scheduler](https://www.npmjs.com/package/scheduler) |
| `semver` | `6.3.1` | ISC | [semver](https://www.npmjs.com/package/semver) |
| `shebang-command` | `2.0.0` | MIT | [shebang-command](https://www.npmjs.com/package/shebang-command) |
| `shebang-regex` | `3.0.0` | MIT | [shebang-regex](https://www.npmjs.com/package/shebang-regex) |
| `sliced` | `1.0.1` | MIT | [sliced](https://www.npmjs.com/package/sliced) |
| `source-map-js` | `1.2.1` | BSD-3-Clause | [source-map-js](https://www.npmjs.com/package/source-map-js) |
| `strictdom` | `1.0.1` | MIT | [strictdom](https://www.npmjs.com/package/strictdom) |
| `stylis` | `4.4.0` | MIT | [stylis](https://www.npmjs.com/package/stylis) |
| `tinyexec` | `1.2.4` | MIT | [tinyexec](https://www.npmjs.com/package/tinyexec) |
| `tinyglobby` | `0.2.17` | MIT | [tinyglobby](https://www.npmjs.com/package/tinyglobby) |
| `tinyglobby/fdir` | `6.5.0` | MIT | [tinyglobby/fdir](https://www.npmjs.com/package/tinyglobby/fdir) |
| `tinyglobby/picomatch` | `4.0.5` | MIT | [tinyglobby/picomatch](https://www.npmjs.com/package/tinyglobby/picomatch) |
| `to-regex-range` | `5.0.1` | MIT | [to-regex-range](https://www.npmjs.com/package/to-regex-range) |
| `ts-dedent` | `2.3.0` | MIT | [ts-dedent](https://www.npmjs.com/package/ts-dedent) |
| `tslib` | `2.8.1` | 0BSD | [tslib](https://www.npmjs.com/package/tslib) |
| `tunnel-rat` | `0.1.2` | MIT | [tunnel-rat](https://www.npmjs.com/package/tunnel-rat) |
| `typescript` | `5.9.3` | Apache-2.0 | [typescript](https://www.npmjs.com/package/typescript) |
| `update-browserslist-db` | `1.2.3` | MIT | [update-browserslist-db](https://www.npmjs.com/package/update-browserslist-db) |
| `use-callback-ref` | `1.3.3` | MIT | [use-callback-ref](https://www.npmjs.com/package/use-callback-ref) |
| `use-sidecar` | `1.1.3` | MIT | [use-sidecar](https://www.npmjs.com/package/use-sidecar) |
| `use-sync-external-store` | `1.6.0` | MIT | [use-sync-external-store](https://www.npmjs.com/package/use-sync-external-store) |
| `uuid` | `14.0.1` | MIT | [uuid](https://www.npmjs.com/package/uuid) |
| `vite` | `6.4.3` | MIT | [vite](https://www.npmjs.com/package/vite) |
| `vite/fdir` | `6.5.0` | MIT | [vite/fdir](https://www.npmjs.com/package/vite/fdir) |
| `vite/picomatch` | `4.0.5` | MIT | [vite/picomatch](https://www.npmjs.com/package/vite/picomatch) |
| `vscode-jsonrpc` | `8.2.0` | MIT | [vscode-jsonrpc](https://www.npmjs.com/package/vscode-jsonrpc) |
| `vscode-languageserver` | `9.0.1` | MIT | [vscode-languageserver](https://www.npmjs.com/package/vscode-languageserver) |
| `vscode-languageserver-protocol` | `3.17.5` | MIT | [vscode-languageserver-protocol](https://www.npmjs.com/package/vscode-languageserver-protocol) |
| `vscode-languageserver-textdocument` | `1.0.12` | MIT | [vscode-languageserver-textdocument](https://www.npmjs.com/package/vscode-languageserver-textdocument) |
| `vscode-languageserver-types` | `3.17.5` | MIT | [vscode-languageserver-types](https://www.npmjs.com/package/vscode-languageserver-types) |
| `vscode-uri` | `3.0.8` | MIT | [vscode-uri](https://www.npmjs.com/package/vscode-uri) |
| `webworkify` | `1.5.0` | MIT | [webworkify](https://www.npmjs.com/package/webworkify) |
| `which` | `2.0.2` | ISC | [which](https://www.npmjs.com/package/which) |
| `yallist` | `3.1.1` | ISC | [yallist](https://www.npmjs.com/package/yallist) |
| `zustand` | `4.5.7` | MIT | [zustand](https://www.npmjs.com/package/zustand) |

---

## 3. Standard Permissive License Texts

### Apache License, Version 2.0
```text
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
```

### MIT License
```text
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.
```

### BSD 3-Clause License
```text
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the conditions of source copyright retention are met.
```

### Mozilla Public License Version 2.0 (MPL-2.0)
```text
This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
```

### ISC License
```text
Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted.
```

