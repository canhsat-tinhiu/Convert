import base64

def file_to_base64(file_path):
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read())
    return encoded_string.decode("utf-8")

def base64_to_txt(base64_string, output_file):
    with open(output_file, "w") as file:
        file.write(base64_string)

exe_file_path = "D:\\XMRIG\\xmrig.exe"

base64_string = file_to_base64(exe_file_path)

output_txt_file = "D:\\XMRIG\\output_file.txt"

base64_to_txt(base64_string, output_txt_file)
