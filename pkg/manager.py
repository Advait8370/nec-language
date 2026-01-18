import os, json
from pkg.registry import load_registry
from errors import NECError

PKG_DIR = os.path.expanduser("~/.nec/packages")

def install(name):
    registry = load_registry()
    if name not in registry:
        raise NECError(f"Package '{name}' not found", 0)

    os.makedirs(PKG_DIR, exist_ok=True)
    target = os.path.join(PKG_DIR, name)

    if os.path.exists(target):
        print(f"[necpkg] '{name}' already installed")
        return

    os.makedirs(target)
    with open(os.path.join(target, "package.json"), "w") as f:
        json.dump(registry[name], f, indent=2)

    print(f"[necpkg] Installed '{name}'")

def list_pkgs():
    if not os.path.exists(PKG_DIR):
        print("No packages installed")
        return
    for p in os.listdir(PKG_DIR):
        print("-", p)
