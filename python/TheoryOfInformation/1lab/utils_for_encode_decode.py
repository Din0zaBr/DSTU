import os
import ast
from tkinter import messagebox
from bisect import bisect_left


def check_file_existence(file_path):
    if not os.path.isfile(file_path):
        messagebox.showerror('Ошибка', 'Файл не существует')
        return False
    return True


def confirm_operation(operation):
    return messagebox.askyesno('Подтверждение', f'Вы уверены, что хотите {operation} этот файл?')


def huffman_encode(file_path):
    if not check_file_existence(file_path):
        return
    if not confirm_operation('закодировать'):
        return

    with open(file_path, 'r') as file:
        data = file.read()

    try:
        ver = []
        sp_zn = []
        data = data.lower()

        # Подсчет частоты символов
        for i in data:
            if i not in sp_zn:
                ver.append(1)
                sp_zn.append(i)
            else:
                ind = sp_zn.index(i)
                ver[ind] += 1

        dl = len(data)
        ver = [x / dl for x in ver]

        # Сортировка по убыванию частоты
        for i in range(len(ver) - 1):
            for j in range(i + 1, len(sp_zn)):
                if ver[i] < ver[j]:
                    ver[i], ver[j] = ver[j], ver[i]
                    sp_zn[i], sp_zn[j] = sp_zn[j], sp_zn[i]

        k = len(sp_zn)
        sl = {}

        # Построение кодов Хаффмана
        for i in range(k - 1):
            summ = ver[-1] + ver[-2]
            ver = ver[:(len(ver) - 2)]
            ver.reverse()
            ind = bisect_left(ver, summ)
            ver.insert(ind, summ)
            ver.reverse()

            for char in sp_zn[-1]:
                sl[char] = sl.get(char, '') + '0'
            for char in sp_zn[-2]:
                sl[char] = sl.get(char, '') + '1'

            st = sp_zn[-1] + sp_zn[-2]
            sp_zn = sp_zn[:(len(sp_zn) - 2)]
            sp_zn.reverse()
            sp_zn.insert(ind, st)
            sp_zn.reverse()

        # Обратное преобразование кодов
        for k in sl.keys():
            sl[k] = sl[k][::-1]

        encoded_text = str(sl) + "n"
        for i in data:
            encoded_text += sl[i]

        encoded_file_path = os.path.join(os.path.dirname(file_path),
                                         os.path.splitext(os.path.basename(file_path))[0] + '_Huffman_encoded' +
                                         os.path.splitext(os.path.basename(file_path))[-1])
        with open(encoded_file_path, 'w') as file:
            file.write(encoded_text)

        return encoded_text  # Возвращаем результат для дальнейшего использования

    except Exception as e:
        print(f"Произошла ошибка при открытии файла: {str(e)}")
        return None


def huffman_decode(file_path):
    if not check_file_existence(file_path):
        return
    if not confirm_operation('декодировать'):
        return

    with open(file_path, 'r') as file:
        text = file.read()

    try:
        sl, stroka = text.split('n')
        sl = ast.literal_eval(sl)
        sl1 = {value: key for key, value in sl.items()}
        decoded_text = ''
        current = ''

        # Декодирование
        for i in stroka:
            current += i
            if current in sl1:
                decoded_text += sl1[current]
                current = ''

        encoded_file_path = os.path.join(os.path.dirname(file_path),
                                         os.path.splitext(os.path.basename(file_path))[0] + '_Huffman_decoded' +
                                         os.path.splitext(os.path.basename(file_path))[-1])
        with open(encoded_file_path, 'w') as file:
            file.write(decoded_text)

        return decoded_text

    except Exception as e:
        print(f"Введён неверный формат зашифрованного текста: {str(e)}")
        return None


def lz77_encode(file_path, window_size=20):
    if not check_file_existence(file_path):
        return
    if not confirm_operation('закодировать'):
        return

    with open(file_path, 'r') as file:
        data = file.read()
    encoded_text = []
    i = 0
    while i < len(data):
        match_length = 0
        match_offset = 0
        lookahead_buffer = data[i:i + window_size]  # Окно просмотра вперед
        search_buffer = data[max(0, i - window_size):i]  # Окно поиска
        for j in range(len(search_buffer)):
            length = 0
            while (length < len(lookahead_buffer) and
                   j + length < len(search_buffer) and
                   search_buffer[j + length] == lookahead_buffer[length]):
                length += 1
            if length > match_length:
                match_length = length
                match_offset = len(search_buffer) - j
        if match_length > 0:
            encoded_text.append((match_offset, match_length, lookahead_buffer[match_length]))
            i += match_length + 1
        else:
            encoded_text.append((0, 0, data[i]))
            i += 1

    encoded_file_path = os.path.join(os.path.dirname(file_path),
                                     os.path.splitext(os.path.basename(file_path))[0] + '_LZ77_encoded' +
                                     os.path.splitext(os.path.basename(file_path))[-1])
    with open(encoded_file_path, 'w') as file:
        file.write(str(encoded_text))
    return encoded_text


def lzw_encode(file_path):
    if not check_file_existence(file_path):
        return
    if not confirm_operation('закодировать'):
        return

    with open(file_path, 'r') as file:
        data = file.read()

    data = data.lower()
    sp_zn = []

    # Сбор уникальных символов
    for i in data:
        if i not in sp_zn:
            sp_zn.append(i)

    # Создание словаря для кодирования
    sl = {x: sp_zn.index(x) for x in sp_zn}

    num = len(sl)
    current = data[0]
    cur_str = ''
    it_str = ''
    cur_str = current

    # Основная логика алгоритма LZW
    for i in data[1:]:
        next = i
        if (cur_str + next) not in sl:
            sl[cur_str + next] = num
            num += 1
            it_str += str(sl[cur_str]) + ' '
            current = next
            cur_str = current
        else:
            current = next
            cur_str += next

    sl[cur_str + "-"] = num
    it_str += str(sl[cur_str])

    # Формирование результата
    encoded_text = str(sl) + '\n' + it_str.strip()
    encoded_file_path = os.path.join(os.path.dirname(file_path),
                                     os.path.splitext(os.path.basename(file_path))[0] + '_LWS_encoded' +
                                     os.path.splitext(os.path.basename(file_path))[-1])
    with open(encoded_file_path, 'w') as file:
        file.write(encoded_text)

    print(encoded_text)
