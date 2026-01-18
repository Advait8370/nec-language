import json, os

REGISTRY = {
    "ai": {"version": "0.1.0", "desc": "AI utilities"},
    "math": {"version": "0.1.0", "desc": "Math utilities"}
}

REG_PATH = os.path.expanduser("~/.nec/registry.json")

def load_registry():
    os.makedirs(os.path.dirname(REG_PATH), exist_ok=True)
    if not os.path.exists(REG_PATH):
        with open(REG_PATH, "w") as f:
            json.dump(REGISTRY, f, indent=2)
    with open(REG_PATH) as f:
        return json.load(f)
