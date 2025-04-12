import json
import os

INPUT_FILE = "wadl_full.json"
OUTPUT_DIR = "resource_chunks"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    full_data = json.load(f)

# Extract just the resources section
resources = full_data.get("resources", {})

# Split each named resource to a file
for resource_name, resource_data in resources.items():
    safe_name = resource_name.replace(" ", "_").replace("/", "_")
    out_path = os.path.join(OUTPUT_DIR, f"{safe_name}.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({resource_name: resource_data}, f, indent=2)

    print(f"✅ Saved {out_path}")
