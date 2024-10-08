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
import tkinter as tk
from utils import analyze_text


def main():
    # Создание графического интерфейса
    root = tk.Tk()
    root.title('Анализатор файла')

    file_label = tk.Label(root, text='Введите путь к файлу:')
    file_label.pack()

    file_entry = tk.Entry(root, width=50)
    file_entry.pack()

    entropy_label = tk.Label(root, text='')
    entropy_label.pack()

    analyze_button = tk.Button(root, text='Анализировать файл', command=lambda: analyze_text(file_entry, entropy_label))
    analyze_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()

#  C:\Users\zabol\OneDrive\Рабочий стол\NASL.txt
#  C:\Users\zabol\Downloads\test.txt
#  C:\Users\zabol\OneDrive\Изображения\t276.jpg
#  C:\Users\zabol\iCloudDrive\iCloud~md~obsidian\Жизнь\Dancing.md
