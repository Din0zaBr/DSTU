"""
Необходимо подсчитать энтропию текста, содержащегося в файле
Входные данные:
Файл с текстом (можете сами себе поставить ограничения на разрешение файла)

В данных файлах содержаться различные буквы (латиница и кириллица), знаки
препинаний, цифры. Символы `@#$^&*{}[]< > <= >= / \ | = + ` можете удалять. Не забывайте, что пробел тоже символ

Выходные данные:
1. Гистограмма появления всех символов, которые встретились в тексте, возможны три
варианта построения гистограммы:
    а. полная гистограмма всех символов на одной оси
    б. 3-4 разных гистограмм, разбитых по смыслу (отдельно кириллица, латиница, символы)
    в. полная таблица символ-частота (вероятность) а гистограмма – первые 10-20 часто встречаемых символов
2. Энтропия текста
Язык: любой, кроме Паскаля, Делфи, Бейсика и подобных
Интерфейс – нужен, конкретных требований к нему на первой лабе не предъявляю
"""
from utils import analyze_text
import tkinter as tk
from tkinter import ttk
import threading


def main():
    # Создание графического интерфейса
    root = tk.Tk()
    root.title('Анализатор файла')

    file_label = tk.Label(root, text='Введите путь к файлу:')
    file_label.grid(row=0, column=0, padx=10, pady=10)

    file_entry = tk.Entry(root, width=50)
    file_entry.grid(row=0, column=1, padx=10, pady=10)

    entropy_label = tk.Label(root, text='')
    entropy_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    progress_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
    progress_bar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    results_table = ttk.Treeview(root, columns=('Параметр', 'Значение'), show='headings')
    results_table.heading('Параметр', text='Параметр')
    results_table.heading('Значение', text='Значение')
    results_table.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    loading_label = tk.Label(root, text='')
    loading_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    analyze_button = tk.Button(root, text='Анализировать файл', command=lambda: threading.Thread(target=analyze_text,
                                                                                                 args=(file_entry,
                                                                                                       entropy_label,
                                                                                                       progress_bar,
                                                                                                       results_table,
                                                                                                       loading_label,
                                                                                                       root)).start())
    analyze_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()

#  C:\Users\zabol\OneDrive\Рабочий стол\NASL.txt
#  C:\Users\zabol\Downloads\test.txt
#  C:\Users\zabol\OneDrive\Изображения\t276.jpg
#  C:\Users\zabol\Downloads\test.docx
#  C:\Users\zabol\iCloudDrive\iCloud~md~obsidian\Жизнь\Dancing.md
