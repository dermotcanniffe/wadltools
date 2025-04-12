import json
import os

INPUT_FILE = "wadl_chunks/resources.json"
OUTPUT_DIR = "resource_chunks"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    all_resources = json.load(f)

for resource_name, resource_obj in all_resources.items():
    safe_name = resource_name.replace(" ", "_").replace("/", "_")
    output_path = os.path.join(OUTPUT_DIR, f"{safe_name}.json")
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump({resource_name: resource_obj}, out, indent=2)
    print(f"Saved: {output_path}")
