import os
from math import sqrt, pow


def count_seconds_from_file():
    """
    Считает общее количество секунд, указанных в файле, который находится в папке с этим файлом.

    Возвращает:
    list: Список секунд, указанных в файле, без последних 6 элементов.
    P.S.
    Не возвращаю последние 6 элементов, так как они портят статистику

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
    return times_list


def compute_average(data):
    """
    Вычисляет среднее арифметическое из выборки ряда.

    Параметры:
    data (list): Список чисел.

    Возвращает:
    float: Среднее арифметическое.
    """
    return sum(data) / len(data)


def compute_variance(data, average):
    """
    Вычисляет дисперсию из выборки ряда.

    Параметры:
    data (list): Список чисел.
    average (float): Среднее значение.

    Возвращает:
    float: Дисперсия.
    """
    return sum(pow(value - average, 2) for value in data) / len(data)


def adjust_variance(variance, data):
    """
    Вычисляет исправленную дисперсию.

    Параметры:
    variance (float): Дисперсия.
    data (list): Список чисел.

    Возвращает:
    float: Исправленная дисперсия.
    """
    return variance * (len(data) / (len(data) - 1))


def compute_std_dev(variance):
    """
    Вычисляет стандартное отклонение.

    Параметры:
    variance (float): Дисперсия.

    Возвращает:
    float: Стандартное отклонение.
    """
    return sqrt(variance)


def get_variation_range(data):
    """
    Возвращает вариационный ряд.

    Параметры:
    data (list): Список чисел.

    Возвращает:
    list: Отсортированный список чисел.
    """
    # variation_range = data.copy()
    # variation_range.sort()
    # return variation_range
    return sorted(data.copy())


def filter_data(data):
    """
    Фильтрует данные, оставляя каждый четвертый элемент, начиная с второго.

    Параметры:
    data (list): Список чисел.

    Возвращает:
    list: Фильтрованный список.
    """
    return data[1::3]
