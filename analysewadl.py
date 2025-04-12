import json

INPUT_FILE = "wadl_full.json"  # Replace with your actual filename

def describe(obj, indent=0, depth=0, max_depth=3):
    prefix = "  " * indent
    if isinstance(obj, dict):
        print(f"{prefix}dict with {len(obj)} keys")
        for i, (k, v) in enumerate(obj.items()):
            print(f"{prefix}  key: {repr(k)}")
            if depth < max_depth:
                describe(v, indent + 2, depth + 1)
            if i >= 2:  # only show first 3 keys
                break
    elif isinstance(obj, list):
        print(f"{prefix}list with {len(obj)} items")
        if obj and depth < max_depth:
            describe(obj[0], indent + 1, depth + 1)
    else:
        print(f"{prefix}{type(obj).__name__}: {repr(obj)}")

# Load and analyze
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

print("🔍 Top-level structure of your WADL-JSON:\n")
describe(data)
