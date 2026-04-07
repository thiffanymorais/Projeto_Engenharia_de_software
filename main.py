import tkinter as tk
from views.login_view import LoginApp


if __name__ == "__main__":
    root = tk.Tk()

    root.update_idletasks()
    width = 400
    height = 370
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    app = LoginApp(root)
    root.mainloop()