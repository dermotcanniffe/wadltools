import json
import os

# Path to your full WADL-style JSON file
INPUT_FILE = "wadl_full.json"
OUTPUT_DIR = "wadl_chunks"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the large WADL JSON
with open(INPUT_FILE, "r", encoding="utf-8") as infile:
    full_data = json.load(infile)

# Split and write each top-level resource to a separate file
for resource_name, resource_data in full_data.items():
    # Safe filename: replace spaces and slashes
    safe_name = resource_name.replace(" ", "_").replace("/", "_")
    output_path = os.path.join(OUTPUT_DIR, f"{safe_name}.json")
    
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump({resource_name: resource_data}, outfile, indent=2)

    print(f"Saved: {output_path}")
