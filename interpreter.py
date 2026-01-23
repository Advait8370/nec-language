import csv, os
from errors import NECError

PKG_DIR = os.path.expanduser("~/.nec/packages")

class NECInterpreter:
    def __init__(self):
        self.vars = {}
        self.models = {}
        self.packages = {}

    def run(self, ast):
        for node in ast:
            self.exec(node)

    def exec(self, node):
        n = node.__class__.__name__

        if n == "Let":
            self.vars[node.name] = self.eval(node.value)

        elif n == "Print":
            print(self.eval(node.value))

        elif n == "Data":
            try:
                with open(node.source) as f:
                    self.vars[node.name] = list(csv.DictReader(f))
            except FileNotFoundError:
                raise NECError(f"File not found '{node.source}'", node.line)

        elif n == "Model":
            self.models[node.name] = {"type": node.model_type, "accuracy": None}

        elif n == "Train":
            if node.dataset not in self.vars:
                raise NECError(f"Dataset '{node.dataset}' not found", node.line)
            self.models[node.model]["accuracy"] = 92.5
            print(f"[NEC AI] Trained {node.model}")

        elif n == "Use":
            path = os.path.join(PKG_DIR, node.package)
            if not os.path.exists(path):
                raise NECError(
                    f"Package '{node.package}' not installed",
                    node.line
                )
            print(f"[NEC] Loaded package '{node.package}'")

        elif n == "If":
            left = self.eval(node.left)
            right = self.eval(node.right)
            cond = {
                "==": left == right,
                "!=": left != right,
                "<": left < right,
                ">": left > right,
                "<=": left <= right,
                ">=": left >= right,
            }[node.op]

            for stmt in node.body if cond else node.else_body:
                self.exec(stmt)

    def eval(self, value):
        if value.startswith('"'):
            return value.strip('"')
        if value.isdigit():
            return int(value)
        return self.vars.get(value, value)
