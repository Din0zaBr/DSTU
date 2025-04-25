def matrix_to_polynomial():
    """
    Преобразует первую строку матрицы G в полином.

    :param matrix: порождающая матрица G (numpy array)
    :return: кортеж из двух строк: бинарного представления и алгебраического представления полинома
    """
    # Берем первую строку матрицы
    first_row = [1, 1, 0]
    print(first_row[-1])

    # Удаляем ведущие нули с конца списка
    while first_row and first_row[-1] == 0:
        first_row.pop()

    print(first_row)

matrix_to_polynomial()