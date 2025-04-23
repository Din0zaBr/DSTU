def polynomial_division(dividend, divisor):
    """
    Делит один многочлен на другой в поле GF(2).

    :param dividend: делимое (список коэффициентов)
    :param divisor: делитель (список коэффициентов)
    :return: остаток от деления (список коэффициентов)
    """
    dividend = dividend[:]
    divisor_len = len(divisor)

    for i in range(len(dividend) - (divisor_len - 1)):
        if dividend[i] == 1:  # если текущий коэффициент делимого равен 1
            for j in range(divisor_len):
                dividend[i + j] ^= divisor[j]  # выполняем XOR (сложение в GF(2))

    # Остаток - это последние (divisor_len - 1) элементов делимого
    remainder = dividend[-(divisor_len - 1):]
    return remainder

def gen_S_array():
    # Преобразуем g(x) в список коэффициентов
    g_x = [1, 1, 0, 1, 0, 0, 0]  # первая строка матрицы G - это g(x)

    S_array = []
    e_array = [[0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0]]
    for el_e_array in e_array:
        # Преобразуем c(x) в список коэффициентов
        c_x = el_e_array

        # Вычисляем s(x) = c(x) mod g(x)
        s_x = polynomial_division(c_x, g_x)

        # Добавляем результат в S_array
        S_array.append(s_x)
    print(S_array)


gen_S_array()
