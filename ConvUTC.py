import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import re
from datetime import datetime, timedelta

# Функция для извлечения числового значения из строки в квадратных скобках
def extract_week(week_str):
    match = re.search(r'\[(\d+)\]', week_str)
    if match:
        return int(match.group(1))
    return None

# Функция для преобразования GPS времени в UTC с учетом коррекции эпохи
def gps_to_utc(gps_week, gps_seconds, use_epoch_correction=True):
    # Эпоха GPS начинается с 6 января 1980 года 00:00:00 UTC
    gps_epoch = datetime(1980, 1, 6, 0, 0, 0)
    
    # Проверяем, нужно ли учитывать коррекцию эпохи
    if use_epoch_correction:
        gps_epoch += timedelta(seconds=19)
    
    # Вычисляем количество секунд от эпохи GPS
    total_seconds = gps_week * 604800 + gps_seconds
    
    # Получаем время в UTC
    utc_time = gps_epoch + timedelta(seconds=total_seconds)
    
    return utc_time

# Функция для обработки данных из файла и сохранения результатов в txt файл
def process_file_and_save(input_filename, output_txt, use_epoch_correction=True):
    with open(output_txt, 'w') as txt_file:
        txt_file.write("")
        
        with open(input_filename, 'r') as file:
            reader = csv.reader(file, delimiter='\t')
            for row in reader:
                gps_seconds = float(row[1])  # GPS секунды из второго столбца
                gps_week_str = row[2]  # GPS неделя в формате [2318]
                
                # Извлекаем числовое значение из строки GPS недели
                gps_week = extract_week(gps_week_str)
                if gps_week is None:
                    print(f"Ошибка: Не удалось извлечь неделю из строки: {gps_week_str}")
                    continue
                
                # Преобразование GPS времени в UTC с учетом выбора коррекции эпохи
                utc_time = gps_to_utc(gps_week, gps_seconds, use_epoch_correction)
                
                # Форматируем время GPS в часы, минуты, секунды и доли секунды
                gps_time = utc_time - timedelta(seconds=19) if use_epoch_correction else utc_time
                gps_hours, gps_minutes, gps_seconds = gps_time.hour, gps_time.minute, gps_time.second + gps_time.microsecond / 1_000_000
                gps_date = f"{gps_time.year}-{gps_time.month:02}-{gps_time.day:02}"
                
                # Форматируем время UTC в часы, минуты, секунды и доли секунды
                utc_hours, utc_minutes, utc_seconds = utc_time.hour, utc_time.minute, utc_time.second + utc_time.microsecond / 1_000_000
                utc_year_last_two = utc_time.year % 100  # Получаем последние две цифры года
                utc_month, utc_day = utc_time.month, utc_time.day
                
                # Записываем строку в файл
                txt_file.write(f"{utc_year_last_two:02}  {utc_month}  {utc_day}  {utc_hours:02} {utc_minutes:02} {utc_seconds:.6f}  5  0\n")
    
    print(f"Результаты сохранены в файле {output_txt}")
    messagebox.showinfo("Готово", f"Преобразование завершено. Результаты сохранены в {output_txt}")

# Функция для создания GUI
def create_gui():
    def browse_input_file():
        nonlocal input_file_entry
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            input_file_entry.delete(0, tk.END)
            input_file_entry.insert(0, filename)
    
    def browse_output_path():
        nonlocal output_path_entry
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            output_path_entry.delete(0, tk.END)
            output_path_entry.insert(0, filename)
    
    def start_conversion():
        input_filename = input_file_entry.get()
        output_filename = output_path_entry.get()
        use_epoch_correction = epoch_correction_var.get()
        
        if not input_filename or not output_filename:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите исходный файл и путь для сохранения")
            return
        
        process_file_and_save(input_filename, output_filename, use_epoch_correction)
    
    # Создание основного окна
    root = tk.Tk()
    root.title("Программа для преобразования GPS времени в UTC")
    
    # Опции для выбора коррекции эпохи GPS
    epoch_correction_var = tk.BooleanVar(value=True)
    epoch_correction_check = tk.Checkbutton(root, text="Учитывать коррекцию эпохи GPS", variable=epoch_correction_var)
    epoch_correction_check.pack(pady=10)
    
    # Поле для выбора исходного файла
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)
    
    input_label = tk.Label(input_frame, text="Выберите исходный файл:")
    input_label.grid(row=0, column=0, padx=10, pady=5)
    
    input_file_entry = tk.Entry(input_frame, width=50)
    input_file_entry.grid(row=0, column=1, padx=10, pady=5)
    
    input_file_button = tk.Button(input_frame, text="Обзор...", command=browse_input_file)
    input_file_button.grid(row=0, column=2, padx=10, pady=5)
    
    # Поле для выбора пути сохранения
    output_frame = tk.Frame(root)
    output_frame.pack(pady=10)
    
    output_label = tk.Label(output_frame, text="Выберите путь для сохранения:")
    output_label.grid(row=0, column=0, padx=10, pady=5)
    
    output_path_entry = tk.Entry(output_frame, width=50)
    output_path_entry.grid(row=0, column=1, padx=10, pady=5)
    
    output_path_button = tk.Button(output_frame, text="Обзор...", command=browse_output_path)
    output_path_button.grid(row=0, column=2, padx=10, pady=5)
    
    # Кнопка для запуска конверсии
    convert_button = tk.Button(root, text="Начать конверсию", command=start_conversion)
    convert_button.pack(pady=20)
    
    # Запуск основного цикла обработки событий
    root.mainloop()

# Запуск создания GUI
if __name__ == "__main__":
    create_gui()