from PySimpleGUI import *
import numpy as np


def start():
    """
    Основная функция
    :return:
    """
    global type_of
    layout = [[Radio('Порождающая матрица (G)', 'RADIO1', key='G'),
               Radio('Полином', 'RADIO1', key='pol')],
              [Button('Далее')]]
    window = Window('Лабораторная работа №4', layout)

    while True:
        event, values = window.read()
        try:
            if event == WIN_CLOSED:
                exit()
            elif event == 'Далее':
                if values['G']:
                    window.close()
                    type_of = 'G'
                    start_window_G()
                    return
                elif values['pol']:
                    window.close()
                    type_of = 'pol'
                    start_window_pol()
                    return
                else:
                    popup_error('Проверьте данные.')
            else:
                popup_error('Проверьте данные.')
        except Exception as e:
            if event == WIN_CLOSED:
                exit()
            else:
                popup_error(f"Ошибка. Проверьте данные: {e}")


def start_window_pol():
    """
    Отвечает за получение размерности матрицы G, а также n и k
    :return:
    """
    global n

    layout = [[Text('n: ', size=(15, 1)), Input(key='n')],
              [Button('Далее')]]
    window = Window('Лабораторная работа №4', layout)

    while True:
        event, values = window.read()
        try:
            if event == WIN_CLOSED:
                exit()
            elif event == 'Далее' and int(values['n']) > 0:
                n = int(values['n'])
                window.close()
                return
            else:
                popup_error('Проверьте данные.')
        except Exception as e:
            if event == WIN_CLOSED:
                exit()
            else:
                popup_error(f"Ошибка. Проверьте данные: {e}")


def start_window_G():
    """
    Отвечает за получение размерности матрицы G, а также n и k
    :return:
    """
    global n, k

    layout = [[Text('Кол-во столбцов (n):', size=(15, 1)), Input(key='n')],
              [Text('Кол-во строк (k):', size=(15, 1)), Input(key='k')],
               [Button('Далее')]]
    window = Window('Лабораторная работа №4', layout)

    while True:
        event, values = window.read()
        try:
            if event == WIN_CLOSED:
                exit()
            elif event == 'Далее' and (values['n'] != values['k']) and int(values['n']) > 0 and int(
                    values['k']) > 0 and int(values['n']) > int(values['k']):
                n, k = int(values['n']), int(values['k'])
                window.close()
                return
            else:
                popup_error('Проверьте данные.')
        except Exception as e:
            if event == WIN_CLOSED:
                exit()
            else:
                popup_error(f"Ошибка. Проверьте данные: {e}")


def is_valid_cyclic_matrix(G):
    """
    Проверяет, является ли матрица G корректной порождающей матрицей циклического кода.

    :param G: матрица (numpy array)
    :return: True, если матрица корректна, иначе False
    """
    k, n = G.shape  # Размеры матрицы
    # Проверяем, что каждая строка является циклическим сдвигом предыдущей строки
    for i in range(1, k):
        # Циклический сдвиг предыдущей строки
        cyclic_shift = np.roll(G[i - 1], 1)

        # Сравниваем текущую строку с циклическим сдвигом
        if not np.array_equal(G[i], cyclic_shift):
            popup_error(f"Ошибка: Строка {i + 1} не является циклическим сдвигом строки {i}.")
            return False

    # Если проверка пройдена
    return True


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
    print(algebraic_representation)
    print()
    print(binary_representation)

    return binary_representation, algebraic_representation

def polynomial_to_matrix(poly, n, k):
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


def get_matrix_or_G():
    """
    Считывание матрицы от пользователя
    :return:
    Возвращает матрицу в формате строки - это столбцы, а столбцы - это строки
    """
    global k, n, G, real_g_x_in_algebraic, real_g_x_in_binary

    if type_of == 'G':
        layout = [[Input(size=(3, 2), key=f'el_{j}_{i}', enable_events=True) for j in range(n)] for i in range(k)]
    else:
        layout = [[Input(size=(3, 2), key=f'el_{i}_{j}', enable_events=True) for j in range(n)] for i in range(1)]

    layout.append([Button('Далее')])
    layout.insert(0, [Text('Введите матрицу или полином:')])
    window = Window('', layout)

    while True:
        event, values = window.read()

        if event == WINDOW_CLOSED:
            break
        elif event.startswith('el_'):
            # Проверяем введенное значение
            input_value = values[event]
            if input_value not in ('0', '1', ''):
                # Если значение не 0 или 1, очищаем поле ввода
                window[event].update('')
                popup_error('Вводите только 0 или 1.')
        elif event == 'Далее':
            if type_of == 'G':
                matrix = [[int(values[f'el_{i}_{j}']) for j in range(k)] for i in range(n)]
                matrix_true = [[matrix[j][i] for j in range(n)] for i in range(k)]
                if is_valid_cyclic_matrix(np.array(matrix_true)):
                    G = matrix_true
                    # for row in G:
                    #     print(row)
                    # print()
                    real_g_x_in_binary, real_g_x_in_algebraic = matrix_to_polynomial(G)
                    # print(real_g_x_in_algebraic)
                    # print(real_g_x_in_binary)
                    window.close()
                    return
                else:
                    popup_error('Матрица не является корректной порождающей матрицей циклического кода.')
            else:
                g_x: list[list] = [[int(values[f'el_{i}_{j}']) for j in range(n)] for i in range(1)]
                real_g_x: str = ''.join(''.join(map(str, el)) for el in g_x)
                # print(real_g_x)
                m = real_g_x.rindex('1')
                # print(m)
                k = n - m
                # print(k)
                G = polynomial_to_matrix(real_g_x, n, k)
                # for row in G:
                #     print(row)
                window.close()
                return


def mul_matrix(matrix, vector):
    temp_result = []
    for i in range(len(vector)):
        if vector[i] == 1:
            temp_result.append(matrix[i])

    result = [0 for _ in range(len(matrix[0]))]

    for i in range(len(temp_result)):
        for j in range(len(temp_result[i])):
            result[j] = result[j] ^ temp_result[i][j]
    return result


def gen_array_i():
    global vector_array_i

    temp_array_i = []
    for i in range(2 ** k):
        temp_array_i.append(str(bin(i)[2:]))

    temp_array_i = [el.zfill(k) for el in temp_array_i]
    vector_array_i = [[int(i) for i in vector] for vector in temp_array_i]
    for i in range(len(vector_array_i)):
        print(vector_array_i[i])


# def gen_array_i_new(k):
#     temp_array_i = []
#     for i in range(2 ** k):
#         temp_array_i.append(str(bin(i)[2:]))
#
#     temp_array_i = [el.zfill(k) for el in temp_array_i]
#     print(temp_array_i)
#     print()
#     vector_array_i = [[int(i) for i in vector] for vector in temp_array_i]
#     print(vector_array_i)
#     return vector_array_i


def gen_array_c():
    global vector_array_c

    vector_array_c = [mul_matrix(G, i) for i in vector_array_i]

def gen_e_array():
    global e_array

    e_array = []

    for el in range(1, 2 ** (n)):
        str_el_bin = str(bin(el)[2:]).zfill(n)
        if str_el_bin.count('1') == 1:
            e_array.append([int(el) for el in str_el_bin])
    print(e_array)



def gf2_polynomial_division(
        dividend,
        divisor
):
    """
    Делит полином dividend на divisor в поле GF(2).

    Параметры
    ----------
    dividend : Sequence[int]
        Список бит полинома от старшей степени к младшей (len = n).
    divisor : Sequence[int]
        Список бит порождающего полинома от старшей степени к младшей (len = m+1).

    Возвращает
    -------
    quotient : List[int]
        Коэффициенты частного (len = n-m+1).
    remainder : List[int]
        Остаток степени < m (len = m).
    """
    while divisor[-1] == 0:
        divisor.pop()
    divisor = divisor[::-1]

    a = list(dividend)
    n, m = len(a), len(divisor)
    if n < m:
        return [0], a.copy()

    quotient = [0] * (n - m + 1)
    for i in range(n - m + 1):
        if a[i]:
            quotient[i] = 1
            # вычитание в GF(2) = XOR
            for j in range(m):
                a[i + j] ^= divisor[j]
    # остаток — последние m бит
    remainder = a[-m:] if m > 0 else []
    return quotient, remainder

def gen_S_array():
    global S_array

    # Преобразуем g(x) в список коэффициентов
    g_x = list(G[0]) # первая строка матрицы G - это g(x)
    g_x = [int(i) for i in g_x]
    print(g_x)


    S_array = []

    for el_e_array in e_array:
        # Преобразуем c(x) в список коэффициентов
        c_x = el_e_array

        # Вычисляем s(x) = c(x) mod g(x)
        _, s_x = gf2_polynomial_division(c_x, g_x)

        # Добавляем результат в S_array
        S_array.append(s_x)
    print(S_array)




def Encoding_and_Decoding(i_array, c_array, S_array, e_array, function_type, text, k, n, g):
    if function_type == "Encoding":
        # Преобразуем текст в бинарную строку
        bin_str = ''.join(format(el, '08b') for el in bytearray(text, 'utf-8'))

        # Дополняем бинарную строку нулями до кратности k
        bin_str = bin_str.zfill(len(bin_str) + k - (len(bin_str) % k))
        print(bin_str)
        print()

        encoding_array = []

        # Разбиваем бинарную строку на блоки по k бит
        for i in range(0, len(bin_str), k):
            encoding_array.append(bin_str[i:i + k])

        print(encoding_array)
        print()

        output_text_real = ''
        # output_text = []
        for el in encoding_array:
            index_c = i_array.index([int(i) for i in el])
            output_text_real += ''.join([str(i) for i in c_array[index_c]])
            # output_text.append(''.join([str(i) for i in c_array[index_c]]))
        print("Encoded output text:", output_text_real)
        return output_text_real
# 000000000101110001101001011100011010010111000000000101110001101
# 000000000101110001101001011100011010010111000000000101110001101
    else:
        g_x = list(G[0])  # первая строка матрицы G - это g(x)
        g_x = [int(i) for i in g_x]

        bin_array = []
        for i in range(0, len(text), n):
            bin_array.append([int(el) for el in text[i:i + n]]) # c-шечки все
        output_text_temp = ''

        for el in bin_array:
            S_temp = mul_matrix(HsysT, el)
            if S_temp in S_array:
                S_temp_index = S_array.index(S_temp)
                e_temp = e_array[S_temp_index]
                for index_el in range(len(el)):
                    el[index_el] = el[index_el] ^ e_temp[index_el]
                index_i = c_array.index([int(i) for i in el])
                output_text_temp += ''.join([str(i) for i in i_array[index_i]])

            else:
                index_i = c_array.index(el)
                output_text_temp += ''.join([str(i) for i in i_array[index_i]])

        binary_word = ''.join(map(str, [int(i) for i in output_text_temp]))

        bity_chunks = [binary_word[i:i + 8] for i in range(len(binary_word) % 8, len(binary_word), 8)]

        byte_array = bytearray(int(byte, 2) for byte in bity_chunks)

        output_text = ''.join(char for char in byte_array.decode('utf-8') if char.isprintable())

    return output_text


def output_matrix():
    layout_matrix = [[Text('G=')],
                     [Table(values=G, headings=[' ' + str(i) + ' ' for i in range(len(G[0]))], max_col_width=20,
                            # background_color='light blue',
                            col_widths=20,
                            justification='center',
                            key='-TABLE-',
                            row_height=25)],
                     [Button('Назад')]]
    window_matrix = Window('Лабораторная работа №4', layout_matrix)

    while True:
        event, values = window_matrix.read()
        if event in (WIN_CLOSED, 'Назад'):
            window_matrix.close()
            break


def output_table():
    layout_table = [
        [Table(values=[[vector_array_i[ind], vector_array_c[ind]] for ind in range(len(vector_array_c))],
               headings=['i', 'c'], max_col_width=20,
               # background_color='light blue',
               col_widths=20,
               justification='center',
               key='-TABLE-',
               row_height=25)],
        [Table(values=[[S_array[ind], e_array[ind]] for ind in range(len(e_array))],
               headings=['S', 'e'], max_col_width=20,
               # background_color='light blue',
               col_widths=20,
               justification='center',
               key='-TABLE-',
               row_height=25)],
        [Button('Назад')]]
    window_table = Window('Лабораторная работа №4', layout_table)
    while True:
        event, values = window_table.read()
        if event in (WIN_CLOSED, 'Назад'):
            window_table.close()
            break


def output_const():
    layout_const = [[Text(f'k = {k}, n = {n})')],
                    [Button('Назад')]]
    window_const = Window('Лабораторная работа №4', layout_const)

    while True:
        event, values = window_const.read()
        if event in (WIN_CLOSED, 'Назад'):
            window_const.close()
            break


def Encoding_and_Decoding_Window():
    layout = [[Text('Текст', size=(8, 1)), Input(key='text')],
              [Text('Результат:', size=(8, 1)), Input(key='output')],
              [Radio('Кодирование', 'RADIO1', key='Encoding'),
               Radio('Декодирование', 'RADIO1', key='Decoding')],
              [Button('Далее'), Button('Матрицы'), Button('Таблицы'), Button('Константы')]]
    window = Window('Лабораторная работа №4', layout)

    while True:
        event, values = window.read()
        if event in (WIN_CLOSED, 'Выход'):
            break
        if event == 'Далее':
            if values['text']:
                if values['Encoding']:
                    function_type, text = 'Encoding', values['text']
                elif values['Decoding']:
                    function_type, text = 'Decoding', values['text']
                else:
                    popup_error('Проверьте данные.')
            else:
                popup_error('Проверьте данные.')

            output_text = Encoding_and_Decoding(vector_array_i, vector_array_c, S_array, e_array, function_type, text,
                                                k, n, G[0]
                                                )

            window['output'].update(output_text)

        if event == 'Матрицы':
            output_matrix()

        if event == 'Таблицы':
            output_table()

        if event == 'Константы':
            output_const()


def main():
    start()
    get_matrix_or_G()
    gen_array_i()
    gen_array_c()
    gen_e_array()
    gen_S_array()
    Encoding_and_Decoding_Window()


if __name__ == '__main__':
    main()
