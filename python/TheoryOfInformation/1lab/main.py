"""
Необходимо подсчитать энтропию файла (любого), если в этом файле есть текст – то сравнить энтропию файла и текста.
Входные данные:
Файл с любым расширением
Выходные данные:
1. Гистограмма появления всех бит
2. Энтропия файла
3. Если файл содержит текст – энтропия текста
"""
from utils import analyze
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

    analyze_button = tk.Button(root, text='Анализировать файл', command=lambda: threading.Thread(target=analyze,
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
#  C:\Users\zabol\Downloads\OpenVPN-2.6.12-I001-amd64.msi
