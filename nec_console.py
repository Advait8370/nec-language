import tkinter as tk
from tkinter import scrolledtext
import sys

from lexer import lex
from parser import parse
from interpreter import NECInterpreter
from errors import NECError


# ==================================
# NEC CONSOLE — WINDOWS TERMINAL UI
# ==================================
class NECConsole:
    def __init__(self, root, file_to_run=None):
        self.root = root
        self.root.title("NEC Console")
        self.root.geometry("820x480")
        self.root.configure(bg="#0c0c0c")

        self.interpreter = NECInterpreter()
        self.build_ui()

        if file_to_run:
            self.run_file(file_to_run)

    def build_ui(self):
        # Terminal text area
        self.console = scrolledtext.ScrolledText(
            self.root,
            font=("Cascadia Mono", 12),
            bg="#0c0c0c",
            fg="#d4d4d4",
            insertbackground="#4cc2ff",
            bd=0,
            padx=14,
            pady=14
        )
        self.console.pack(fill=tk.BOTH, expand=True)

        # Tags for colored output
        self.console.tag_config("prompt", foreground="#4cc2ff")
        self.console.tag_config("output", foreground="#9cdcfe")
        self.console.tag_config("error", foreground="#f44747")
        self.console.tag_config("banner", foreground="#6a9955")

        # Banner
        self.console.insert(
            tk.END,
            "NEC Console v0.8.0\nType NEC code below\n\n",
            "banner"
        )
        self.show_prompt()

        self.console.bind("<Return>", self.on_enter)
        self.console.focus()

    # ===============================
    # PROMPT
    # ===============================
    def show_prompt(self):
        self.console.insert(tk.END, ">>> ", "prompt")
        self.console.see(tk.END)

    # ===============================
    # RUN FILE FROM IDLE
    # ===============================
    def run_file(self, filename):
        self.console.insert(
            tk.END,
            f"\n[Running {filename}]\n",
            "banner"
        )

        from io import StringIO
        old_stdout = sys.stdout
        buffer = StringIO()
        sys.stdout = buffer

        try:
            with open(filename, "r", encoding="utf-8") as f:
                code = f.read()

            ast = parse(lex(code))
            self.interpreter = NECInterpreter()
            self.interpreter.run(ast)

        except NECError as e:
            print(e)

        except Exception as e:
            print(f"[Internal Error] {e}")

        finally:
            sys.stdout = old_stdout
            self.console.insert(tk.END, buffer.getvalue(), "output")
            self.show_prompt()

    # ===============================
    # REPL INPUT
    # ===============================
    def on_enter(self, event):
        start = self.console.search(
            ">>>", "end-1c", backwards=True
        )
        command = self.console.get(
            start + "+4c", "end-1c"
        ).strip()

        self.console.insert(tk.END, "\n")

        if command == "":
            self.show_prompt()
            return "break"

        from io import StringIO
        old_stdout = sys.stdout
        buffer = StringIO()
        sys.stdout = buffer

        try:
            ast = parse(lex(command + "\n"))
            self.interpreter.run(ast)

        except NECError as e:
            buffer.write(str(e) + "\n")

        except Exception as e:
            buffer.write(f"[Internal Error] {e}\n")

        finally:
            sys.stdout = old_stdout
            self.console.insert(tk.END, buffer.getvalue(), "output")
            self.show_prompt()

        return "break"


# ===============================
# APP ENTRY
# ===============================
if __name__ == "__main__":
    file_arg = sys.argv[1] if len(sys.argv) > 1 else None

    root = tk.Tk()
    NECConsole(root, file_arg)
    root.mainloop()
