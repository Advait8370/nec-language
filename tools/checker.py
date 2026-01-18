from errors import NECError

def check(ast):
    defined_vars = set()

    for node in ast:
        name = node.__class__.__name__

        if name == "Let":
            defined_vars.add(node.name)

        elif name == "Train":
            if node.dataset not in defined_vars:
                raise NECError(
                    f"Dataset '{node.dataset}' used before declaration",
                    node.line
                )
