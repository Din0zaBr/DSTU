import numpy as np


def polynomial_to_matrix(polynomial, n):
    """
    Преобразует полином в порождающую матрицу.
    :param polynomial: строка, представляющая полином (например, "1+x+x^3")
    :param n: длина кодового слова
    :return: порождающая матрица
    """
    # Создаем список коэффициентов полинома
    coefficients = [0] * n
    terms = polynomial.split('+')
    for term in terms:
        if 'x' not in term:
            coefficients[0] = int(term)
        elif '^' in term:
            power = int(term.split('^')[1])
            coefficients[power] = 1
        else:
            coefficients[1] = 1

    # Формируем порождающую матрицу
    matrix = []
    for i in range(n - len(coefficients) + 1):
        row = [0] * n
        for j in range(len(coefficients)):
            row[i + j] = coefficients[j]
        matrix.append(row)

    return np.array(matrix)


def matrix_to_polynomial(matrix):
    """
    Преобразует порождающую матрицу в полином.
    :param matrix: порождающая матрица
    :return: строка, представляющая полином
    """
    # Берем первую строку матрицы как коэффициенты полинома
    coefficients = matrix[0]
    polynomial = ""
    for i, coeff in enumerate(coefficients):
        if coeff == 1:
            if i == 0:
                polynomial += "1+"
            elif i == 1:
                polynomial += "x+"
            else:
                polynomial += f"x^{i}+"
    return polynomial.rstrip('+')


def encode_text(text, method, param):
    """
    Кодирует текст с использованием выбранного метода.
    :param text: входной текст
    :param method: метод кодирования ('polynomial' или 'matrix')
    :param param: параметр для метода (полином или матрица)
    :return: закодированная последовательность
    """
    # Преобразуем текст в битовую последовательность
    binary_sequence = ''.join(format(ord(char), '08b') for char in text)

    if method == 'polynomial':
        # Кодирование с использованием полинома
        n = len(param)  # Длина кодового слова
        encoded_sequence = ''
        for bit in binary_sequence:
            encoded_sequence += bit  # Просто добавляем биты (можно усложнить)
    elif method == 'matrix':
        # Кодирование с использованием матрицы
        encoded_sequence = np.dot(binary_sequence, param) % 2  # Упрощенная логика

    return encoded_sequence


def main():
    print("Выберите источник текста:")
    print("1. Ввод с клавиатуры")
    print("2. Загрузка из файла")
    choice = input("Введите номер: ")

    if choice == '1':
        text = input("Введите текст: ")
    elif choice == '2':
        filename = input("Введите имя файла: ")
        with open(filename, 'r') as file:
            text = file.read()
    else:
        print("Неверный выбор.")
        return

    print("\nВыберите способ ввода кода:")
    print("1. Полином")
    print("2. Матрица")
    code_choice = input("Введите номер: ")

    if code_choice == '1':
        polynomial = input("Введите полином (например, '1+x+x^3'): ")
        n = int(input("Введите длину кодового слова (n): "))
        matrix = polynomial_to_matrix(polynomial, n)
        print("\nПолином:", polynomial)
        print("Матрица:")
        print(matrix)
    elif code_choice == '2':
        rows = int(input("Введите количество строк матрицы: "))
        cols = int(input("Введите количество столбцов матрицы: "))
        print("Введите элементы матрицы построчно:")
        matrix = []
        for _ in range(rows):
            row = list(map(int, input().split()))
            matrix.append(row)
        matrix = np.array(matrix)
        polynomial = matrix_to_polynomial(matrix)
        print("\nМатрица:")
        print(matrix)
        print("Полином:", polynomial)
    else:
        print("Неверный выбор.")
        return

    # Выбираем метод кодирования
    method = 'polynomial' if code_choice == '1' else 'matrix'
    encoded_sequence = encode_text(text, method, matrix)
    print("\nЗакодированная последовательность:")
    print(encoded_sequence)


if __name__ == "__main__":
    main()