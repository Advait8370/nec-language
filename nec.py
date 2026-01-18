import sys

# Core language
from lexer import lex
from parser import parse
from interpreter import NECInterpreter
from errors import NECError

# Package manager
from pkg.manager import install, list_pkgs

# Tools
from tools.formatter import format_code
from tools.repl import start_repl
from tools.doctor import run_doctor
from tools.checker import check


def run_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()

        tokens = lex(code)
        ast = parse(tokens)

        interpreter = NECInterpreter()
        interpreter.run(ast)

    except FileNotFoundError:
        print(f"[NEC Error] File not found: {filename}")

    except NECError as e:
        print(e)

    except Exception as e:
        print("[NEC Internal Error]", e)


def format_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()

        formatted = format_code(code)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(formatted)

        print("[NEC] File formatted successfully")

    except Exception as e:
        print("[NEC Error]", e)


def check_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()

        ast = parse(lex(code))
        check(ast)

        print("[NEC] No issues found")

    except NECError as e:
        print(e)


def show_help():
    print("""
NEC — Next-gen Code

Usage:
  nec run <file.nec>        Run NEC program
  nec install <package>     Install NEC package
  nec list                  List installed packages
  nec fmt <file.nec>        Format NEC source file
  nec check <file.nec>      Static check (lint)
  nec repl                  Interactive NEC shell
  nec doctor                Check NEC environment
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    cmd = sys.argv[1]

    if cmd == "run" and len(sys.argv) >= 3:
        run_file(sys.argv[2])

    elif cmd == "install" and len(sys.argv) >= 3:
        try:
            install(sys.argv[2])
        except NECError as e:
            print(e)

    elif cmd == "list":
        list_pkgs()

    elif cmd == "fmt" and len(sys.argv) >= 3:
        format_file(sys.argv[2])

    elif cmd == "check" and len(sys.argv) >= 3:
        check_file(sys.argv[2])

    elif cmd == "repl":
        start_repl()

    elif cmd == "doctor":
        run_doctor()

    else:
        show_help()


if __name__ == "__main__":
    main()
