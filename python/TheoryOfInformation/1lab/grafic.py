import os
import collections
import matplotlib.pyplot as plt
from tkinter import messagebox
from utils import calculate_entropy, calculate_file_entropy


def analyze_text(file_entry, entropy_label, progress_bar, results_table, loading_label, root):
    file_path = file_entry.get()

    # Проверка существования файла
    if not os.path.isfile(file_path):
        messagebox.showerror('Ошибка', 'Файл не существует')
        return

    # Подтверждение операции
    if not messagebox.askyesno('Подтверждение', 'Вы уверены, что хотите проанализировать этот файл?'):
        return

    # Отображение индикатора загрузки
    loading_label.config(text='Вычисление энтропии...')
    root.after(100)

    # Вычисление энтропии файла
    file_entropy = calculate_file_entropy(file_path)

    # Чтение содержимого файла
    with open(file_path, 'rb') as file:
        data = file.read()
    # Проверка, является ли файл текстовым
    try:
        text = data.decode('utf-8')
        # Удаление специальных символов
        special_chars = "@#$^&*{}[]<><=>=/\\|=+"
        trans = str.maketrans('', '', special_chars)
        text = text.translate(trans)

        # Вычисление энтропии текста
        text_entropy = calculate_entropy(text)

        # Построение гистограммы появления символов
        build_histogram(text)
    except UnicodeDecodeError:
        pass

    # Построение гистограммы появления всех бит
    build_bit_histogram(data)

    # Отображение результатов в таблице
    results_table.delete(*results_table.get_children())
    results_table.insert('', 'end', values=('Энтропия файла', file_entropy))
    if 'text_entropy' in locals():
        results_table.insert('', 'end', values=('Энтропия текста', text_entropy))

    # Обновление прогресс-бара
    progress_bar['value'] = 100

    # Скрытие индикатора загрузки
    loading_label.config(text='')


def build_histogram(text):
    # Разделение текста на кириллицу, латиницу и символы
    cyrillic_text = ''.join(c for c in text if 'А' <= c <= 'я' or c == 'Ё' or c == 'ё')
    latin_text = ''.join(c for c in text if 'A' <= c <= 'Z' or 'a' <= c <= 'z')
    symbols_text = ''.join(c for c in text if not (
            'А' <= c <= 'я' or c == 'Ё' or c == 'ё' or 'A' <= c <= 'Z' or 'a' <= c <= 'z') and c.isprintable())

    # Подсчет частоты каждого символа в каждом тексте
    cyrillic_frequency = collections.Counter(cyrillic_text)
    latin_frequency = collections.Counter(latin_text)
    symbols_frequency = collections.Counter(symbols_text)

    # Построение гистограмм
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    # Сортировка символов в алфавитном порядке
    cyrillic_frequency = dict(sorted(cyrillic_frequency.items()))
    latin_frequency = dict(sorted(latin_frequency.items()))
    symbols_frequency = dict(sorted(symbols_frequency.items()))

    axs[0].bar(cyrillic_frequency.keys(), cyrillic_frequency.values())
    axs[0].set_title('Гистограмма появления кириллицы')
    axs[0].set_xlabel('Символы')
    axs[0].set_ylabel('Частота')

    axs[1].bar(latin_frequency.keys(), latin_frequency.values())
    axs[1].set_title('Гистограмма появления латиницы')
    axs[1].set_xlabel('Символы')
    axs[1].set_ylabel('Частота')

    axs[2].bar(symbols_frequency.keys(), symbols_frequency.values())
    axs[2].set_title('Гистограмма появления всего остального')
    axs[2].set_xlabel('Символы')
    axs[2].set_ylabel('Частота')

    plt.tight_layout()
    plt.show()


def build_bit_histogram(data):
    # Подсчет частоты каждого байта в файле
    byte_frequency = collections.Counter(data)

    # Построение гистограммы
    plt.bar(byte_frequency.keys(), byte_frequency.values())
    plt.title('Гистограмма появления всех бит')
    plt.xlabel('Байты')
    plt.ylabel('Частота')
    plt.show()
