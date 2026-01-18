def generate(ast):
    lines = [
        "import csv",
        "from runtime.ai import train_model",
    ]

    for node in ast:
        name = node.__class__.__name__

        if name == "Let":
            lines.append(f"{node.name} = {node.value}")

        elif name == "Print":
            lines.append(f"print({node.value})")

        elif name == "Data":
            lines.append(f"{node.name} = []")
            lines.append(f"with open({node.source}, newline='') as f:")
            lines.append(f"    reader = csv.DictReader(f)")
            lines.append(f"    for row in reader:")
            lines.append(f"        {node.name}.append(row)")

        elif name == "Model":
            lines.append(f"{node.name} = None  # model placeholder")

        elif name == "Train":
            lines.append(
                f"{node.model} = train_model('classification', {node.dataset})"
            )

    return "\n".join(lines)
