import heapq
import os
from tkinter import messagebox


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
        text = file.read()

    frequency = {char: text.count(char) for char in set(text)}
    heap = [[weight, [char, ""]] for char, weight in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    huffman_table = dict(heapq.heappop(heap)[1:])
    encoded_text = ''.join(huffman_table[char] for char in text)

    encoded_file_path = os.path.join(os.path.dirname(file_path),
                                     os.path.splitext(os.path.basename(file_path))[0] + '_huffman' +
                                     os.path.splitext(os.path.basename(file_path))[-1])
    with open(encoded_file_path, 'w') as file:
        file.write(encoded_text)

    print('Huffman coding table:')
    sorted_huffman_table = sorted(huffman_table.items(), key=lambda x: x[1])
    for char, code in sorted_huffman_table:
        print(f'{char}: {code}')


def huffman_decode(file_path):
    if not check_file_existence(file_path):
        return
    if not confirm_operation('декодировать'):
        return

    with open(file_path, 'r') as file:
        encoded_text = file.read()

    huffman_table = {}
    with open(os.path.splitext(file_path)[0], 'r') as file:
        for line in file:
            char, code = line.strip().split(': ')
            huffman_table[code] = char

    decoded_text = ''
    current_code = ''
    for bit in encoded_text:
        current_code += bit
        if current_code in huffman_table:
            decoded_text += huffman_table[current_code]
            current_code = ''

    decoded_file_path = os.path.join(os.path.dirname(file_path),
                                     os.path.splitext(os.path.basename(file_path))[0] + 'Huffman_decoded' +
                                     os.path.splitext(os.path.basename(file_path))[-1])
    with open(decoded_file_path, 'w') as file:
        file.write(decoded_text)

    print('Decoded text:')
    print(decoded_text)


def lz77_encode(file_path):
    if not check_file_existence(file_path):
        return
    if not confirm_operation('закодировать'):
        return

    with open(file_path, 'r') as file:
        data = file.read()
    # window_size = 12
    # while i < len(data):
    #     match_length = 0
    #     match_distance = 0
    #     next_char = data[i]
    #
    #     # Define the search window
    #     start_window = max(0, i - window_size)
    #     search_buffer = data[start_window:i]
    #
    #     # Try to find the longest match
    #     for j in range(len(search_buffer)):
    #         length = 0
    #         while (length < len(data) - i and
    #                search_buffer[j:j + length + 1] == data[i:i + length + 1]):
    #             length += 1
    #
    #         # Update the best match if found
    #         if length >= match_length:
    #             match_length = length
    #             match_distance = len(search_buffer) - j
    #             if i + match_length < len(data):
    #                 next_char = data[i + match_length]
    #             else:
    #                 next_char = ''
    #
    #             # Append (distance, length, next character) tuple
    #     if match_length > 0:
    #         compressed_data.append((match_distance, match_length, next_char))
    #         i += match_length + 1
    #     else:
    #         compressed_data.append((0, 0, next_char))
    #         i += 1
    # print(compressed_data)
    pass

def lzw_encode(file_path):
    if not check_file_existence(file_path):
        return
    if not confirm_operation('закодировать'):
        return

    with open(file_path, 'r') as file:
        data = file.read()

    data = data.lower()  # Приведение к нижнему регистру
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

    sl[cur_str + "@"] = num
    it_str += str(sl[cur_str])

    # Формирование результата
    encoded_text = str(sl) + '\n' + it_str.strip()
    encoded_file_path = os.path.join(os.path.dirname(file_path),
                                     os.path.splitext(os.path.basename(file_path))[0] + '_LWS_encoded' +
                                     os.path.splitext(os.path.basename(file_path))[-1])
    with open(encoded_file_path, 'w') as file:
        file.write(encoded_text)

    print(encoded_text)

