import tkinter as tk

def create_result_frame(root):
    frame = tk.Frame(root, bg="white")

    lbl_image = tk.Label(frame, bg="white")
    lbl_image.pack(pady=20)

    lbl_result = tk.Label(frame, text="Kết quả nhận diện sẽ hiển thị tại đây",
                          bg="white", fg="#333", font=("Arial", 12))
    lbl_result.pack(pady=10)

    return frame, lbl_image, lbl_result
