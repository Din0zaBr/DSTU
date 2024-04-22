import os
from math import sqrt


def count_seconds_from_file():
    """
    Считает общее количество секунд, указанных в файле.

    Возвращает:
    int: Общее количество секунд, указанных в файле.

    Исключения:
    FileNotFoundError: Если файл не найден.
    """
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, 'dataset.txt')
    # Проверяем, существует ли файл, и если нет, создаем его
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            print("Наполните файл dataset.txt данными")
        return 0

    with open(file_path, 'r') as file:
        times_list = [int(line) // 100 * 60 + int(line) % 100 for line in file]
        times_list.sort()
    # не возвращаю последние 6 элементов, так как портят статистику
    return times_list[:-6]


print(count_seconds_from_file())


def calculate_mean(data):  # Среднее арифметическое из выборки ряда
    sum = 0
    for i in range(len(data)):
        sum += data[i]
    return sum / len(data)


def calculate_dispersion(data, mean):  # Дисперсия из выборки ряда
    sum = 0
    for i in range(len(data)):
        sum = sum + pow((float(data[i]) - mean), 2)
    return sum / len(data)


def calculate_correct_dispersion(dispersion, data):  # Исправленная дисперсия
    return dispersion * (len(data) / (len(data) - 1))


def calculate_standard_deviation(dispersion):  # Стандартное отклонение
    return sqrt(dispersion)


def variation_range(data):  # Вариационный ряд
    variation_range = data.copy()
    variation_range.sort()
    return variation_range


def range_every_four_odd(data):  # Из выборки ряда оставляется каждый через 4 элемента, начиная с первого
    data = [data[i] for i in range(1, len(data), 4)]
    return data


def range_every_four_odd(data):  # Из выборки ряда оставляется каждый через 4 элемента, начиная с первого
    data = [data[i] for i in range(1, len(data), 4)]
    return data
