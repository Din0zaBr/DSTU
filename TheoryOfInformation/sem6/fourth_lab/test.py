import numpy as np


def polynomial_to_matrix_or_G(poly, n, k):
    # Преобразование полинома в матрицу
    matrix = np.zeros((k, n), dtype=int)
    for i in range(k):
        for j in range(n):
            matrix[i,j] = []
    return matrix


def matrix_to_polynomial(matrix):
    # Преобразование матрицы в полином
    poly = matrix[0, :]
    return poly


# Пример использования
infor_message = '1101'
poly = infor_message
m = poly.rindex('1')
print(poly)
n = int(input("Введите длину кода: "))
k = n - m
print(k)

matrix = polynomial_to_matrix(poly, n, k)
print("Матрица:")
print(matrix)
