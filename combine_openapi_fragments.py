import yaml
import os
import glob
from collections import defaultdict

INPUT_FOLDER = "./openapi_chunks"  # change this if needed
OUTPUT_FILE = "openapi_combined.yaml"

combined_paths = {}
combined_schemas = {}
schema_sources = defaultdict(list)
schema_conflicts = {}

# Step 1: Merge all paths and track schema sources
for file in glob.glob(os.path.join(INPUT_FOLDER, "*_openapi.yaml")):
    with open(file, "r", encoding="utf-8") as f:
        try:
            fragment = yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️ Skipping {file}: {e}")
            continue

    # Merge paths
    for path, methods in fragment.get("paths", {}).items():
        if path not in combined_paths:
            combined_paths[path] = methods
        else:
            for method, op in methods.items():
                if method in combined_paths[path]:
                    print(f"⚠️ Conflict: {method.upper()} {path} already defined. Skipping duplicate.")
                else:
                    combined_paths[path][method] = op

    # Track schemas and their source files
    for name, schema in fragment.get("components", {}).get("schemas", {}).items():
        schema_sources[name].append((file, schema))

# Step 2: Merge schemas and detect true conflicts
for name, entries in schema_sources.items():
    base_file, base_schema = entries[0]
    all_equal = all(s == base_schema for _, s in entries)
    if all_equal:
        combined_schemas[name] = base_schema
    else:
        conflict_files = [f for f, _ in entries]
        schema_conflicts[name] = conflict_files

# Step 3: Write final merged output
final_spec = {
    "openapi": "3.0.3",
    "info": {
        "title": "Combined SpiraTest API",
        "version": "7.0",
        "description": "Automatically combined from WADL-based fragments"
    },
    "paths": combined_paths,
    "components": {
        "schemas": combined_schemas
    }
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    yaml.dump(final_spec, out, sort_keys=False)

print(f"\n✅ Combined OpenAPI spec written to: {OUTPUT_FILE}")

# Step 4: Show conflict summary and diff suggestion
if schema_conflicts:
    print("\n⚠️ Real schema conflicts detected (same name, different definitions):")
    for name, files in schema_conflicts.items():
        print(f"\n🛑 Schema: {name}")
        for f in files:
            print(f"   - {f}")
        print(f"💡 To diff: python diff_conflicting_schemas.py {name} {' '.join(files)}")
else:
    print("🎉 No real schema conflicts found!")

