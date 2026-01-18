def format_code(code):
    lines = code.splitlines()
    formatted = []

    for line in lines:
        line = line.strip()
        if line:
            formatted.append(line)

    return "\n".join(formatted) + "\n"
