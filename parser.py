from ast_nodes import *
from errors import NECError

def parse(tokens):
    pos = 0
    ast = []

    def consume(expected):
        nonlocal pos
        if pos >= len(tokens):
            raise NECError("Unexpected end of file", tokens[-1][2])
        t, v, l = tokens[pos]
        if t != expected:
            raise NECError(f"Expected {expected}, got {t}", l)
        pos += 1
        return v, l

    while pos < len(tokens):
        t, v, l = tokens[pos]

        if t == "LET":
            pos += 1
            name, _ = consume("IDENT")
            consume("OP")
            value, _ = consume(tokens[pos][0])
            ast.append(Let(name, value, l))

        elif t == "PRINT":
            pos += 1
            value, _ = consume(tokens[pos][0])
            ast.append(Print(value, l))

        elif t == "DATA":
            pos += 1
            name, _ = consume("IDENT")
            consume("FROM")
            source, _ = consume("STRING")
            ast.append(Data(name, source.strip('"'), l))

        elif t == "MODEL":
            pos += 1
            name, _ = consume("IDENT")
            consume("TYPE")
            model_type, _ = consume("IDENT")
            ast.append(Model(name, model_type, l))

        elif t == "TRAIN":
            pos += 1
            model, _ = consume("IDENT")
            consume("USING")
            dataset, _ = consume("IDENT")
            ast.append(Train(model, dataset, l))

        elif t == "USE":
            pos += 1
            pkg, _ = consume("IDENT")
            ast.append(Use(pkg, l))

        else:
            raise NECError(f"Unexpected token '{v}'", l)

    return ast
