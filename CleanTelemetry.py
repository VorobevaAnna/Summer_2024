import os
import pandas as pd
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox

def clean_telemetry(telemetry_file, images_dir, header_size):
    try:
        with open(telemetry_file, 'r') as file:
            lines = file.readlines()
        
        header = lines[:header_size]
        
        data_lines = lines[header_size:]
        
        images = set(os.listdir(images_dir))
        y
        def image_exists(line):
            image_name = line.split('\t')[0]
            return image_name in images
        
        filtered_data_lines = [line for line in data_lines if image_exists(line)]
        
        cleaned_data = header + filtered_data_lines
        
        cleaned_telemetry_file = telemetry_file.replace('.txt', '_cleaned.txt')
        with open(cleaned_telemetry_file, 'w') as file:
            file.writelines(cleaned_data)
        
        messagebox.showinfo("Успех", f"Очищенный файл телеметрии сохранен как {cleaned_telemetry_file}")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def select_telemetry_file():
    filename = filedialog.askopenfilename(title="Выберите файл телеметрии", filetypes=[("Text files", "*.txt")])
    telemetry_entry.delete(0, 'end')
    telemetry_entry.insert(0, filename)

def select_image_folder():
    foldername = filedialog.askdirectory(title="Выберите папку со снимками")
    image_folder_entry.delete(0, 'end')
    image_folder_entry.insert(0, foldername)

def start_cleaning():
    telemetry_file = telemetry_entry.get()
    image_folder = image_folder_entry.get()
    header_size = int(header_entry.get())

    if not telemetry_file or not image_folder:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
        return

    clean_telemetry(telemetry_file, image_folder, header_size)

root = Tk()
root.title("Очистка телеметрии")

Label(root, text="Файл телеметрии:").grid(row=0, column=0, padx=5, pady=5)
telemetry_entry = Entry(root, width=50)
telemetry_entry.grid(row=0, column=1, padx=5, pady=5)
Button(root, text="Выбрать", command=select_telemetry_file).grid(row=0, column=2, padx=5, pady=5)

Label(root, text="Папка со снимками:").grid(row=1, column=0, padx=5, pady=5)
image_folder_entry = Entry(root, width=50)
image_folder_entry.grid(row=1, column=1, padx=5, pady=5)
Button(root, text="Выбрать", command=select_image_folder).grid(row=1, column=2, padx=5, pady=5)

Label(root, text="Размер шапки:").grid(row=2, column=0, padx=5, pady=5)
header_entry = Entry(root, width=50)
header_entry.grid(row=2, column=1, padx=5, pady=5)
header_entry.insert(0, "5")
Button(root, text="Начать очистку", command=start_cleaning).grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()
