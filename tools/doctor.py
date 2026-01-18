import os

def run_doctor():
    print("[NEC Doctor] Checking environment...")

    home = os.path.expanduser("~/.nec")
    if not os.path.exists(home):
        print("✗ NEC home not found")
        print("✓ Will be created on first install")
    else:
        print("✓ NEC home directory found")

    pkg = os.path.join(home, "packages")
    print("✓ Package directory:", pkg)
