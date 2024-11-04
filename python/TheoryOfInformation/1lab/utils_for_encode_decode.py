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
    for char, code in huffman_table.items():
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
    pass


def lzw_encode(file_path):
    if not check_file_existence(file_path):
        return
    if not confirm_operation('закодировать'):
        return
    pass
