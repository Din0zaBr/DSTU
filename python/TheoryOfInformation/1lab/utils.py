import collections
import math


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
