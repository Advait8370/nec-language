import re
from errors import NECError

TOKENS = [
    ("NUMBER", r"\d+"),
    ("STRING", r'"[^"]*"'),
    ("LET", r"\blet\b"),
    ("PRINT", r"\bprint\b"),
    ("DATA", r"\bdata\b"),
    ("FROM", r"\bfrom\b"),
    ("MODEL", r"\bmodel\b"),
    ("TYPE", r"\btype\b"),
    ("TRAIN", r"\btrain\b"),
    ("USING", r"\busing\b"),
    ("USE", r"\buse\b"),
    ("IDENT", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("OP", r"="),
    ("NEWLINE", r"\n"),
    ("SKIP", r"[ \t]+"),
]

def lex(code):
    pos, line = 0, 1
    tokens = []

    while pos < len(code):
        match = None
        for name, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                text = match.group(0)
                if name == "NEWLINE":
                    line += 1
                elif name != "SKIP":
                    tokens.append((name, text, line))
                pos = match.end()
                break

        if not match:
            raise NECError(f"Illegal character '{code[pos]}'", line)

    return tokens
