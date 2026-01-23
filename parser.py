from ast_nodes import *
from errors import NECError

def parse(tokens):
    pos = 0
    ast = []

    def consume(t):
        nonlocal pos
        if pos >= len(tokens):
            raise NECError("Unexpected end of file", tokens[-1][2])
        if tokens[pos][0] != t:
            raise NECError(f"Expected {t}", tokens[pos][2])
        val = tokens[pos][1]
        pos += 1
        return val

    while pos < len(tokens):
        t, v, l = tokens[pos]

        if t == "LET":
            pos += 1
            name = consume("IDENT")
            consume("OP")
            value = consume(tokens[pos][0])
            ast.append(Let(name, value, l))

        elif t == "PRINT":
            pos += 1
            value = consume(tokens[pos][0])
            ast.append(Print(value, l))

        elif t == "DATA":
            pos += 1
            name = consume("IDENT")
            consume("FROM")
            src = consume("STRING")
            ast.append(Data(name, src.strip('"'), l))

        elif t == "MODEL":
            pos += 1
            name = consume("IDENT")
            consume("TYPE")
            model_type = consume("IDENT")
            ast.append(Model(name, model_type, l))

        elif t == "TRAIN":
            pos += 1
            model = consume("IDENT")
            consume("USING")
            dataset = consume("IDENT")
            ast.append(Train(model, dataset, l))

        elif t == "USE":
            pos += 1
            pkg = consume("IDENT")
            ast.append(Use(pkg, l))

        elif t == "IF":
            pos += 1
            left = consume("IDENT")
            op = tokens[pos][1]; pos += 1
            right = consume(tokens[pos][0])
            consume("COLON")

            body = []
            else_body = []

            if tokens[pos][0] == "PRINT":
                pos += 1
                body.append(Print(consume(tokens[pos][0]), l))

            if pos < len(tokens) and tokens[pos][0] == "ELSE":
                pos += 1
                consume("COLON")
                if tokens[pos][0] == "PRINT":
                    pos += 1
                    else_body.append(Print(consume(tokens[pos][0]), l))

            ast.append(If(left, op, right, body, else_body, l))

        else:
            raise NECError(f"Unexpected token '{v}'", l)

    return ast
