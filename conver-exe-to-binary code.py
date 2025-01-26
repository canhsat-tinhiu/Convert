import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os

class ExeToBinaryConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Chuyển EXE sang Nhị Phân")
        self.root.geometry("600x300")
        
        # Tạo style cho giao diện
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame chính
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input file
        input_frame = ttk.LabelFrame(main_frame, text="File EXE", padding="5")
        input_frame.pack(fill=tk.X, pady=5)
        
        self.input_path = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.input_path, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Chọn File", command=self.browse_input).pack(side=tk.LEFT, padx=5)
        
        # Output file
        output_frame = ttk.LabelFrame(main_frame, text="File Output", padding="5")
        output_frame.pack(fill=tk.X, pady=5)
        
        self.output_path = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_path, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(output_frame, text="Chọn Nơi Lưu", command=self.browse_output).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress.pack(fill=tk.X, pady=10)
        
        # Convert button
        ttk.Button(main_frame, text="Chuyển Đổi", command=self.convert).pack(pady=10)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Sẵn sàng")
        ttk.Label(main_frame, textvariable=self.status_var).pack()

    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="Chọn file EXE",
            filetypes=[("EXE files", "*.exe"), ("All files", "*.*")]
        )
        if filename:
            self.input_path.set(filename)
            # Tự động đề xuất tên file output
            suggested_output = os.path.splitext(filename)[0] + "_binary.txt"
            self.output_path.set(suggested_output)

    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Chọn nơi lưu file",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.output_path.set(filename)

    def convert(self):
        input_path = self.input_path.get()
        output_path = self.output_path.get()
        
        if not input_path or not output_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn file input và output")
            return
        
        try:
            # Đọc file EXE
            self.status_var.set("Đang đọc file...")
            self.progress_var.set(20)
            self.root.update()
            
            with open(input_path, 'rb') as exe_file:
                binary_data = exe_file.read()
            
            # Chuyển đổi sang nhị phân
            self.status_var.set("Đang chuyển đổi...")
            self.progress_var.set(50)
            self.root.update()
            
            binary_string = ' '.join(format(byte, '08b') for byte in binary_data)
            
            # Lưu file
            self.status_var.set("Đang lưu file...")
            self.progress_var.set(80)
            self.root.update()
            
            with open(output_path, 'w') as txt_file:
                txt_file.write(binary_string)
            
            self.progress_var.set(100)
            self.status_var.set("Hoàn thành!")
            messagebox.showinfo("Thành công", "Chuyển đổi file thành công!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
            self.status_var.set("Có lỗi xảy ra!")
        
        finally:
            # Reset progress bar
            self.root.after(2000, lambda: self.progress_var.set(0))
            self.root.after(2000, lambda: self.status_var.set("Sẵn sàng"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ExeToBinaryConverter(root)
    root.mainloop()