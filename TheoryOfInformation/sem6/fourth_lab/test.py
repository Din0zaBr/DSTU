import numpy as np


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


# Пример использования
infor_message = '0010'
poly = infor_message
m = poly.rindex('1')  # Находим степень полинома (индекс последней единицы)
print("Полином:", poly)

n = int(input("Введите длину кода (n): "))
k = n - m  # Количество строк (информационных битов)
print("Количество строк (k):", k)

G = polynomial_to_matrix_or_G(poly, n, k)
print("Матрица G:")
print(G)