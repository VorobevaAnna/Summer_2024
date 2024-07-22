import pandas as pd
import re
import os
from tkinter import Tk, filedialog, Button, Label, messagebox, StringVar

def extract_number_and_sign(value):
    """Извлекает число и знак перед ним из строки."""
    match = re.search(r'([-+]?\d*\.?\d+)', str(value))
    return float(match.group(1)) if match else 0

def select_mrt_file():
    mrt_file.set(filedialog.askopenfilename(title="Выберите MRK файл", filetypes=[("MRK Files", "*.MRK")]))
    if mrt_file.get():
        lbl_mrt_file.config(text=os.path.basename(mrt_file.get()))

def select_txt_file():
    txt_file.set(filedialog.askopenfilename(title="Выберите TXT файл", filetypes=[("Text Files", "*.txt")]))
    if txt_file.get():
        lbl_txt_file.config(text=os.path.basename(txt_file.get()))

def select_image_folder():
    image_folder.set(filedialog.askdirectory(title="Выберите папку с изображениями"))
    if image_folder.get():
        lbl_image_folder.config(text=os.path.basename(image_folder.get()))

def select_output_folder():
    output_folder.set(filedialog.askdirectory(title="Выберите папку для сохранения"))
    if output_folder.get():
        lbl_output_folder.config(text=os.path.basename(output_folder.get()))

def remove_empty_lines(file_path):
    with open(file_path, 'r', encoding='Windows-1251') as file:
        lines = file.readlines()

    with open(file_path, 'w', encoding='Windows-1251') as file:
        for line in lines:
            if line.strip():  # Пропускаем пустые строки
                file.write(line)

def process_files():
    if not mrt_file.get() or not txt_file.get() or not image_folder.get() or not output_folder.get():
        messagebox.showwarning("Внимание", "Пожалуйста, выберите все необходимые файлы и папки.")
        return

    try:
        # Чтение данных из MRT файла
        mrt_data = pd.read_csv(mrt_file.get(), sep='\s+', header=None, usecols=[3, 4, 5],
                               names=['Col4', 'Col5', 'Col6'], encoding='Windows-1251')
        mrt_data['Col4'] = mrt_data['Col4'].apply(extract_number_and_sign) / 1000
        mrt_data['Col5'] = mrt_data['Col5'].apply(extract_number_and_sign) / 1000
        mrt_data['Col6'] = mrt_data['Col6'].apply(extract_number_and_sign) / 1000

        # Чтение заголовка из исходного TXT файла
        with open(txt_file.get(), 'r', encoding='Windows-1251') as file:
            header = file.readline().strip()

        # Чтение данных из TXT файла
        txt_data = pd.read_csv(txt_file.get(), sep='\s+', header=1, usecols=[0, 1, 2, 3, 4, 5, 6],
                               names=['col1', 'Col2', 'Col3', 'col4', 'Col5', 'Col6', 'Col7'], encoding='Windows-1251')

        # Получение списка файлов изображений из выбранной папки (только JPG)
        image_files = sorted([f for f in os.listdir(image_folder.get()) if f.lower().endswith('.jpg') and os.path.isfile(os.path.join(image_folder.get(), f))])

        # Проверка, что количество изображений совпадает с количеством строк в txt_data
        if len(image_files) != len(txt_data):
            messagebox.showerror("Ошибка", "Количество изображений не совпадает с количеством строк в TXT файле.")
            return

        # Добавление имен файлов изображений в первую колонку txt_data
        txt_data['col1'] = image_files

        # Выполнение операций
        txt_data['Col2'] = txt_data['Col2'] + mrt_data['Col5']
        txt_data['Col3'] = txt_data['Col3'] + mrt_data['Col4']
        txt_data['col4'] = txt_data['col4'] - mrt_data['Col6']

        # Создаем новый TXT файл для сохранения
        new_txt_file = filedialog.asksaveasfilename(title="Сохранить как", defaultextension=".txt",
                                                    filetypes=[("Text Files", "*.txt")],
                                                    initialdir=output_folder.get())
        if new_txt_file:
            with open(new_txt_file, 'w', encoding='Windows-1251') as file:
                file.write(header + "\n")  # Записываем заголовок из исходного TXT файла
                txt_data.to_csv(file, sep='\t', index=False, header=False)

            # Удаляем пустые строки из нового файла
            remove_empty_lines(new_txt_file)

            messagebox.showinfo("Успех", f"Обновленные данные успешно записаны в файл '{new_txt_file}'.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

# Создаем главное окно
root = Tk()
root.title("Обработка файлов")

# Переменные для хранения путей
mrt_file = StringVar()
txt_file = StringVar()
image_folder = StringVar()
output_folder = StringVar()

# Метки и кнопки для выбора файлов и папок
Label(root, text="Выберите MRK файл:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
Button(root, text="Выбрать MRK файл", command=select_mrt_file).grid(row=0, column=1, padx=10, pady=5)
lbl_mrt_file = Label(root, text="", wraplength=200)
lbl_mrt_file.grid(row=0, column=2, padx=10, pady=5)

Label(root, text="Выберите TXT файл:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
Button(root, text="Выбрать TXT файл", command=select_txt_file).grid(row=1, column=1, padx=10, pady=5)
lbl_txt_file = Label(root, text="", wraplength=200)
lbl_txt_file.grid(row=1, column=2, padx=10, pady=5)

Label(root, text="Выберите папку с изображениями:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
Button(root, text="Выбрать папку с изображениями", command=select_image_folder).grid(row=2, column=1, padx=10, pady=5)
lbl_image_folder = Label(root, text="", wraplength=200)
lbl_image_folder.grid(row=2, column=2, padx=10, pady=5)

Label(root, text="Выберите папку для сохранения:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
Button(root, text="Выбрать папку", command=select_output_folder).grid(row=3, column=1, padx=10, pady=5)
lbl_output_folder = Label(root, text="", wraplength=200)
lbl_output_folder.grid(row=3, column=2, padx=10, pady=5)

# Кнопка для запуска обработки файлов
Button(root, text="Обработать файлы", command=process_files).grid(row=4, columnspan=3, padx=10, pady=20)

# Запуск главного цикла
root.mainloop()