import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image
import os

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Converter")

        self.label = tk.Label(root, text="Chọn ảnh để chuyển đổi:")
        self.label.pack()

        self.select_button = tk.Button(root, text="Chọn ảnh", command=self.select_image)
        self.select_button.pack()

        self.convert_button = tk.Button(root, text="Chuyển đổi", command=self.convert_image, state=tk.DISABLED)
        self.convert_button.pack()

        self.image_path = None

    def select_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff;*.webp;*.ico;*.jfif")]
        )
        if self.image_path:
            self.convert_button.config(state=tk.NORMAL)

    def convert_image(self):
        if not self.image_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn ảnh trước!")
            return

        formats = [
            ("PNG", "png"),
            ("JPEG", "jpeg"),
            ("BMP", "bmp"),
            ("GIF", "gif"),
            ("TIFF", "tiff"),
            ("WEBP", "webp"),
            ("ICO", "ico"),
            ("JFIF", "jfif")
        ]

        format_options = "\n".join([f"{name} (*.{ext})" for name, ext in formats])
        format_choice = simpledialog.askstring("Chọn định dạng", f"Chọn định dạng để chuyển đổi:\n{format_options}")

        if not format_choice:
            return

        format_ext = dict(formats).get(format_choice.upper())
        if not format_ext:
            messagebox.showerror("Lỗi", "Định dạng không hợp lệ!")
            return

        try:
            with Image.open(self.image_path) as img:
                base, _ = os.path.splitext(self.image_path)
                new_image_path = f"{base}.{format_ext}"
                img.save(new_image_path, format=format_choice.upper())
                messagebox.showinfo("Thành công", f"Ảnh đã được chuyển đổi và lưu tại: {new_image_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()
