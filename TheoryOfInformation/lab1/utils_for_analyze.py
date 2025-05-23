import collections
import math
from tkinter import messagebox
import os
from TheoryOfInformation.lab1.grafic import build_histogram, build_byte_histogram
import zipfile
import xml.etree.ElementTree as ET


def try_load_text_file(file_path):
    if file_path.endswith(".docx"):
        return load_word_file(file_path)  # Загрузка Word-файла
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except (UnicodeDecodeError, FileNotFoundError):
        # Если не удается загрузить как текст, возвращаем None
        return None


# def delete_symbols(text):
#     special_chars = "@#$^&*{}[]<><=>=/\\|=+"
#     trans = str.maketrans('', '', special_chars)
#     text = text.translate(trans)
#     return text


def analyze(file_entry, entropy_label, progress_bar, results_table, loading_label, root):
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
        text = try_load_text_file(file_path)
        if text is None:
            pass
        else:
            # Вычисление энтропии текста
            text_entropy = calculate_entropy(text)

            # Построение гистограммы появления символов
            build_histogram(text)

    except UnicodeDecodeError:
        pass

    # Построение гистограммы появления всех бит
    build_byte_histogram(data)

    # Отображение результатов в таблице
    results_table.delete(*results_table.get_children())
    results_table.insert('', 'end', values=('Энтропия файла', file_entropy))
    if 'text_entropy' in locals():
        results_table.insert('', 'end', values=('Энтропия текста', text_entropy))

    # Обновление прогресс-бара
    progress_bar['value'] = 100

    # Скрытие индикатора загрузки
    loading_label.config(text='')


"""
Cодержимое файла декодируется в формате UTF-8 с игнорированием ошибок и 
создается дерево XML с помощью xml.etree.ElementTree.
Функция использует пространство имен для извлечения текста из элементов дерева и возвращает объединенный текст.
Если во время выполнения этой функции происходит исключение, 
функция выводит сообщение об ошибке в консоль и возвращает None.


 XML позволяет описывать данные в виде тегов, которые могут быть вложены друг в друга, образуя иерархическую структуру. 
 Каждый тег может содержать атрибуты, которые описывают свойства тега. 
 XML используется для обмена данными между различными приложениями и платформами, 
 а также для хранения данных в различных форматах, таких как веб-сервисы, базы данных и файлы.
 
 В контексте данного кода, XML используется для хранения текста в файле Word (.docx). 
 Функция load_word_file открывает файл document.xml в файле Word и извлекает текст из тегов w:t, 
 используя пространство имен w для доступа к этим тегам. 
 Затем текст объединяется и возвращается в виде строки.
"""


def load_word_file(file_path):
    try:
        with zipfile.ZipFile(file_path, 'r') as docx:
            with docx.open('word/document.xml') as document:
                content = document.read().decode('utf-8', errors='ignore')
                tree = ET.ElementTree(ET.fromstring(content))
                root = tree.getroot()
                namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                text_elements = root.findall('.//w:t', namespace)
                text = ''.join([elem.text for elem in text_elements if elem.text])
        return text
    except Exception as e:
        print(f"Ошибка при чтении файла Word: {e}")
        return None


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


def calculate_file_entropy(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    # Подсчет частоты каждого байта в файле
    frequency = collections.Counter(data)
    total_bytes = len(data)
    # Вычисление энтропии
    entropy = 0
    for count in frequency.values():
        probability = count / total_bytes
        entropy -= probability * math.log2(probability)

    return entropy
