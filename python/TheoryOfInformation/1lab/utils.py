import os

import collections
import math
from tkinter import messagebox
import matplotlib.pyplot as plt
import re


def calculate_entropy(text):
    # Подсчет частоты каждого символа в тексте
    frequency = collections.Counter(text)
    total_chars = len(text)

    # Вычисление энтропии
    entropy = 0
    for count in frequency.values():
        probability = count / total_chars
        entropy -= probability * math.log2(probability)

    return entropy


# "C:\Users\zabol\OneDrive\Рабочий стол\NASL.txt"

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
    axs[2].set_title('Гистограмма появления символов')
    axs[2].set_xlabel('Символы')
    axs[2].set_ylabel('Частота')

    plt.tight_layout()
    plt.show()


def analyze_text():
    file_path = file_entry.get()

    # Проверка существования файла
    if not os.path.isfile(file_path):
        messagebox.showerror('Ошибка', 'Файл не существует')
        return

    # Проверка расширения файла
    if not file_path.endswith('.txt'):
        messagebox.showerror('Ошибка', 'Пожалуйста, выберите файл с расширением .txt')
        return

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Удаление специальных символов и символов табуляции
    text = re.sub(r'[@#$^&*{}[]< > <= >= / \\ | = +]', '', text)
    text = text.replace('\t', '')  # удаление табуляции

    # Вычисление энтропии текста
    entropy = calculate_entropy(text)
    entropy_label.config(text=f'Энтропия текста: {entropy}')

    # Построение гистограммы появления символов
    build_histogram(text)
