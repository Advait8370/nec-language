import tkinter as tk
from tkinter import scrolledtext

from lexer import lex
from parser import parse
from interpreter import NECInterpreter
from errors import NECError


class NECConsole:
    def __init__(self, root):
        self.root = root
        self.root.title("NEC Console")
        self.root.geometry("700x450")

        self.interpreter = NECInterpreter()
        self.build_ui()

    def build_ui(self):
        self.console = scrolledtext.ScrolledText(
            self.root,
            font=("Consolas", 12),
            bg="#000000",
            fg="#00ff00",
            insertbackground="white"
        )
        self.console.pack(fill=tk.BOTH, expand=True)

        self.console.insert(tk.END, "NEC Console v0.7\n>>> ")
        self.console.bind("<Return>", self.on_enter)
        self.console.focus()

    def on_enter(self, event):
        # Get last command after >>>
        start = self.console.search(">>>", "end-1c", backwards=True)
        command = self.console.get(start + "+4c", "end-1c").strip()

        self.console.insert(tk.END, "\n")

        if command == "":
            self.console.insert(tk.END, ">>> ")
            return "break"

        try:
            tokens = lex(command + "\n")
            ast = parse(tokens)
            self.interpreter.run(ast)

        except NECError as e:
            self.console.insert(tk.END, str(e) + "\n")

        except Exception as e:
            self.console.insert(tk.END, f"[Internal Error] {e}\n")

        self.console.insert(tk.END, ">>> ")
        self.console.see(tk.END)
        return "break"


if __name__ == "__main__":
    root = tk.Tk()
    NECConsole(root)
    root.mainloop()
