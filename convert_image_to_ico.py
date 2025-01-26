import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import os

class ImageConverter:
    def __init__(self):
        # Tạo cửa sổ chính
        self.window = tk.Tk()
        self.window.title("Chuyển đổi ảnh sang ICO")
        self.window.geometry("400x700")
        self.window.resizable(False, False)

        # Định nghĩa các định dạng hỗ trợ
        self.supported_formats = {
            'PNG': 'Portable Network Graphics',
            'JPEG/JPG': 'Joint Photographic Experts Group',
            'BMP': 'Bitmap Image',
            'GIF': 'Graphics Interchange Format',
            'TIFF': 'Tagged Image File Format',
            'WebP': 'Web Picture Format'
        }

        # Khởi tạo các biến
        self.input_paths = []
        self.output_dir = ""
        self.size = tk.StringVar(value="256")
        
        # Tạo giao diện
        self.create_ui()
        
    def create_ui(self):
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(expand=True, fill="both")
        
        # Tiêu đề
        ttk.Label(
            main_frame, 
            text="Chuyển đổi ảnh sang ICO",
            font=("Helvetica", 16, "bold"),
            justify="center"
        ).pack(pady=10)

        # Phần hiển thị định dạng hỗ trợ
        format_frame = ttk.LabelFrame(main_frame, text="Định dạng ảnh hỗ trợ", padding=10)
        format_frame.pack(fill="x", pady=10)
        
        for format_name, format_desc in self.supported_formats.items():
            ttk.Label(
                format_frame,
                text=f"• {format_name}: {format_desc}",
                wraplength=350,
                justify="left"
            ).pack(anchor="w", pady=2)

        # Phần chọn kích thước
        size_frame = ttk.LabelFrame(main_frame, text="Chọn kích thước", padding=10)
        size_frame.pack(fill="x", pady=10)
        
        # Tạo grid cho các radio button kích thước
        size_grid = ttk.Frame(size_frame)
        size_grid.pack(fill="x")
        
        sizes = [("16x16", "16"), ("32x32", "32"), ("48x48", "48"), 
                ("64x64", "64"), ("128x128", "128"), ("256x256", "256")]
        
        for i, (text, value) in enumerate(sizes):
            ttk.Radiobutton(
                size_grid,
                text=text,
                value=value,
                variable=self.size
            ).grid(row=i//3, column=i%3, padx=10, pady=5, sticky="w")

        # Phần chọn file và thư mục
        select_frame = ttk.LabelFrame(main_frame, text="Chọn ảnh và thư mục", padding=10)
        select_frame.pack(fill="x", pady=10)
        
        # Nút chọn ảnh
        ttk.Button(
            select_frame, 
            text="Chọn ảnh cần chuyển đổi",
            command=self.select_files,
            width=30
        ).pack(pady=5)
        
        # Label hiển thị số ảnh đã chọn
        self.file_label = ttk.Label(select_frame, text="Chưa chọn ảnh")
        self.file_label.pack(pady=5)
        
        # Nút chọn thư mục
        ttk.Button(
            select_frame,
            text="Chọn thư mục lưu",
            command=self.select_folder,
            width=30
        ).pack(pady=5)
        
        # Label hiển thị thư mục đã chọn
        self.folder_label = ttk.Label(select_frame, text="Chưa chọn thư mục")
        self.folder_label.pack(pady=5)

        # Nút bắt đầu chuyển đổi
        self.convert_button = ttk.Button(
            main_frame,
            text="BẮT ĐẦU CHUYỂN ĐỔI",
            command=self.convert_images,
            state="disabled",
            width=30
        )
        self.convert_button.pack(pady=20)

        # Thanh tiến trình
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill="x", pady=5)
        
        self.progress = ttk.Progressbar(progress_frame, length=300)
        self.progress.pack(side="left", padx=(0, 10))
        
        self.progress_label = ttk.Label(progress_frame, text="0%")
        self.progress_label.pack(side="left")

    def select_files(self):
        # Tạo filter cho dialog chọn file
        filetypes = [("Tất cả ảnh hỗ trợ", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp")]
        for format_name in self.supported_formats:
            ext = format_name.lower().split('/')[0]
            filetypes.append((format_name, f"*.{ext}"))
        filetypes.append(("Tất cả file", "*.*"))
        
        # Chọn các file ảnh
        files = filedialog.askopenfilenames(
            title="Chọn ảnh cần chuyển đổi",
            filetypes=filetypes
        )
        
        if files:
            self.input_paths = files
            self.file_label.config(text=f"Đã chọn {len(files)} ảnh")
            self.check_ready()

    def select_folder(self):
        # Chọn thư mục lưu file
        folder = filedialog.askdirectory(title="Chọn thư mục lưu ICO")
        
        if folder:
            self.output_dir = folder
            self.folder_label.config(text=f"Thư mục: {os.path.basename(folder)}")
            self.check_ready()

    def check_ready(self):
        # Kiểm tra đã chọn đủ file và thư mục chưa
        if self.input_paths and self.output_dir:
            self.convert_button.config(state="normal")
        else:
            self.convert_button.config(state="disabled")

    def convert_images(self):
        # Vô hiệu hóa nút trong quá trình chuyển đổi
        self.convert_button.config(state="disabled")
        
        # Đặt giá trị tối đa cho thanh tiến trình
        total = len(self.input_paths)
        self.progress["maximum"] = total
        
        success = 0
        errors = []

        # Xử lý từng ảnh
        for i, input_path in enumerate(self.input_paths, 1):
            try:
                # Mở ảnh
                img = Image.open(input_path)
                
                # Chuyển sang RGBA nếu cần
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGBA')
                
                # Xử lý ảnh không vuông
                if img.size[0] != img.size[1]:
                    size = min(img.size)
                    left = (img.size[0] - size) // 2
                    top = (img.size[1] - size) // 2
                    img = img.crop((left, top, left + size, top + size))
                
                # Thay đổi kích thước
                size = int(self.size.get())
                img = img.resize((size, size), Image.Resampling.LANCZOS)
                
                # Lưu file ICO
                output_name = os.path.splitext(os.path.basename(input_path))[0] + '.ico'
                output_path = os.path.join(self.output_dir, output_name)
                img.save(output_path, format='ICO')
                
                success += 1
                
            except Exception as e:
                errors.append(f"{os.path.basename(input_path)}: {str(e)}")
            
            # Cập nhật tiến trình
            self.progress["value"] = i
            percent = int((i / total) * 100)
            self.progress_label.config(text=f"{percent}%")
            self.window.update()

        # Hiển thị kết quả
        result = f"Hoàn thành!\n\nThành công: {success}/{total}"
        if errors:
            result += "\n\nLỗi:\n" + "\n".join(errors)
        
        messagebox.showinfo("Kết quả", result)
        
        # Reset giao diện
        self.convert_button.config(state="normal")
        self.progress["value"] = 0
        self.progress_label.config(text="0%")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ImageConverter()
    app.run()