import numpy as np


def is_valid_cyclic_matrix(G):
    """
    Проверяет, является ли матрица G корректной порождающей матрицей циклического кода.

    :param G: матрица (numpy array)
    :return: True, если матрица корректна, иначе False
    """
    k, n = G.shape  # Размеры матрицы
    # if k > n:
    #     print("Ошибка: Количество строк (k) больше, чем количество столбцов (n).")
    #     return False
    # Проверяем, что все элементы матрицы бинарные
    if not np.all((G == 0) | (G == 1)):
        print("Ошибка: Матрица содержит недопустимые значения (не 0 или 1).")
        return False

    # Проверяем, что каждая строка является циклическим сдвигом предыдущей строки
    for i in range(1, k):
        # Циклический сдвиг предыдущей строки
        cyclic_shift = np.roll(G[i - 1], 1)

        # Сравниваем текущую строку с циклическим сдвигом
        if not np.array_equal(G[i], cyclic_shift):
            print(f"Ошибка: Строка {i + 1} не является циклическим сдвигом строки {i}.")
            return False

    # Если все проверки пройдены
    return True


def input_matrix():
    """
    Позволяет пользователю ввести матрицу G.

    :return: матрица G (numpy array)
    """
    print("Введите матрицу G построчно.")
    rows = int(input("Введите количество строк (k): "))
    cols = int(input("Введите количество столбцов (n): "))

    G = []
    for i in range(rows):
        row = list(map(int, input(f"Введите элементы строки {i + 1} через пробел: ").split()))
        if len(row) != cols:
            print(f"Ошибка: В строке {i + 1} должно быть {cols} элементов.")
            return None
        G.append(row)

    return np.array(G)


def polynomial_to_matrix_or_G(poly, n, k):
    """
    Преобразует полином в порождающую матрицу G размера (k, n) с циклическим сдвигом.

    :param poly: строка, представляющая полином (например, "1101")
    :param n: количество столбцов (длина кодового слова)
    :param k: количество строк (количество информационных битов)
    :return: порождающая матрица G размера (k, n)
    """
    # Создаем пустую матрицу размера (k, n)
    G = np.zeros((k, n), dtype=int)

    # Преобразуем полином в список целых чисел
    poly_bits = list(map(int, poly))

    # Заполняем матрицу G
    for i in range(k):
        # Сдвигаем полином на i позиций вправо
        shifted_poly = [0] * i + poly_bits

        # Обрезаем или дополняем до длины n
        if len(shifted_poly) > n:
            shifted_poly = shifted_poly[:n]
        else:
            shifted_poly += [0] * (n - len(shifted_poly))

        # Записываем сдвинутый полином в i-ю строку матрицы
        G[i] = shifted_poly

    return G


def matrix_to_polynomial(matrix):
    """
    Преобразует первую строку матрицы G в полином.

    :param matrix: порождающая матрица G (numpy array)
    :return: кортеж из двух строк: бинарного представления и алгебраического представления полинома
    """
    # Берем первую строку матрицы
    first_row = matrix[0]

    # Преобразуем в бинарное представление
    binary_representation = ''.join(map(str, first_row))

    # Преобразуем в алгебраическое представление
    algebraic_representation = ""
    for i, coeff in enumerate(first_row):
        if coeff == 1:
            if i == 0:
                algebraic_representation += "1+"
            elif i == 1:
                algebraic_representation += "x+"
            else:
                algebraic_representation += f"x^{i}+"

    # Убираем последний символ "+"
    algebraic_representation = algebraic_representation.rstrip('+')

    return binary_representation, algebraic_representation


if __name__ == "__main__":
    # Пример использования
    print("Выберите режим работы:")
    print("1. Ввод матрицы G")
    print("2. Ввод полинома")

    mode = int(input("Введите номер режима: "))

    if mode == 1:
        # Ввод матрицы G
        G = input_matrix()

        if G is not None:
            print("\nВведенная матрица G:")
            print(G)

            # Проверка корректности матрицы
            if is_valid_cyclic_matrix(G):
                print("Матрица G построена верно!")
            else:
                print("Матрица G построена неверно.")
            print("\nВведенная матрица G:")
            print(G)

            # Вычисляем полином
            binary_poly, algebraic_poly = matrix_to_polynomial(G)

            # Выводим результаты
            print("Бинарное представление полинома:", binary_poly)
            print("Алгебраическое представление полинома:", algebraic_poly)
            i = input("Введите информационное слово (например, '1101'): ")


    elif mode == 2:
        # Ввод полинома
        i = input("Введите информационное слово (например, '1101'): ")
        poly = input("Введите полином (например, '1101'): ")
        m = poly.rindex('1')  # Находим макс. степень полинома
        print("Полином:", poly)

        n = int(input("Введите длину кода (n): "))
        k = n - m  # Количество строк (информационных битов)
        print("Количество строк (k):", k)

        G = polynomial_to_matrix_or_G(poly, n, k)
        print("Матрица G:")
        print(G)


    else:
        print("Неверный режим. Пожалуйста, выберите 1, 2 или 3.")
