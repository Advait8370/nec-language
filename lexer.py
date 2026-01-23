import re
from errors import NECError

TOKENS = [
    ("IF", r"\bif\b"),
    ("ELSE", r"\belse\b"),
    ("WHILE", r"\bwhile\b"),

    ("EQ", r"=="),
    ("NE", r"!="),
    ("LE", r"<="),
    ("GE", r">="),
    ("LT", r"<"),
    ("GT", r">"),

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

    ("COLON", r":"),
    ("OP", r"="),
    ("IDENT", r"[a-zA-Z_][a-zA-Z0-9_]*"),

    ("NEWLINE", r"\n"),
    ("SKIP", r"[ \t]+"),
]

def lex(code):
    pos = 0
    line = 1
    tokens = []

    while pos < len(code):
        for name, pattern in TOKENS:
            m = re.match(pattern, code[pos:])
            if m:
                text = m.group(0)
                if name == "NEWLINE":
                    line += 1
                elif name != "SKIP":
                    tokens.append((name, text, line))
                pos += len(text)
                break
        else:
            raise NECError(f"Illegal character '{code[pos]}'", line)

    return tokens
