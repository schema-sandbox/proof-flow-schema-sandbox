# Third-Party Software Notices and Software Bill of Materials (SBOM)

ProofFlow Schema Sandbox incorporates or depends upon open-source software libraries.
This document provides full attribution, dependency taxonomy, and notices required by the licenses of these third-party packages.

---

## 1. Python Server Runtime Dependencies (Direct & Transitive)

| Package | Version | License | Component / Purpose | Upstream Project |
|---|---|---|---|---|
| **FastAPI** | `>=0.115,<1` | MIT | Core REST API framework | [tiangolo/fastapi](https://github.com/tiangolo/fastapi) |
| **Starlette** | `>=0.38,<1` | BSD-3-Clause | ASGI toolkit under FastAPI | [encode/starlette](https://github.com/encode/starlette) |
| **Uvicorn** | `>=0.30,<1` | BSD-3-Clause | ASGI web server | [encode/uvicorn](https://github.com/encode/uvicorn) |
| **Pydantic** | `>=2.8,<3` | MIT | Data validation & schemas | [pydantic/pydantic](https://github.com/pydantic/pydantic) |
| **pydantic-core** | `>=2.20,<3` | MIT | High-performance C-extensions for Pydantic | [pydantic/pydantic-core](https://github.com/pydantic/pydantic-core) |
| **annotated-types** | `>=0.6,<1` | MIT | Type annotation metadata | [annotated-types/annotated-types](https://github.com/annotated-types/annotated-types) |
| **typing-extensions** | `>=4.12,<5` | Python-2.0 | Type hinting backports | [python/typing_extensions](https://github.com/python/typing_extensions) |
| **python-multipart** | `>=0.0.9,<1` | Apache-2.0 | Streaming multipart/form-data parser | [Kludex/python-multipart](https://github.com/Kludex/python-multipart) |
| **jsonschema** | `>=4.22,<5` | MIT | JSON Schema validation | [python-jsonschema/jsonschema](https://github.com/python-jsonschema/jsonschema) |
| **jsonschema-specifications** | `>=2023.12` | MIT | Schema dialect specifications | [python-jsonschema/jsonschema-specifications](https://github.com/python-jsonschema/jsonschema-specifications) |
| **referencing** | `>=0.35` | MIT | JSON Schema reference resolution | [python-jsonschema/referencing](https://github.com/python-jsonschema/referencing) |
| **rpds-py** | `>=0.18` | MIT | Persistent data structures | [crate-py/rpds](https://github.com/crate-py/rpds) |
| **attrs** | `>=23.2` | MIT | Attribute definition helper | [python-attrs/attrs](https://github.com/python-attrs/attrs) |
| **click** | `>=8.1,<9` | BSD-3-Clause | CLI command line parser | [pallets/click](https://github.com/pallets/click) |
| **h11** | `>=0.14,<1` | MIT | Pure-Python HTTP/1.1 protocol | [python-hyper/h11](https://github.com/python-hyper/h11) |
| **sniffio** | `>=1.3` | Apache-2.0 / MIT | Async library sniffer | [python-trio/sniffio](https://github.com/python-trio/sniffio) |
| **anyio** | `>=4.4,<5` | MIT | Asynchronous networking and concurrency | [agronholm/anyio](https://github.com/agronholm/anyio) |
| **idna** | `>=3.7` | BSD-3-Clause | Internationalized Domain Names in Applications | [kjd/idna](https://github.com/kjd/idna) |
| **certifi** | `>=2024.7` | MPL-2.0 | Mozilla Root Certificates Bundle | [certifi/python-certifi](https://github.com/certifi/python-certifi) |
| **httpx** | `>=0.27,<1` | BSD-3-Clause | Next-generation HTTP client | [encode/httpx](https://github.com/encode/httpx) |
| **httpcore** | `>=1.0,<2` | BSD-3-Clause | Minimal low-level HTTP client | [encode/httpcore](https://github.com/encode/httpcore) |
| **pytest** | `>=8,<10` | MIT | Testing framework | [pytest-dev/pytest](https://github.com/pytest-dev/pytest) |
| **iniconfig** | `>=2.0` | MIT | Brain-dead simple config-ini parsing | [pytest-dev/iniconfig](https://github.com/pytest-dev/iniconfig) |
| **packaging** | `>=24.1` | Apache-2.0 / BSD-2-Clause | Core utilities for Python packages | [pypa/packaging](https://github.com/pypa/packaging) |
| **pluggy** | `>=1.5` | MIT | Plugin mechanism for pytest | [pytest-dev/pluggy](https://github.com/pytest-dev/pluggy) |
| **ruff** | `>=0.8,<1` | MIT / Apache-2.0 | Extremely fast Python linter and formatter | [astral-sh/ruff](https://github.com/astral-sh/ruff) |
| **sympy** | `>=1.12,<2` | BSD-3-Clause | Computer algebra and symbolic mathematics | [sympy/sympy](https://github.com/sympy/sympy) |
| **mpmath** | `>=1.3,<2` | BSD-3-Clause | Real and complex floating-point arithmetic | [mpmath/mpmath](https://github.com/mpmath/mpmath) |

---

## 2. Frontend Web Runtime & Build Dependencies

| Package | Version | License | Component / Purpose | Upstream Project |
|---|---|---|---|---|
| **React** | `^18.3.1` | MIT | UI component framework | [facebook/react](https://github.com/facebook/react) |
| **React-DOM** | `^18.3.1` | MIT | DOM rendering engine for React | [facebook/react](https://github.com/facebook/react) |
| **scheduler** | `^0.23.2` | MIT | Cooperative scheduling for browser | [facebook/react](https://github.com/facebook/react) |
| **@excalidraw/excalidraw** | `^0.18.0` | MIT | Virtual whiteboard and freehand canvas | [excalidraw/excalidraw](https://github.com/excalidraw/excalidraw) |
| **@xyflow/react** | `^12.3.6` | MIT | Node-based workflow and graph canvas | [xyflow/xyflow](https://github.com/xyflow/xyflow) |
| **@xyflow/system** | `^0.0.44` | MIT | Core graph engine for xyflow | [xyflow/xyflow](https://github.com/xyflow/xyflow) |
| **KaTeX** | `^0.16.11` | MIT | Fast math typesetting for the web | [KaTeX/KaTeX](https://github.com/KaTeX/KaTeX) |
| **DOMPurify** | `3.4.14` | Apache-2.0 / MPL-2.0 | DOM-only XSS sanitizer | [cure53/DOMPurify](https://github.com/cure53/DOMPurify) |
| **Mermaid** | `11.17.0` | MIT | Markdown-inspired diagram rendering | [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid) |
| **nanoid** | `3.3.18 / 5.1.16` | MIT | Secure URL-friendly unique ID generator | [ai/nanoid](https://github.com/ai/nanoid) |
| **lodash-es** | `4.18.1` | MIT | Modular utility library | [lodash/lodash](https://github.com/lodash/lodash) |
| **d3** | `^7.9.0` | ISC | Data-driven visualization utilities | [d3/d3](https://github.com/d3/d3) |
| **dagre** | `^0.8.5` | MIT | Directed graph layout engine | [dagrejs/dagre](https://github.com/dagrejs/dagre) |
| **TypeScript** | `^5.7.2` | Apache-2.0 | Static typing toolchain | [microsoft/TypeScript](https://github.com/microsoft/TypeScript) |
| **Vite** | `^6.0.1` | MIT | Next generation frontend tooling | [vitejs/vite](https://github.com/vitejs/vite) |
| **@vitejs/plugin-react** | `^4.3.4` | MIT | Babel/SWC Fast Refresh for React in Vite | [vitejs/vite-plugin-react](https://github.com/vitejs/vite-plugin-react) |

---

## 3. Standard License Texts

### MIT License
```text
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Apache License, Version 2.0
```text
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

### BSD 3-Clause License
```text
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

### Mozilla Public License 2.0 (MPL-2.0)
```text
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
```
