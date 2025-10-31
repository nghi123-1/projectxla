import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk
import cv2
from utils.detect_multi import detect_objects
from utils.preprocess import preprocess_image
from utils.history import save_history, load_history
from model.coin_model import classify_coin
from ui.sidebar import create_sidebar
from ui.result_frame import create_result_frame


def create_main_ui():
    app = tk.Tk()
    app.title("Ứng dụng nhận diện đồng xu")
    app.geometry("1100x750")
    app.config(bg="#f5f5f5")

    frame_sidebar = create_sidebar(app)
    frame_sidebar.pack(side="left", fill="y")

    frame_result, lbl_image, lbl_result = create_result_frame(app)
    frame_result.pack(side="right", fill="both", expand=True)

    # --- Hàm xử lý ---
    def choose_image(single=True):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if not path:
            return
        image = cv2.imread(path)
        processed = preprocess_image(image)

        if single:
            decoded = classify_coin(processed)
            label, conf = decoded[0][1], float(decoded[0][2])
            cv2.putText(processed, f"{label} ({conf*100:.1f}%)", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            results = [{"label": label, "confidence": conf}]
        else:
            processed, results = detect_objects(processed)

        save_history({"file": path, "results": results})

        rgb_img = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
        imgtk = ImageTk.PhotoImage(Image.fromarray(rgb_img))
        lbl_image.config(image=imgtk)
        lbl_image.image = imgtk
        lbl_result.config(text="\n".join([f"{r['label']}: {r['confidence']*100:.1f}%" for r in results]))

    def open_history():
        hist = load_history()
        if not hist:
            messagebox.showinfo("Lịch sử", "Chưa có lịch sử nhận diện nào.")
            return

        win = Toplevel(app)
        win.title(" Lịch sử nhận diện")
        win.geometry("500x400")
        tk.Label(win, text="Lịch sử kết quả nhận diện", font=("Arial", 14, "bold")).pack(pady=10)
        listbox = tk.Listbox(win, width=70, height=20)
        listbox.pack(padx=10, pady=10)

        for item in hist:
            s = f"{item['file'].split('/')[-1]}  →  {', '.join([r['label'] for r in item['results']])}"
            listbox.insert(tk.END, s)

    # --- Nút Sidebar ---
    tk.Button(frame_sidebar, text=" Nhận diện 1 vật thể", width=22, bg="#1976D2", fg="white",
              font=("Arial", 11, "bold"), command=lambda: choose_image(True)).pack(pady=10)

    tk.Button(frame_sidebar, text=" Nhận diện nhiều vật thể", width=22, bg="#43A047", fg="white",
              font=("Arial", 11, "bold"), command=lambda: choose_image(False)).pack(pady=10)

    tk.Button(frame_sidebar, text=" Lịch sử kết quả", width=22, bg="#FB8C00", fg="white",
              font=("Arial", 11, "bold"), command=open_history).pack(pady=10)

    app.mainloop()
