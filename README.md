# WADL-to-OpenAPI Conversion Toolkit

This repo contains a set of Python scripts to convert a WADL-style JSON API description into a modern OpenAPI 3.0+ specification, piece by piece — then recombine, validate, and share the result.

---

## 🔧 Scripts Included

### `convert_wadl_chunk_to_oas.py`
Converts a single WADL-style JSON resource into an OpenAPI 3.0 YAML fragment.

**Usage:**
```bash
python convert_wadl_chunk_to_oas.py path/to/resource_chunk.json

# WADL-to-OpenAPI Conversion Toolkit

This project provides a modular, scriptable toolkit for converting a large WADL-style JSON API description (such as the SpiraTest REST API) into a clean, valid OpenAPI 3.0 specification.

It is designed for transparency, collaboration, and minimal interference with the source API structure — preserving naming, casing, and formatting as defined by the original system.

---

## 🔧 Toolkit Overview

This toolkit supports:

- WADL structure inspection
- Chunk-based resource extraction
- Per-resource OpenAPI conversion
- YAML fragment merging
- Conflict detection and schema diffing
- Final OpenAPI spec validation and sharing

---

## 🧰 Scripts Included

### 🟡 1. WADL Analysis & Splitting

#### `analysewadl.py`
Inspect and summarize the structure of a WADL JSON file.

**Usage:**
```bash
python analysewadl.py path/to/full_wadl.json
Outputs top-level shape and per-resource summaries to help guide conversion.

splitresources.py
Splits a WADL JSON file into individual resource chunks (1 JSON file per resource).

Usage:

bash
Copy code
python splitresources.py path/to/full_wadl.json
Outputs individual files to resource_chunks/.

2. Resource Conversion
convert_wadl_chunk_to_oas.py
Converts a single WADL resource chunk (JSON) into an OpenAPI 3.0 YAML fragment.

Usage:

bash
Copy code
python convert_wadl_chunk_to_oas.py resource_chunks/Test_Set.json
Outputs: Test_Set_openapi.yaml in the same folder.

convert.py and old-convert.py
Legacy or experimental versions of the conversion logic. Retained for historical comparison or experimentation.

🔵 3. Merging & Conflict Detection
combine_openapi_fragments.py
Combines all _openapi.yaml fragments into a single valid OpenAPI 3.0 spec.

Usage:

bash
Copy code
python combine_openapi_fragments.py
Merges all paths and components.schemas

Detects real schema conflicts (same name, different definitions)

Outputs: openapi_combined.yaml

Prints ready-to-run diff commands for each conflict

diff_conflicting_schemas.py
Compares one schema name across multiple fragment files.

Usage:

bash
Copy code
python diff_conflicting_schemas.py <schema_name> file1.yaml file2.yaml
Example:

bash
Copy code
python diff_conflicting_schemas.py remoteCustomList \
  openapi_chunks/Custom_List_openapi.yaml \
  openapi_chunks/System_Custom_List_openapi.yaml
Helps you visually compare definitions and decide whether to merge, rename, or preserve both.

✅ Suggested Workflow
Analyze the WADL:

bash
Copy code
python analysewadl.py full_wadl.json
Split into chunks:

bash
Copy code
python splitresources.py full_wadl.json
Convert each chunk to OpenAPI:

bash
Copy code
mkdir -p openapi_chunks
ls resource_chunks/*.json | while read f; do python convert_wadl_chunk_to_oas.py "$f"; done
Merge YAML fragments:

bash
Copy code
python combine_openapi_fragments.py
Compare conflicting schemas (if any):

bash
Copy code
python diff_conflicting_schemas.py <schema_name> fileA.yaml fileB.yaml
Validate final spec:

bash
Copy code
python -m openapi_spec_validator openapi_combined.yaml
Upload to SwaggerHub or preview in Swagger Editor.

📦 Requirements
Install dependencies:

bash
Copy code
pip install pyyaml openapi-spec-validator
Requires Python 3.7+

📤 Output
*_openapi.yaml: Per-resource OpenAPI 3.0 fragments

openapi_combined.yaml: Full OpenAPI 3.0 specification

💡 Notes
All schema names are preserved exactly as in the source WADL

Casing is respected to avoid overstepping API owner decisions

Conflict detection is non-destructive: no automatic merging or renaming is performed

Designed to be safe, auditable, and easy to iterate with

Acknowledgments
Developed to reverse-engineer and modernize the SpiraTest 7.0 WADL API into an OpenAPI 3.0-compliant format, ready for validation, documentation, and code generation.

Built for collaboration with API owners and to respect original schema fidelity.
