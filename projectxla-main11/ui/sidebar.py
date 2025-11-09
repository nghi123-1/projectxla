import tkinter as tk

def create_sidebar(root):
    frame = tk.Frame(root, bg="#E3F2FD", width=250)
    tk.Label(frame, text="Menu chức năng", bg="#1565C0", fg="white",
             font=("Arial", 14, "bold"), pady=10).pack(fill="x")
    return frame
