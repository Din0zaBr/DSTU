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


def calculate_sum(data):
    """
    Вычисляет сумму чисел для переданного массива.

    Параметры:
    data (list): Список чисел.

    Возвращает:
    int: Сумма чисел.
    """
    total = 0
    for item in data:
        total += item
    return total


def calculate_length(data):
    """
    Вычисляет длину списка.

    Параметры:
    data (list): Список чисел.

    Возвращает:
    int: Длина списка.
    """
    count = 0
    for _ in data:
        count += 1
    return count


def compute_average(data):
    """
    Вычисляет среднее арифметическое из выборки ряда.

    Параметры:
    data (list): Список чисел.

    Возвращает:
    float: Среднее арифметическое.
    """
    return calculate_sum(data) / calculate_length(data)


def compute_variance(data, average):
    """
    Вычисляет дисперсию из выборки ряда.

    Параметры:
    data (list): Список чисел.
    average (float): Среднее значение.

    Возвращает:
    float: Дисперсия.
    """
    return calculate_sum(pow(value - average, 2) for value in data) / calculate_length(data)


def adjust_variance(variance, data):
    """
    Вычисляет исправленную дисперсию.

    Параметры:
    variance (float): Дисперсия.
    data (list): Список чисел.

    Возвращает:
    float: Исправленная дисперсия.
    """
    return variance * (calculate_length(data) / (calculate_length(data) - 1))


def compute_std_dev(variance):
    """
    Вычисляет стандартное отклонение.

    Параметры:
    variance (float): Дисперсия.

    Возвращает:
    float: Стандартное отклонение.
    """
    return sqrt(variance)


def partition(arr, low, high):
    """
    Подфункция, которая разделяет массив на два подмассива.
    Она выбирает опорный элемент (в данном случае последний элемент в диапазоне), перемещает все элементы,
    меньшие или равные опорному, влево от него, а все большие — вправо.

    Параметры:
    arr (list): Массив.
    low (int): Начало диапазона.
    high (int): Конец диапазона.

    Возвращает:
    int: Индекс опорного элемента после разделения.
    """
    pivot = arr[high]  # pivot - опорный элемент
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(arr, low, high):
    """
    Реализация быстрой сортировки.
    Алгоритм QuickSort — это эффективный алгоритм сортировки, использующий принцип "разделяй и властвуй".
    Он состоит из трех основных этапов:

1. Выбор опорного элемента: Опорный элемент выбирается из массива.
Обычно это первый, последний или средний элемент, хотя могут использоваться и другие стратегии выбора.

2. Разделение: Массив разделяется на два подмассива таким образом, что все элементы в первом подмассиве меньше опорного,
а во втором — больше. Опорный элемент оказывается на своём месте в отсортированном массиве.

3. Рекурсивная сортировка: Процесс повторяется рекурсивно для двух полученных подмассивов.

В данном случае функция quicksort() рекурсивно вызывает себя для двух поддиапазонов, образованных после разделения
массива вокруг опорного элемента.

    Параметры:
    arr (list): Список чисел.

    Возвращает:
    list: Отсортированный список чисел.
    """
    if low < high:
        pi = partition(arr, low, high)  # pi -  индекс опорного элемента после разделения
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)


def get_variation_range(data):
    """
    Возвращает вариационный ряд.

    Параметры:
    data (list): Список чисел.

    Возвращает:
    list: Отсортированный список чисел.
    """
    quick_sort(data, 0, calculate_length(data) - 1)
    return data


def filter_data(data):
    """
    Фильтрует данные, оставляя каждый четвертый элемент, начиная с четвёртого.

    Параметры:
    data (list): Список чисел.

    Возвращает:
    list: Фильтрованный список.
    """
    new_data = []
    for i in range(3, calculate_length(data), 4):
        new_data.append(data[i])
    return new_data
