'''
hello and welcome to the custombox module, in this module you can add custom messages
with custom commands and buttons, so your not forced on only "Ok", "Cancel", "Yes", "No"
and the others, you can put it all custom!
'''

import tkinter as tk
import sys
import webbrowser
from tkinter import ttk

class CustomBox:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.default_commands = {
            "exit": self.exit_app,
            "download_tismiy": lambda: webbrowser.open("https://scratch.mit.edu/projects/1103965827/fullscreen/")
        }

    def show_custombox(self, title="Message", message="Something happened!", buttons=None):
        if not buttons or not (1 <= len(buttons) <= 4):
            raise ValueError("You must provide 1 to 4 buttons.")

        self.win = tk.Toplevel(self.root)
        self.win.title(title)
        self.win.resizable(False, False)

        self.win.update_idletasks()
        w, h = 300, 150
        x = (self.win.winfo_screenwidth() - w) // 2
        y = (self.win.winfo_screenheight() - h) // 2
        self.win.geometry(f"{w}x{h}+{x}+{y}")

        tk.Label(self.win, text=message, wraplength=280, justify="center").pack(pady=15, expand=True)

        btn_frame = tk.Frame(self.win)
        btn_frame.pack(side="bottom", pady=10)

        for btn in buttons:
            text = btn.get("text", "Button")
            command = btn.get("command", None)
            after = btn.get("after_command", "exit")

            width = max(10, min(len(text) + 2, 20))
            b = tk.Button(btn_frame, text=text, width=width,
                          command=lambda cmd=command, after_cmd=after: self.run_command(cmd, after_cmd))
            b.pack(side="left", padx=5)

        self.win.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def run_command(self, command, after_command="exit"):
        self.win.destroy()

        if callable(command):
            command()
        elif isinstance(command, str):
            if command in self.default_commands:
                self.default_commands[command]()
            else:
                print(f"Unknown command: {command}")

        # Perform after_command
        if after_command == "exit":
            self.exit_app()
        elif after_command == "close":
            self.root.quit()
        elif after_command == "none":
            pass
        else:
            print(f"Unknown after_command: {after_command}")
            self.exit_app()

    def on_close(self):
        self.win.destroy()

    def exit_app(self):
        self.root.quit()
        sys.exit()

class CustomBoxEnhanced(CustomBox):
    def show_custombox(self, title="Message", message="Something happened!", buttons=None):
        if not buttons or not (1 <= len(buttons) <= 4):
            raise ValueError("You must provide 1 to 4 buttons.")

        self.win = tk.Toplevel(self.root)
        self.win.title(title)
        self.win.resizable(False, False)

        self.win.update_idletasks()
        w, h = 300, 150
        x = (self.win.winfo_screenwidth() - w) // 2
        y = (self.win.winfo_screenheight() - h) // 2
        self.win.geometry(f"{w}x{h}+{x}+{y}")

        ttk.Label(self.win, text=message, wraplength=280, justify="center").pack(pady=15, expand=True)

        btn_frame = ttk.Frame(self.win)
        btn_frame.pack(side="bottom", pady=10)

        for btn in buttons:
            text = btn.get("text", "Button")
            command = btn.get("command", None)
            after = btn.get("after_command", "exit")

            width = max(10, min(len(text) + 2, 20))
            b = ttk.Button(btn_frame, text=text, width=width,
                           command=lambda cmd=command, after_cmd=after: self.run_command(cmd, after_cmd))
            b.pack(side="left", padx=5)

        self.win.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

def show_custombox(title="Message", message="Something happened!", buttons=None, use_enhancer=False):
    if use_enhancer:
        box = CustomBoxEnhanced()
    else:
        box = CustomBox()
    box.show_custombox(title=title, message=message, buttons=buttons)


# Example usage
if __name__ == "__main__":
    def hello_world():
        print("Hello from a custom command!")

    show_custombox(
        title="custombox test",
        message="Choose an option:",
        buttons=[
            {"text": "Say Hello", "command": hello_world, "after_command": "close"},
            {"text": "Download tismiy", "command": "download_tismiy", "after_command": "exit"}
        ],
        use_enhancer=False
    )
