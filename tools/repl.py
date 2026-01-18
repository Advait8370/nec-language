from lexer import lex
from parser import parse
from interpreter import NECInterpreter
from errors import NECError

def start_repl():
    print("NEC REPL v0.7 — type 'exit' to quit")
    interp = NECInterpreter()

    while True:
        try:
            line = input(">>> ")
            if line == "exit":
                break

            tokens = lex(line + "\n")
            ast = parse(tokens)
            interp.run(ast)

        except NECError as e:
            print(e)
        except KeyboardInterrupt:
            break
