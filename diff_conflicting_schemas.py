import yaml
import os
import argparse
from pprint import pprint

def load_schema_from_file(schema_name, filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return data.get("components", {}).get("schemas", {}).get(schema_name)

def main(schema_name, filepaths):
    print(f"\n🔍 Comparing schema: {schema_name}")
    schemas = []

    for path in filepaths:
        print(f"\n📄 From: {os.path.basename(path)}")
        schema = load_schema_from_file(schema_name, path)
        if schema is None:
            print(f"⚠️ Schema not found in {path}")
        else:
            pprint(schema, sort_dicts=False)
            schemas.append(schema)

    if len(schemas) >= 2:
        if schemas[0] == schemas[1]:
            print("\n✅ These schemas are identical. You can safely deduplicate.")
        else:
            print("\n⚠️ Schemas differ! Consider renaming or manually merging.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Diff a schema across multiple OpenAPI YAML fragments.")
    parser.add_argument("schema", help="Schema name (as it appears in components.schemas)")
    parser.add_argument("files", nargs="+", help="YAML files to compare (at least 2)")
    args = parser.parse_args()

    main(args.schema, args.files)
