import tkinter as tk
from tkinter import scrolledtext, filedialog

from lexer import lex
from parser import parse
from interpreter import NECInterpreter
from errors import NECError


class NECIdle:
    def __init__(self, root):
        self.root = root
        self.root.title("NEC IDLE — Next-gen Code")
        self.root.geometry("900x650")

        self.interpreter = NECInterpreter()

        self.build_ui()

    def build_ui(self):
        # ===== MENU =====
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

        # ===== EDITOR =====
        self.editor = scrolledtext.ScrolledText(
            self.root, font=("Consolas", 12), height=18
        )
        self.editor.pack(fill=tk.BOTH, expand=True)

        # ===== RUN BUTTON =====
        run_btn = tk.Button(
            self.root,
            text="▶ Run File",
            bg="#1e1e1e",
            fg="white",
            command=self.run_file
        )
        run_btn.pack(fill=tk.X)

        # ===== CONSOLE LABEL =====
        tk.Label(
            self.root,
            text="NEC Console",
            bg="#111",
            fg="#0f0",
            anchor="w"
        ).pack(fill=tk.X)

        # ===== CONSOLE =====
        self.console = scrolledtext.ScrolledText(
            self.root,
            font=("Consolas", 11),
            height=10,
            bg="#000",
            fg="#0f0",
            insertbackground="white"
        )
        self.console.pack(fill=tk.BOTH)
        self.console.insert(tk.END, "NEC IDLE v0.7\n>>> ")
        self.console.bind("<Return>", self.console_enter)

        # Default editor text
        self.editor.insert(tk.END, 'print "Welcome to NEC IDLE"\n')

    # ===== FILE OPS =====
    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("NEC Files", "*.nec")])
        if path:
            with open(path) as f:
                self.editor.delete("1.0", tk.END)
                self.editor.insert(tk.END, f.read())

    def save_file(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".nec",
            filetypes=[("NEC Files", "*.nec")]
        )
        if path:
            with open(path, "w") as f:
                f.write(self.editor.get("1.0", tk.END))

    # ===== RUN FULL FILE =====
    def run_file(self):
        code = self.editor.get("1.0", tk.END)
        self.console.insert(tk.END, "\n[Running file]\n")

        try:
            ast = parse(lex(code))
            self.interpreter.run(ast)
        except NECError as e:
            self.console.insert(tk.END, str(e) + "\n")

        self.console.insert(tk.END, ">>> ")
        self.console.see(tk.END)

    # ===== CONSOLE REPL =====
    def console_enter(self, event):
        line_start = self.console.search(">>>", "end-1c", backwards=True)
        cmd = self.console.get(line_start + "+4c", "end-1c").strip()

        self.console.insert(tk.END, "\n")

        if cmd == "":
            self.console.insert(tk.END, ">>> ")
            return "break"

        try:
            ast = parse(lex(cmd + "\n"))
            self.interpreter.run(ast)
        except NECError as e:
            self.console.insert(tk.END, str(e) + "\n")

        self.console.insert(tk.END, ">>> ")
        self.console.see(tk.END)
        return "break"


if __name__ == "__main__":
    root = tk.Tk()
    NECIdle(root)
    root.mainloop()
