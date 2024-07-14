import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from openpyxl import Workbook

def extract_info_from_path(path):
    parts = path.split(os.sep)
    date_indices = [i for i, part in enumerate(parts) if part.isdigit() and len(part) == 8]
    
    if not date_indices:
        return '', '', '', ''
    
    brigade = ''
    # Находим все папки с именем 'бр' в пути и выбираем самую последнюю
    brigade_folders = [parts[i] for i in range(len(parts)) if 'бр' in parts[i]]
    if brigade_folders:
        last_brigade_folder = brigade_folders[-1]
        brigade_match = re.findall(r'\d+', last_brigade_folder)
        brigade = brigade_match[0] if brigade_match else ''
    
    # Извлечение даты
    date = parts[date_indices[-1]]
    
    # Извлечение номера борта и полета из следующей папки после последней даты
    flight = ''
    bort = ''
    if date_indices[-1] + 1 < len(parts):
        flight = parts[date_indices[-1] + 1][:10]  # Используем полное название папки "полет"
        bort = parts[date_indices[-1] + 1][:5]  # первые 5 символов для номера борта
    
    return brigade, date, bort, flight

def count_images_in_folder(folder_path):
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'}
    image_count = 0
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_count += 1

    return image_count

def create_excel_report(folder_path, output_file):
    wb = Workbook()
    ws = wb.active
    ws.title = "Report"
    
    ws.append(["Бригада", "Дата", "Борт", "Полет", "Количество картинок"])
    
    for root, dirs, files in os.walk(folder_path):
        if 'photo' in root:
            brigade, date, bort, flight = extract_info_from_path(root)
            if flight and bort:
                image_count = count_images_in_folder(root)
                ws.append([brigade, date, bort, flight, image_count])
    
    wb.save(output_file)
    messagebox.showinfo("Готово", f"Отчет сохранен в файл {output_file}")

def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def save_as():
    output_file = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                               filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if output_file:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_file)

def generate_report():
    folder_path = folder_entry.get()
    output_file = output_entry.get()
    if folder_path and output_file:
        create_excel_report(folder_path, output_file)
    else:
        messagebox.showwarning("Ошибка", "Пожалуйста, укажите путь к папке и имя выходного файла")

root = tk.Tk()
root.title("Генератор отчетов")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

folder_label = tk.Label(frame, text="Путь к папке:")
folder_label.grid(row=0, column=0, sticky="e")
folder_entry = tk.Entry(frame, width=50)
folder_entry.grid(row=0, column=1, padx=5)
folder_button = tk.Button(frame, text="Обзор...", command=browse_folder)
folder_button.grid(row=0, column=2)

output_label = tk.Label(frame, text="Имя выходного файла:")
output_label.grid(row=1, column=0, sticky="e")
output_entry = tk.Entry(frame, width=50)
output_entry.grid(row=1, column=1, padx=5)
output_button = tk.Button(frame, text="Сохранить как...", command=save_as)
output_button.grid(row=1, column=2)

generate_button = tk.Button(frame, text="Создать отчет", command=generate_report)
generate_button.grid(row=2, columnspan=3, pady=10)

root.mainloop()