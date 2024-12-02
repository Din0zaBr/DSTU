from PySimpleGUI import *


def start_window():
    """
    Отвечает за получение размерности матрицы и её типа G или H
    :return:
    """
    global m, l, type_matrix

    layout = [[Text('Кол-во столбцов (m):', size=(15, 1)), Input(key='m')],
              [Text('Кол-во строк (l):', size=(15, 1)), Input(key='l')],
              [Radio('Порождающая матрица (G)', 'RADIO1', key='G'),
               Radio('Проверочная матрица (H)', 'RADIO1', key='H')],
              [Button('Далее')]]
    window = Window('Лабораторная работа №4', layout)

    while True:
        event, values = window.read()
        try:
            if event == WIN_CLOSED:
                exit()
            elif event == 'Далее' and values['m'] != values['l'] and int(values['m']) > 0 and int(
                    values['l']) > 0 and int(values['m']) > int(values['l']):
                if values['G']:
                    type_matrix, m, l = 'G', int(values['m']), int(values['l'])
                    window.close()
                    return
                elif values['H']:
                    type_matrix, m, l = 'H', int(values['m']), int(values['l'])
                    window.close()
                    return
                else:
                    popup_error('Проверьте данные.')
            else:
                popup_error('Проверьте данные.')
        except:
            if event == WIN_CLOSED:
                exit()
            else:
                popup_error('Проверьте данные.')


def get_matrix():
    """
    Считывание матрицы от пользователя
    :return:
    Возвращает матрицу в формате строки - это столбцы, а столбцы - это строки
    """
    global matrix

    if type_matrix == 'G':
        layout = [[Input(size=(3, 2), key=f'el_{j}_{i}', enable_events=True) for j in range(m)] for i in range(l)]
    else:
        layout = [[Input(size=(3, 2), key=f'el_{j}_{i}', enable_events=True) for j in range(m)] for i in range(l)]

    layout.append([Button('Далее')])
    layout.insert(0, [Text('Введите матрицу:')])
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
            if type_matrix == 'G':
                matrix = [[int(values[f'el_{i}_{j}']) for j in range(l)] for i in range(m)]
                print('G=')
                matrix_true = [[matrix[j][i] for j in range(m)] for i in range(l)]
                print(*matrix_true, sep='\n')
                print('============================')
                window.close()
                return
            else:
                matrix = [[int(values[f'el_{i}_{j}']) for j in range(l)] for i in range(m)]
                print('H=')
                matrix_true = [[matrix[j][i] for j in range(m)] for i in range(l)]
                print(*matrix_true, sep='\n')
                print('============================')
                window.close()
                return


def gen_once_matrix(len_matrix):
    matrix_1 = []

    for i in range(len_matrix):
        temp = []
        for j in range(len_matrix):
            if i == j:
                temp.append(1)
            else:
                temp.append(0)
        matrix_1.append(temp)

    return matrix_1


def get_system(type_matrix, matrix):
    temp_dict_index = {}
    second_matrix_sys = []

    if type_matrix == 'G':
        # Находим индексы столбцов которые имеют 1 единицу
        for index_curent_column in range(len(matrix)):
            if sum(matrix[index_curent_column]) == 1:
                temp_dict_index[matrix[index_curent_column].index(1)] = index_curent_column

        temp_sys_matrix = [[] for i in range(l)]
        for key in sorted(temp_dict_index):
            temp_sys_matrix[key] = matrix[temp_dict_index[key]]
            matrix[temp_dict_index[key]] = []  # Заменяем строку пустым списком вместо удаления

        # Удаляем пустые строки из матрицы
        matrix = [row for row in matrix if row]

        for column in matrix:
            temp_sys_matrix.append(column)

        k = len(temp_sys_matrix[0])
        n = len(temp_sys_matrix)

        # len(matrix) - кол-во строк матрицы H

        second_matrix_sys = [[matrix[i][j] for j in range(len(matrix[0]))] for i in range(len(matrix))]

        temp_add_matrix = gen_once_matrix(len(matrix))

        for i in range(len(matrix)):
            second_matrix_sys[i].extend(temp_add_matrix[i])

        sys_matrix = [[temp_sys_matrix[j][i] for j in range(m)] for i in range(l)]

    else:
        # Находим индексы столбцов которые имеют 1 единицу
        for index_curent_column in range(len(matrix)):
            if sum(matrix[index_curent_column]) == 1:
                temp_dict_index[matrix[index_curent_column].index(1)] = index_curent_column

        temp_sys_matrix = [[] for i in range(l)]
        for key in sorted(temp_dict_index):
            temp_sys_matrix[key] = matrix[temp_dict_index[key]]
            matrix[temp_dict_index[key]] = []  # Заменяем строку пустым списком вместо удаления

        temp_sys_matrix.reverse()

        # Удаляем пустые строки из матрицы
        matrix = [row for row in matrix if row]

        for column in matrix:
            temp_sys_matrix.append(column)

        k = len(temp_sys_matrix[0])
        n = len(temp_sys_matrix)

        # len(matrix) - кол-во строк матрицы H
        for i in matrix:
            i.reverse()
        matrix.reverse()

        second_matrix_sys = [[matrix[i][j] for j in range(len(matrix[0]))] for i in range(len(matrix))]
        print('===============')
        print(*second_matrix_sys, sep='\n')
        print('===============')

        temp_add_matrix = gen_once_matrix(len(matrix))

        for i in range(len(matrix)):
            second_matrix_sys[i] = temp_add_matrix[i] + second_matrix_sys[i]

        k = len(second_matrix_sys)
        n = len(second_matrix_sys[0])

        temp_sys_matrix.reverse()

        sys_matrix = [[temp_sys_matrix[j][i] for j in range(m)] for i in range(l)]

    return sys_matrix, second_matrix_sys, n, k


def get_sys_matrix():
    """
    Преобразует матарицу в системуную и находит вторую системную
    :return:
    """
    global Gsys, Hsys, n, k

    if type_matrix == 'G':
        Gsys, Hsys, n, k = get_system(type_matrix, matrix)
        print('Gsys=')
        print(*Gsys, sep='\n')
        print('Hsys=')
        print(*Hsys, sep='\n')
        print('k=', k)
        print('n=', n)
    else:
        Hsys, Gsys, n, k = get_system(type_matrix, matrix)
        print('Hsys=')
        print(*Hsys, sep='\n')
        print('Gsys=')
        print(*Gsys, sep='\n')
        print('k=', k)
        print('n=', n)


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
    print('i = ')
    print(*vector_array_i, sep='\n')
    print('=' * 10)


def gen_array_c_and_dmin_t_p():
    global vector_array_c, dmin, t, p

    vector_array_c = [mul_matrix(Gsys, i) for i in vector_array_i]
    print('c = ')
    print(*vector_array_c, sep='\n')
    print('=' * 10)
    wh_array = [str(vector_array_c[inde]).count('1') for inde in range(1, len(vector_array_c))]
    dmin = min(wh_array)
    p = dmin - 1
    t = p // 2
    print(f'p {p} t {t}')


def gen_HsysT():
    global HsysT

    HsysT = [[0 for _ in range(len(Hsys))] for _ in range(len(Hsys[0]))]

    for i in range(len(Hsys)):
        for j in range(len(Hsys[0])):
            HsysT[j][i] = Hsys[i][j]
    print('HsysT=')
    print(*HsysT, sep='\n')


def gen_e_array():
    global e_array

    e_array = []

    for el in range(1, 2 ** (n)):
        str_el_bin = str(bin(el)[2:]).zfill(n)
        if str_el_bin.count('1') < (t + 1):
            e_array.append([int(el) for el in str_el_bin])

    print('e = ')
    print(*e_array, sep='\n')
    print('=' * 10)


def gen_S_array():
    global S_array

    S_array = [mul_matrix(HsysT, el_e_array) for el_e_array in e_array]

    print('S = ')
    print(*S_array, sep='\n')
    print('=' * 10)


def Encoding_and_Decoding(i_array, c_array, S_array, e_array, function_type, text, k, n, HsysT):
    if function_type == "Encoding":
        bin_str = ''.join(format(el, '08b') for el in bytearray(text, 'utf-8'))
        print(bin_str)

        bin_str = bin_str.zfill(len(bin_str) + k - (len(bin_str) % k))
        print(bin_str)

        encoding_array = []

        for i in range(0, len(bin_str), k):
            encoding_array.append(bin_str[i:i + k])
            print(bin_str[i:i + k])

        print(len(encoding_array))
        output_text = ''
        for el in encoding_array:
            index_c = i_array.index([int(i) for i in el])
            output_text += ''.join([str(i) for i in c_array[index_c]])
            print(f'el {el} c {c_array[index_c]}, i {i_array[index_c]}')

    else:
        print('=' * 10)
        bin_array = []
        for i in range(0, len(text), n):
            bin_array.append([int(el) for el in text[i:i + n]])

        output_text = ''
        output_text_temp = ''

        for el in bin_array:
            S_temp = mul_matrix(HsysT, el)
            if S_temp in S_array:
                S_temp_index = S_array.index(S_temp)
                e_temp = e_array[S_temp_index]

                for index_el in range(len(el)):
                    el[index_el] = el[index_el] ^ e_temp[index_el]

                index_i = c_array.index([int(i) for i in el])
                output_text += chr(int(''.join([str(i) for i in i_array[index_i]])))
            else:
                index_i = c_array.index(el)
                output_text_temp += ''.join([str(i) for i in i_array[index_i]])
                print(f'el {el} c {c_array[index_i]}, i {i_array[index_i]}')

        print(output_text_temp)
        binary_word = ''.join(map(str, output_text_temp))
        print(binary_word)

        bity_chunks = [binary_word[i:i + 8] for i in range(len(binary_word) % 8, len(binary_word), 8)]
        print(bity_chunks)

        byte_array = bytearray(int(byte, 2) for byte in bity_chunks)

        output_text = ''.join(char for char in byte_array.decode('utf-8') if char.isprintable())

    return output_text


def Encoding_and_Decoding_Window():
    layout = [[Text('Текст', size=(8, 1)), Input(key='text')],
              [Text('Результат:', size=(8, 1)), Input(key='output')],
              [Radio('Кодирование', 'RADIO1', key='Encoding'),
               Radio('Декодирование', 'RADIO1', key='Decoding')],
              [Button('Далее')]]
    window = Window('Лабораторная работа №4', layout)

    while True:
        event, values = window.read()
        if event in (WIN_CLOSED, 'Выход'):
            exit()
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

        output_text = Encoding_and_Decoding(vector_array_i, vector_array_c, S_array, e_array, function_type, text, k, n,
                                            HsysT)
        window['output'].update(output_text)


def main_new():
    start_window()
    get_matrix()
    get_sys_matrix()
    gen_array_i()
    gen_array_c_and_dmin_t_p()
    gen_HsysT()
    gen_e_array()
    gen_S_array()
    Encoding_and_Decoding_Window()
