import numpy as np

def input_text():
    return input("Введите текст для кодирования: ")

def input_polynomial():
    poly = input("Введите полином (например, x^3 + x + 1): ")
    n = int(input("Введите параметр n: "))
    return poly, n

def input_matrix():
    rows = int(input("Введите количество строк матрицы: "))
    cols = int(input("Введите количество столбцов матрицы: "))
    matrix = []
    print("Введите элементы матрицы по строкам:")
    for i in range(rows):
        row = list(map(int, input().split()))
        matrix.append(row)
    return np.array(matrix)

def polynomial_to_matrix(poly, n):
    # Преобразование полинома в матрицу
    # Пример: x^3 + x + 1 -> [[1, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    coeffs = [1 if 'x^' + str(i) in poly or ('x' in poly and i == 1) or (i == 0 and '1' in poly) else 0 for i in range(n)]
    matrix = np.zeros((n, n), dtype=int)
    for i in range(n):
        matrix[i][:len(coeffs)] = coeffs
        coeffs = [0] + coeffs[:-1]
    return matrix

def matrix_to_polynomial(matrix):
    # Преобразование матрицы в полином
    # Пример: [[1, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]] -> x^3 + x + 1
    n = matrix.shape[0]
    coeffs = matrix[0]
    poly = ' + '.join([f"x^{i}" if coeffs[i] == 1 else '' for i in range(n) if coeffs[i] == 1])
    if '1' in poly.split(' + '):
        poly += ' + 1'
    return poly.strip(' + ')

def encode_text_with_polynomial(text, poly, n):
    # Кодирование текста с использованием полинома
    encoded = []
    for char in text:
        encoded.append(ord(char))
    return encoded

def encode_text_with_matrix(text, matrix):
    # Кодирование текста с использованием матрицы
    encoded = []
    for char in text:
        encoded.append(ord(char))
    return encoded

def main():
    print("Выберите способ ввода:")
    print("1. Ввести полином")
    print("2. Ввести матрицу")
    choice = int(input("Введите номер выбора: "))

    if choice == 1:
        poly, n = input_polynomial()
        matrix = polynomial_to_matrix(poly, n)
        print(f"Полином: {poly}")
        print(f"Матрица: \n{matrix}")
    elif choice == 2:
        matrix = input_matrix()
        poly = matrix_to_polynomial(matrix)
        n = matrix.shape[0]
        print(f"Матрица: \n{matrix}")
        print(f"Полином: {poly}")
    else:
        print("Неверный выбор")
        return

    text = input_text()
    encoded_poly = encode_text_with_polynomial(text, poly, n)
    encoded_matrix = encode_text_with_matrix(text, matrix)

    print(f"Закодированная последовательность (полином): {encoded_poly}")
    print(f"Закодированная последовательность (матрица): {encoded_matrix}")

if __name__ == "__main__":
    main()
