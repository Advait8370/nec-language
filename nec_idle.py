import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import tempfile
import os
import sys


# ===============================
# NEC IDLE — MODERN EDITOR
# ===============================
class NECIdle:
    def __init__(self, root):
        self.root = root
        self.root.title("NEC IDLE")
        self.root.geometry("1000x650")
        self.root.configure(bg="#0f111a")

        self.build_ui()

    def build_ui(self):
        # ===== TOP BAR =====
        top = tk.Frame(self.root, bg="#0f111a", height=48)
        top.pack(fill=tk.X)

        title = tk.Label(
            top,
            text="NEC IDLE",
            fg="#e6edf3",
            bg="#0f111a",
            font=("Segoe UI", 14, "bold")
        )
        title.pack(side=tk.LEFT, padx=20)

        run_btn = tk.Button(
            top,
            text="▶ Run",
            command=self.run_in_console,
            bg="#4cc2ff",
            fg="#000",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=16,
            pady=6,
            cursor="hand2",
            activebackground="#63d0ff"
        )
        run_btn.pack(side=tk.RIGHT, padx=20)

        # ===== CARD CONTAINER =====
        card = tk.Frame(
            self.root,
            bg="#161a2b",
            bd=0
        )
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # ===== EDITOR HEADER =====
        header = tk.Frame(card, bg="#161a2b")
        header.pack(fill=tk.X, pady=(10, 5))

        tk.Label(
            header,
            text="Editor",
            fg="#4cc2ff",
            bg="#161a2b",
            font=("Segoe UI", 11, "bold")
        ).pack(side=tk.LEFT, padx=14)

        open_btn = tk.Button(
            header,
            text="Open",
            command=self.open_file,
            bg="#161a2b",
            fg="#e6edf3",
            bd=0,
            cursor="hand2"
        )
        open_btn.pack(side=tk.RIGHT, padx=10)

        save_btn = tk.Button(
            header,
            text="Save",
            command=self.save_file,
            bg="#161a2b",
            fg="#e6edf3",
            bd=0,
            cursor="hand2"
        )
        save_btn.pack(side=tk.RIGHT)

        # ===== EDITOR =====
        self.editor = tk.Text(
            card,
            bg="#0b0e17",
            fg="#e6edf3",
            insertbackground="#4cc2ff",
            font=("Consolas", 12),
            undo=True,
            bd=0,
            padx=16,
            pady=16
        )
        self.editor.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        # Default content
        self.editor.insert(
            "1.0",
            'print "Welcome to NEC"\n'
        )

    # ===============================
    # FILE OPS
    # ===============================
    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("NEC Files", "*.nec")]
        )
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.editor.delete("1.0", tk.END)
                self.editor.insert(tk.END, f.read())

    def save_file(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".nec",
            filetypes=[("NEC Files", "*.nec")]
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.get("1.0", tk.END))

    # ===============================
    # RUN IN NEC CONSOLE
    # ===============================
    def run_in_console(self):
        code = self.editor.get("1.0", tk.END)

        tmp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".nec",
            mode="w",
            encoding="utf-8"
        )
        tmp.write(code)
        tmp.close()

        python = sys.executable
        console_path = os.path.join(
            os.path.dirname(__file__),
            "nec_console.py"
        )

        try:
            subprocess.Popen(
                [python, console_path, tmp.name],
                cwd=os.path.dirname(__file__)
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))


# ===============================
# APP ENTRY
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    NECIdle(root)
    root.mainloop()
