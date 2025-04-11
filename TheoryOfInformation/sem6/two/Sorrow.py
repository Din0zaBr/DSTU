from PySimpleGUI import *
import os
import numpy as np
from PIL import Image
import PySimpleGUI as sg
from typing import List, Tuple
import re


# C:\Users\ivanz\PycharmProjects\DSTU\TheoryOfInformation\sem6\3\abcd.pn
transposed_matrix_shape = None

def check_file_existence(file_path):
    if not os.path.isfile(file_path):
        sg.popup_error('Ошибка', 'Файл не существует')
        return False
    return True


def image_to_binary(image_path):
    """
    Convert image pixels to binary, then to hexadecimal, and finally encode using Huffman coding.

    :param image_path: Path to the image file.
    :return: Huffman-encoded string and the Huffman dictionary.
    """
    # Open the image
    image = Image.open(image_path).convert("RGB")
    print(f'image = {image}')
    # Convert the image to a numpy array of pixels
    pixel_array = np.array(image)
    print()
    print(f'pixel_array = {pixel_array}')
    # Convert pixel values to binary (8 bits)
    binary_array = np.unpackbits(np.array(pixel_array, dtype=np.uint8), axis=-1)
    print()
    print(f"binary_array = {binary_array}")
    # Reshape binary array to have 8-bit chunks
    binary_string = ''.join(''.join(map(str, array)) for chunk in binary_array for array in chunk)

    print()
    print("binary_string = ",binary_string)
    return binary_string,binary_array.shape


def binary_to_image(binary_string, image_path):
    _, shape = image_to_binary(image_path)
    print(f"shape = {shape}")
    # Convert binary string to binary array
    binary_array = np.array(list(binary_string), dtype=int).reshape(shape)
    print()
    print(f"binary_array = {binary_array}")
    # Pack binary array back to 8-bit values
    pixel_array = np.packbits(binary_array, axis=-1)
    print()
    print(f"pixel_array = {pixel_array}")
    # Convert pixel array to image
    image = Image.fromarray(pixel_array.astype(np.uint8), mode="RGB")
    image.save("Result.png")


def main1():
    layout = [
        [sg.Text('Выберите изображение:')],
        [sg.Input(key='image_path'), sg.FileBrowse()],
        [sg.Button('Проверить файл')],
        [sg.Text('', size=(40, 1), key='result')],
        [sg.Button('Преобразовать в бинарный вид')],
        [sg.Multiline(size=(60, 10), key='binary_array')]
    ]

    window = sg.Window('Преобразование изображения', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Проверить файл':
            image_path = values['image_path']
            if check_file_existence(image_path):
                window['result'].update('Файл существует и корректен.')
            else:
                window['result'].update('Файл не найден или путь некорректен.')
        elif event == 'Преобразовать в бинарный вид':
            image_path = values['image_path']
            if check_file_existence(image_path):
                encoded_text, _ = image_to_binary(image_path)
                window['binary_array'].update(encoded_text)
            else:
                sg.popup_error('Ошибка', 'Файл не найден или путь некорректен.')

    window.close()


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

                matrix_true = [[matrix[j][i] for j in range(m)] for i in range(l)]

                window.close()
                return
            else:
                matrix = [[int(values[f'el_{i}_{j}']) for j in range(l)] for i in range(m)]

                matrix_true = [[matrix[j][i] for j in range(m)] for i in range(l)]

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

        temp_add_matrix = gen_once_matrix(len(matrix))

        for i in range(len(matrix)):
            second_matrix_sys[i] = temp_add_matrix[i] + second_matrix_sys[i]

        k = len(second_matrix_sys)
        n = len(second_matrix_sys[0])

        temp_sys_matrix.reverse()

        sys_matrix = [[temp_sys_matrix[j][i] for j in range(m)] for i in range(l)]

    return sys_matrix, second_matrix_sys, n, k


def get_system_new(matrix, kolvo_str, kolvo_stl):
    temp_dict_index = {}
    second_matrix_sys = []

    matrix_true = [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]

    # Находим индексы столбцов которые имеют 1 единицу
    for index_curent_column in range(len(matrix_true)):
        if sum(matrix_true[index_curent_column]) == 1:
            temp_dict_index[matrix_true[index_curent_column].index(1)] = index_curent_column

    temp_sys_matrix = [[] for _ in range(kolvo_str)]
    for key in sorted(temp_dict_index):
        temp_sys_matrix[key] = matrix_true[temp_dict_index[key]]
        matrix_true[temp_dict_index[key]] = []  # Заменяем строку пустым списком вместо удаления

    temp_sys_matrix.reverse()

    # Удаляем пустые строки из матрицы
    matrix_true = [row for row in matrix_true if row]

    for column in matrix_true:
        temp_sys_matrix.append(column)

    second_matrix_sys = [[matrix_true[i][j] for i in range(len(matrix_true))] for j in range(len(matrix_true[0]))]

    temp_add_matrix = gen_once_matrix(len(second_matrix_sys))

    temp_sys_matrix = []
    for i in range(len(second_matrix_sys)):
        temp_sys_matrix.append(second_matrix_sys[i] + temp_add_matrix[i])

    sys_matrix = [[temp_sys_matrix[j][i] for i in range(kolvo_str)] for j in range(kolvo_stl)]
    return sys_matrix


def get_sys_matrix():
    """
    Преобразует матрицу в системную и находит вторую системную
    :return:
    """
    global Gsys, Hsys, n, k

    if type_matrix == 'G':
        Gsys, Hsys, n, k = get_system(type_matrix, matrix)
    else:
        Hsys, Gsys, n, k = get_system(type_matrix, matrix)


def get_sys_matrix_new(type_matrix, matrix):
    """
    Преобразует матрицу в системную и находит вторую системную
    :return:
    """
    global Gsys, Hsys, n, k

    if type_matrix == 'G':
        Gsys, Hsys, n, k = get_system(type_matrix, matrix)
    else:
        Hsys, Gsys, n, k = get_system(type_matrix, matrix)


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


def gen_array_i_new(k):
    temp_array_i = []
    for i in range(2 ** k):
        temp_array_i.append(str(bin(i)[2:]))

    temp_array_i = [el.zfill(k) for el in temp_array_i]
    vector_array_i = [[int(i) for i in vector] for vector in temp_array_i]
    return vector_array_i


def gen_array_c_and_dmin_t_p():
    global vector_array_c, dmin, t, p

    vector_array_c = [mul_matrix(Gsys, i) for i in vector_array_i]

    wh_array = [str(vector_array_c[inde]).count('1') for inde in range(1, len(vector_array_c))]
    dmin = min(wh_array)
    p = dmin - 1
    t = p // 2


def gen_HsysT():
    global HsysT

    HsysT = [[0 for _ in range(len(Hsys))] for _ in range(len(Hsys[0]))]

    for i in range(len(Hsys)):
        for j in range(len(Hsys[0])):
            HsysT[j][i] = Hsys[i][j]


def gen_e_array():
    global e_array

    e_array = []

    for el in range(1, 2 ** (n)):
        str_el_bin = str(bin(el)[2:]).zfill(n)

        if str_el_bin.count('1') < (t + 1):
            e_array.append([int(el) for el in str_el_bin])


def gen_S_array():
    global S_array

    S_array = [mul_matrix(HsysT, el_e_array) for el_e_array in e_array]



def Encoding_and_Decoding(i_array, c_array, S_array, e_array, function_type, text, k, n, HsysT):
    global transposed_matrix_shape

    if function_type == "Encoding":
        # Преобразуем текст в бинарную строку
        bin_str = ''.join(format(el, '08b') for el in bytearray(text, 'utf-8'))

        # Дополняем бинарную строку нулями до кратности k
        bin_str = bin_str.zfill(len(bin_str) + k - (len(bin_str) % k))

        encoding_array = []

        # Разбиваем бинарную строку на блоки по k бит
        for i in range(0, len(bin_str), k):
            encoding_array.append(bin_str[i:i + k])

        # output_text_real = ''
        output_text = []
        for el in encoding_array:
            index_c = i_array.index([int(i) for i in el])
            # output_text_real += ''.join([str(i) for i in c_array[index_c]])
            output_text.append(''.join([str(i) for i in c_array[index_c]]))
        # print("Encoded output text:", output_text_real)
        output_text = np.array(output_text)
        # print(output_text)
        # print()
        result = np.array([list(x) for x in output_text])
        # print(result)
        transposed_matrix = result.transpose()
        transposed_matrix_shape = transposed_matrix.shape
        # print()
        # print(transposed_matrix)
        # print(output_text)
        # print()
        # print("".join("".join(x) for x in transposed_matrix))
        return "".join("".join(x) for x in transposed_matrix)

    else:
# 001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010000101010101010101010101010101010101000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001010101010101010101010101010101010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010001000100010001000100010001000010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100
# ['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']['0']['1']['0']['0']        for i in range(0, len(text), n):
        encoded_text_str_list = [[] for _ in range(transposed_matrix_shape[1]) for _ in range(transposed_matrix_shape[0])]
        # print(encoded_text_str_list)
        for i in range(transposed_matrix_shape[1]):
            for j in range(i, transposed_matrix_shape[0]*transposed_matrix_shape[1], transposed_matrix_shape[1]):
                encoded_text_str_list[i].append(text[j])
        # print(encoded_text_str_list)
        new_text = "".join("".join(x) for x in encoded_text_str_list)
        print(new_text)

        bin_array = []
        for i in range(0, len(new_text), n):
            bin_array.append([int(el) for el in new_text[i:i + n]])


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
    layout_matrix = [[Text('Gsys='), Text('Hsys=')],
                     [Table(values=Gsys, headings=[' ' + str(i) + ' ' for i in range(len(Gsys[0]))], max_col_width=20,
                            # background_color='light blue',
                            col_widths=20,
                            justification='center',
                            key='-TABLE-',
                            row_height=25),
                      Table(values=Hsys, headings=[' ' + str(i) + ' ' for i in range(len(Hsys[0]))], max_col_width=20,
                            # background_color='light blue',
                            col_widths=20,
                            justification='center',
                            key='-TABLE-',
                            row_height=25)],
                     [Text('HsysT=')],
                     [Table(values=HsysT, headings=[' ' + str(i) + ' ' for i in range(len(HsysT[0]))], max_col_width=20,
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


def output_modified_matrix(title, matrix, n=None, k=None, dmin=None, t=None):
    layout = [[Text(title)]]
    if n is not None and k is not None:
        layout.append([Text(f'n = {n}, k = {k}')])
    if dmin is not None and t is not None:
        layout.append([Text(f'dmin = {dmin}, t = {t}')])
    layout.append([Table(values=matrix, headings=[' ' + str(i) + ' ' for i in range(len(matrix[0]))], max_col_width=20,
                         # background_color='light blue',
                         col_widths=20,
                         justification='center',
                         key='-TABLE-',
                         row_height=25)])
    layout.append([Button('Назад')])
    window_matrix = Window('Модифицированные матрицы', layout)

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
    layout_const = [[Text(f'k = {k}, n = {n}, p = {p}, t = {t}, dmin = {dmin}')],
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
              [Button('Далее'), Button('Матрицы'), Button('Таблицы'), Button('Константы'), Button('Модификации'),
               Button('Витерби'), Button('binary_to_picture')]]
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
                                                k, n,
                                                HsysT)
            window['output'].update(output_text)

        if event == 'Матрицы':
            output_matrix()

        if event == 'Таблицы':
            output_table()

        if event == 'Константы':
            output_const()

        if event == 'Модификации':
            modify_matrix_window()

        if event == "Витерби":
            main3()

        if event == 'binary_to_picture':
            main4()


def shorten_matrix(matrix, rows, cols):
    """
    Укорачивает матрицу, удаляя строки и столбцы с заданными индексами.
    """
    for row in sorted(rows, reverse=True):
        matrix = [matrix[i] for i in range(len(matrix)) if i != row]
    for col in sorted(cols, reverse=True):
        matrix = [[matrix[i][j] for j in range(len(matrix[i])) if j != col] for i in range(len(matrix))]
    return matrix


def extend_matrix(matrix):
    """
    Расширяет матрицу, добавляя строку сверху и после столбец слева.
    """
    new_row = [1] * len(matrix[0])
    new_matrix = [new_row] + matrix
    for i in range(len(new_matrix)):
        new_matrix[i] = [sum(new_matrix[i]) % 2] + new_matrix[i]
    return new_matrix


def augment_matrix(matrix):
    """
    Пополняет матрицу, добавляя строку сверху.
    """
    new_row = [1] * len(matrix[0])
    new_matrix = [new_row] + matrix
    return new_matrix


def modify_matrix_window():
    layout = [
        [Text('Введите индексы строк для удаления (через пробел):', size=(55, 1)), Input(key='rows')],
        [Text('Введите индексы столбцов для удаления (через пробел):', size=(55, 1)), Input(key='cols')],
        [Button('Укорочение'), Button('Перфорация'), Button('Расширение'), Button('Пополнение')]
    ]
    window = Window('Модификация матрицы', layout)

    while True:
        event, values = window.read()
        if event in (WIN_CLOSED, 'Выход'):
            window.close()
            break
        if event == 'Укорочение':
            try:
                rows = list(map(int, values['rows'].split()))
                cols = list(map(int, values['cols'].split()))
                if len(rows) != len(cols):
                    popup_error('Количество строк и столбцов для удаления должно быть одинаковым.')
                elif len(rows) == len(Gsys) or len(cols) == len(Gsys[0]):
                    popup_error('Матрица не может содержать ни строк, ни столбцов после удаления.')
                else:
                    modified_Gsys = shorten_matrix(Gsys.copy(), rows, cols)
                    n = len(modified_Gsys[0])
                    k = len(modified_Gsys)
                    dmin, t = calculate_dmin_t(modified_Gsys)
                    window.close()
                    output_modified_matrix('Gsys_yk =', modified_Gsys, n, k, dmin, t)
                    break
            except ValueError:
                popup_error('Введите корректные значения для строк и столбцов.')
        elif event == 'Перфорация':
            try:
                rows = list(map(int, values['rows'].split()))
                cols = list(map(int, values['cols'].split()))
                if len(rows) != len(cols):
                    popup_error('Количество строк и столбцов для удаления должно быть одинаковым.')
                elif len(rows) == len(Hsys) or len(cols) == len(Hsys[0]):
                    popup_error('Матрица не может содержать ни строк, ни столбцов после удаления.')
                else:
                    modified_Hsys = shorten_matrix(Hsys.copy(), rows, cols)
                    n = len(modified_Hsys[0])
                    k = len(modified_Hsys)
                    modified_Hsys_to_Gsys = get_system_new(modified_Hsys, n, k)
                    dmin, t = calculate_dmin_t(modified_Hsys_to_Gsys)
                    window.close()
                    output_modified_matrix('Hsys_pr =', modified_Hsys_to_Gsys, n, k, dmin, t)
                    break
            except ValueError:
                popup_error('Введите корректные значения для строк и столбцов.')
        elif event == 'Расширение':
            modified_Hsys = extend_matrix(Hsys.copy())
            n = len(modified_Hsys[0])
            k = len(modified_Hsys)
            window.close()
            output_modified_matrix('Hext =', modified_Hsys, n, k)
            break
        elif event == 'Пополнение':
            modified_Gsys = augment_matrix(Gsys.copy())
            n = len(modified_Gsys[0])
            k = len(modified_Gsys)
            window.close()
            output_modified_matrix('Gext =', modified_Gsys, n, k)
            break


def calculate_dmin_t(matrix):
    """
    Вычисляет dmin и t для матрицы.
    """
    k = len(matrix)
    gen_array_i()
    vector_array_c = [mul_matrix(matrix, i) for i in gen_array_i_new(k)]
    wh_array = [str(vector_array_c[inde]).count('1') for inde in range(1, len(vector_array_c))]
    dmin = min(wh_array)
    t = (dmin - 1) // 2
    return dmin, t


def main2():
    start_window()
    get_matrix()
    get_sys_matrix()
    gen_array_i()
    gen_array_c_and_dmin_t_p()
    gen_HsysT()
    gen_e_array()
    gen_S_array()
    Encoding_and_Decoding_Window()


# def text_to_binary(text: str) -> str:
#     """
#     Переводит текст в двоичную строку (UTF-8)
#     :param text: текст
#     :return: двоичная строка"""
#     return ''.join(f"{byte:08b}" for byte in text.encode('utf-8'))
#
#
# def binary_to_text(binary_string: str) -> str:
#     """
#     Переводит двоичную строку обратно в текст (UTF-8)
#     :param binary_string: двоичная строка
#     :return: текст
#     """
#     byte_array = bytearray(int(binary_string[i:i + 8], 2) for i in range(0, len(binary_string), 8))
#     return byte_array.decode('utf-8', errors='ignore')  # Пропускает ошибки


def convolutional_encode(input_bits: str, polynomials: List[Tuple[int, ...]]) -> str:
    """
    Свёрточное кодирование
    :param input_bits: входящие биты
    :param polynomials: полиномы
    :return: закодированные биты
    """
    if not input_bits:
        return ''

    max_register: int = max(max(tup) for tup in polynomials)
    shift_register: list = [0] * (max_register + 1)
    encoded_data: list = []

    for bit in input_bits:
        shift_register.insert(0, int(bit))
        shift_register.pop()

        for tup in polynomials:
            xor: int = sum(shift_register[index] for index in tup) % 2
            encoded_data.append(str(xor))

    return ''.join(encoded_data)


def viterbi_decode(encoded_bits: str, polynomials: List[Tuple[int, ...]]) -> str:
    """
    Алгоритм Витерби
    :param encoded_bits: закодированные биты
    :param polynomials: полиномы
    :return: декодированные биты
    """
    if not encoded_bits:
        return ''

    bit_outputs: int = len(polynomials)
    max_register: int = max(max(tup) for tup in polynomials)
    count_bit_states: int = 2 ** max_register
    states: list = [format(i, f'0{max_register}b') for i in range(count_bit_states)]

    path_metrics: dict = {s: float('inf') for s in states}
    path_metrics['0' * max_register] = 0
    paths: dict = {s: [] for s in states}

    for step in range(0, len(encoded_bits) // bit_outputs):
        current_bits: str = encoded_bits[step * bit_outputs: (step + 1) * bit_outputs]
        new_metrics: dict = {s: float('inf') for s in states}
        new_paths: dict = {s: [] for s in states}

        for state in states:
            if path_metrics[state] == float('inf'):
                continue
            for input_bit in ['0', '1']:
                next_state: str = (input_bit + state)[:-1]
                shift_register: list = list(map(int, input_bit + state))

                expected_bits_list: list = []
                for tup in polynomials:
                    xor: int = sum(shift_register[index] for index in tup) % 2
                    expected_bits_list.append(str(xor))
                expected_str = ''.join(expected_bits_list)

                hammings_weight: int = sum(
                    1
                    for bit_in_current_bits, bit_in_expected_str in zip(current_bits, expected_str)
                    if bit_in_current_bits != bit_in_expected_str
                )
                total_hammings_weight: int = path_metrics[state] + hammings_weight

                if total_hammings_weight < new_metrics[next_state]:
                    new_metrics[next_state] = total_hammings_weight
                    new_paths[next_state] = paths[state] + [input_bit]

        path_metrics, paths = new_metrics, new_paths

    final_state: int = min(path_metrics, key=path_metrics.get)
    result = ''.join(paths[final_state])
    return result[:len(encoded_bits) // len(polynomials)]


def create_layout():
    """
    Создает графический интерфейс
    :return:
    """
    layout = [
        [sg.Text('Регистры для каждого сумматора (через запятую, разделенные новой строкой):')],
        [sg.Multiline(size=(80, 10), key='summators')],
        [sg.Text('Последовательность для кодирования:'), sg.InputText(key='sequence')],
        [sg.Button('Кодировать'), sg.Button('Декодировать'), sg.Button('Пример')],
        [sg.Text('Результат:')],
        [sg.Output(size=(80, 20))]
    ]
    return layout


def validate_input(values):
    """
    Проверка корректности входных данных
    """
    errors = []

    # Проверка содержимого + длины строки
    sequence = values['sequence'].strip()
    if not sequence:
        errors.append("Строка не может быть пустой!")
    if len(sequence) > 10000:
        errors.append("Строка слишком длинная! Максимальная длина 1000 символов.")

    # Проверка сумматоров
    summators_input = values['summators'].strip().split('\n')

    # Проверка формата строки сумматоров
    for i, sum_line in enumerate(summators_input, 1):
        sum_line = sum_line.strip()
        if not sum_line:
            continue

        # Проверка формата строки с помощью регулярного выражения
        if not re.match(r'^\d+(,\s*\d+)+$', sum_line):
            errors.append(f"Сумматор {i}: некорректный формат! Используйте числа через запятую.")
            continue

        try:
            numbers = [int(x.strip()) for x in sum_line.split(',')]
            if not numbers:
                errors.append(f"Сумматор {i}: пустая строка!")
            if any((number < 0 or number > 15) for number in numbers):
                errors.append(f"Сумматор {i}: числа не могут быть отрицательными, а также больше 15!")
            if len(numbers) > 10:
                errors.append(f"Сумматор {i}: слишком много регистров! Максимальное число регистров 10!")
        except ValueError:
            errors.append(f"Сумматор {i}: некорректные значения!")

    return errors


def show_example(window):
    """
    Показывает пример использования программы
    """
    example_text = "Привет123@#$%HelloWelt!456"
    summators = [
        "1,0",
        "1,1",
        "1,2"
    ]

    window['sequence'].update(example_text)
    window['summators'].update('\n'.join(summators))

    # Демонстрация кодирования
    print("=== Пример кодирования ===")
    print(f"Входная строка: {example_text}")
    print("\nСумматоры:")
    for i, sum in enumerate(summators, 1):
        print(f"Сумматор {i}: {sum}")

    # binary_data = text_to_binary(example_text)
    # print(f"\nДвоичный формат: {binary_data}")

    # Демонстрация декодирования
    print("\n=== Пример декодирования ===")
    encoded_data = convolutional_encode(example_text, [tuple(map(int, s.split(','))) for s in summators])
    print(f"Закодированные данные: {encoded_data}")

    decoded_data = viterbi_decode(encoded_data, [tuple(map(int, s.split(','))) for s in summators])
    print(f"Декодированные данные (бинарный вид): {decoded_data}")


def main3():
    sg.theme('DarkAmber')
    layout = create_layout()
    window = sg.Window('Сверточное кодирование и декодирование', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Кодировать':
            errors = validate_input(values)
            if errors:
                sg.popup_error('\n'.join(errors), title='Ошибка!')
                continue

            try:
                summators_input: list = [line.replace('\n', '').strip()
                                         for line in values['summators'].strip().split('\n')]
                summators: list = [tuple(map(int, line.split(','))) for line in summators_input if line]

                # Проверка на уникальность сумматоров (независимо от порядка)
                # unique_summators = set(frozenset(s) for s in summators)
                # if len(unique_summators) != len(summators):
                #     sg.popup_error('Сумматоры должны быть уникальными (независимо от порядка регистров).')
                #     continue

                sequence: str = values['sequence']

                if re.fullmatch(r'[01]+', sequence):  # проверка на ввод бинарной строки
                    binary_data: str = sequence
                else:
                    binary_data: str = sequence

                encoded_data: str = convolutional_encode(binary_data, summators)
                print(f"Закодированные данные: {encoded_data}")
            except Exception as e:
                sg.popup_error(f'Ошибка при кодировании: {e}')

        elif event == 'Декодировать':
            errors = validate_input(values)
            if errors:
                sg.popup_error('\n'.join(errors), title='Ошибка!')
                continue

            try:
                summators_input: list = [line.replace('\n', '').strip()
                                         for line in values['summators'].strip().split('\n')]
                summators: list = [tuple(map(int, line.split(','))) for line in summators_input if line]

                # Проверка на уникальность сумматоров (независимо от порядка)
                # unique_summators = set(frozenset(s) for s in summators)
                # if len(unique_summators) != len(summators):
                #     sg.popup_error('Сумматоры должны быть уникальными (независимо от порядка регистров).')
                #     continue

                encoded_sequence: str = values['sequence']

                decoded_data: str = viterbi_decode(encoded_sequence, summators)
                print(f"Декодированные данные (бинарный вид): {decoded_data}")
                decoded_text: str = decoded_data
                print()
            except Exception as e:
                sg.popup_error(f'Ошибка при декодировании: {e}')

        elif event == 'Пример':
            show_example(window)

    window.close()


def create_layout_main4():
    """
    Создает графический интерфейс
    :return:
    """
    layout = [
        [Text('Бинарная строка:', size=(15, 1)), Input(key='binary')],
        [Text('Путь к картинке:', size=(15, 1)), Input(key='path_to_picture')],
        [Button('Преобразовать'), Button('Выход')]
    ]
    return layout


def main4():
    sg.theme('DarkAmber')
    layout = create_layout_main4()
    window = sg.Window('В картинку', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Преобразовать':
            binary_data = values['binary']
            path_to_picture = values['path_to_picture']
            binary_to_image(binary_data, path_to_picture)
            #
            # # Open the image
            # image = Image.open(image_path)
            # # Convert the image to a numpy array of pixels
            # pixel_array = np.array(image)
            # # Convert pixel values to binary (8 bits)
            # binary_array = np.unpackbits(np.array(pixel_array, dtype=np.uint8), axis=-1)
            # # Reshape binary array to have 8-bit chunks
            # binary_string = ''.join(''.join(map(str, array)) for chunk in binary_array for array in chunk)
            # print(binary_string)
        elif event == 'Выход':
            exit()

    window.close()


if __name__ == '__main__':
    main1()

if __name__ == '__main__':
    main2()
