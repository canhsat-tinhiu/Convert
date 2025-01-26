
import os
import fitz
import tkinter as tk
from tkinter import filedialog, messagebox
import uuid



def pdf_to_png(pdf_path, output_folder):
    try:
        # Tạo thư mục ngẫu nhiên
        random_folder = os.path.join(output_folder, str(uuid.uuid4()))
        os.makedirs(random_folder)
        
        pdf_document = fitz.open(pdf_path)
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            output_file = os.path.join(random_folder, f"page_{page_num + 1}.png")
            pix.save(output_file)
            print(f"Đã lưu {output_file}")
        messagebox.showinfo("Thành công", f"Chuyển đổi PDF sang PNG thành công! Tệp đã được lưu vào {random_folder}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

def select_pdf_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf")],
        title="Chọn tệp PDF"
    )
    if file_path:
        pdf_path.set(file_path)

def select_output_folder():
    folder_path = filedialog.askdirectory(title="Chọn thư mục đầu ra")
    if folder_path:
        output_folder.set(folder_path)

def start_conversion():
    if pdf_path.get() and output_folder.get():
        pdf_to_png(pdf_path.get(), output_folder.get())
    else:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn tệp PDF và thư mục đầu ra!")

app = tk.Tk()
app.title("Chuyển đổi PDF sang PNG")

pdf_path = tk.StringVar()
output_folder = tk.StringVar()

tk.Label(app, text="Tệp PDF:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=pdf_path, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(app, text="Chọn tệp", command=select_pdf_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(app, text="Thư mục đầu ra:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=output_folder, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(app, text="Chọn thư mục", command=select_output_folder).grid(row=1, column=2, padx=10, pady=10)

tk.Button(app, text="Bắt đầu chuyển đổi", command=start_conversion).grid(row=2, columnspan=3, pady=20)

app.mainloop()
