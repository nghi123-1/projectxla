import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk
import cv2
import numpy as np 

from utils.preprocess import preprocess_image, rotate_image, convert_to_grayscale, invert_colors 
from utils.detect_multi import detect_objects
from utils.history import save_history, load_history
from model.coin_model import classify_coin
from ui.sidebar import create_sidebar
from ui.result_frame import create_result_frame

current_raw_image = None 
lbl_image_global = None 


def create_main_ui():
   
    global current_raw_image
    global lbl_image_global
    
    app = tk.Tk()
    app.title("Ứng dụng nhận diện đồng xu")
    app.geometry("1100x750")
    app.config(bg="#f5f5f5")

    frame_sidebar = create_sidebar(app)
    frame_sidebar.pack(side="left", fill="y")

    frame_result, lbl_image, lbl_result = create_result_frame(app)
    frame_result.pack(side="right", fill="both", expand=True)
    
    lbl_image_global = lbl_image

   
    def display_image(image):
        """Hiển thị ảnh CV2 lên Label Tkinter và resize vừa khung"""
        if image is None: return
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        h, w = image.shape[:2]
        ratio = min(500 / w, 500 / h) if w > 0 and h > 0 else 1
        new_w, new_h = int(w * ratio), int(h * ratio)
        display_img = cv2.resize(image, (new_w, new_h))
        
        rgb_img = cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB)
        imgtk = ImageTk.PhotoImage(Image.fromarray(rgb_img))
        lbl_image_global.config(image=imgtk)
        lbl_image_global.image = imgtk

    def choose_image(single=True):
        global current_raw_image
        
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if not path: return
        image = cv2.imread(path)
        if image is None:
            messagebox.showerror("Lỗi", "Không thể đọc file ảnh.")
            return
            
     
        current_raw_image = image.copy() 
        
        processed = preprocess_image(image.copy())

        if single:
            decoded = classify_coin(processed)
            label, conf = decoded[0][1], float(decoded[0][2])
            cv2.putText(processed, f"{label} ({conf*100:.1f}%)", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            results = [{"label": label, "confidence": conf}]
            display_image(processed)
        else:
            processed, results = detect_objects(processed)
            display_image(processed)

        save_history({"file": path, "results": results})
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

    
    def open_image_tools():
        global current_raw_image
        
        if current_raw_image is None:
            messagebox.showwarning("Lỗi", "Vui lòng chọn ảnh trước khi sử dụng công cụ.")
            return

        win = Toplevel(app)
        win.title("Xử lý ảnh")
        win.geometry("300x350")
        
      
        def apply_tool(tool_func):
            global current_raw_image
            processed_img = tool_func(current_raw_image)
            current_raw_image = processed_img.copy() 
            display_image(current_raw_image)
            
        tk.Label(win, text=" Chỉnh sửa ảnh", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Button(win, text=" Xoay 90°", width=20, command=lambda: apply_tool(lambda img: rotate_image(img, 90))).pack(pady=5)
        tk.Button(win, text=" Chuyển Grayscale", width=20, command=lambda: apply_tool(convert_to_grayscale)).pack(pady=5)
        tk.Button(win, text=" Đảo ngược màu", width=20, command=lambda: apply_tool(invert_colors)).pack(pady=5)
        
        def export_image():
            global current_raw_image 
            
            if current_raw_image is None: 
                messagebox.showwarning("Lỗi", "Không có ảnh để xuất.")
                return
                
            f = filedialog.asksaveasfile(mode='w', defaultextension=".png", 
                                         filetypes=(("PNG file", "*.png"), ("JPG file", "*.jpg"), ("All Files", "*.*")))
            if f is None: return
            f.close()
            cv2.imwrite(f.name, current_raw_image)
            messagebox.showinfo("Thông báo", f"Đã lưu ảnh thành công tại: {f.name}")
            
        tk.Button(win, text=" Xuất Ảnh (Export)", width=20, bg="#28A745", fg="white", 
                  font=("Arial", 10, "bold"), command=export_image).pack(pady=15)
        
        tk.Button(win, text=" Đóng", width=20, command=win.destroy).pack(pady=5)

    tk.Button(frame_sidebar, text=" Nhận diện 1 vật thể", width=22, bg="#1976D2", fg="white",
              font=("Arial", 11, "bold"), command=lambda: choose_image(True)).pack(pady=10)

    tk.Button(frame_sidebar, text=" Nhận diện nhiều vật thể", width=22, bg="#43A047", fg="white",
              font=("Arial", 11, "bold"), command=lambda: choose_image(False)).pack(pady=10)
              
    # <<< NÚT CÔNG CỤ XỬ LÝ ẢNH BẠN CẦN >>>
    tk.Button(frame_sidebar, text="Xử lý ảnh", width=22, bg="#FFB300", fg="white",
              font=("Arial", 11, "bold"), command=open_image_tools).pack(pady=10)

    tk.Button(frame_sidebar, text=" Lịch sử kết quả", width=22, bg="#FB8C00", fg="white",
              font=("Arial", 11, "bold"), command=open_history).pack(pady=10)

    app.mainloop()