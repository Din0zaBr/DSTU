import heapq
import os
import collections
from tkinter import messagebox
import ast


def check_file_existence(file_path):
    if not os.path.isfile(file_path):
        messagebox.showerror('Ошибка', 'Файл не существует')
        return False
    return True


def confirm_operation(operation):
    return messagebox.askyesno('Подтверждение', f'Вы уверены, что хотите {operation} этот файл?')


class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(frequency):
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(left=left, right=right, freq=left.freq + right.freq)
        heapq.heappush(heap, merged)
    return heap[0]


def build_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}
    if node is not None:
        if node.char is not None:
            code_map[node.char] = prefix
        build_codes(node.left, prefix + "0", code_map)
        build_codes(node.right, prefix + "1", code_map)
    return code_map


def huffman_encode(file_path):
    if not check_file_existence(file_path):
        return
    if not confirm_operation('закодировать'):
        return

    with open(file_path, 'r') as file:
        file_content = file.read()

    frequency = collections.Counter(file_content)
    huffman_tree = build_huffman_tree(frequency)
    huffman_codes = build_codes(huffman_tree)

    encoded_text = ''.join(huffman_codes[char] for char in file_content)

    encoded_file_path = os.path.join(os.path.dirname(file_path),
                                     os.path.splitext(os.path.basename(file_path))[0] + '_Huffman_encoded.txt')
    with open(encoded_file_path, 'w') as file:
        file.write(str(huffman_codes) + "\n" + encoded_text)


def huffman_decode(file_path):
    if not check_file_existence(file_path):
        return
    if not confirm_operation('декодировать'):
        return

    with open(file_path, 'r') as encoded_file:
        encoded_text = encoded_file.read()

    try:
        code_dict_str, encoded_string = encoded_text.split('\n', 1)
        code_dictionary = ast.literal_eval(code_dict_str)

        reverse_code_dictionary = {v: k for k, v in code_dictionary.items()}

        decoded_text = ''
        current_code = ''

        for bit in encoded_string:
            current_code += bit
            if current_code in reverse_code_dictionary:
                decoded_text += reverse_code_dictionary[current_code]
                current_code = ''

        decoded_file_path = os.path.join(
            os.path.dirname(file_path),
            os.path.splitext(os.path.basename(file_path))[0] + '_Huffman_decoded.txt'
        )

        with open(decoded_file_path, 'w') as decoded_file:
            decoded_file.write(decoded_text)

        return decoded_text

    except Exception as error:
        print(f"Введён неверный формат зашифрованного текста: {str(error)}")
        messagebox.showerror('Ошибка', 'В файле неверный формат зашифрованного текста')
        return None


def lz77_encode(input_file_path):
    if not check_file_existence(input_file_path):
        return
    if not confirm_operation('закодировать'):
        return

    with open(input_file_path, 'r') as input_file:
        input_data = input_file.read()

    encoded_output = []
    current_index = 0

    while current_index < len(input_data):
        match_length = 0
        match_offset = 0

        search_buffer = input_data[:current_index]

        for search_index in range(len(search_buffer)):
            if search_buffer[search_index] == input_data[current_index]:
                temp_length = 0
                while (search_index + temp_length < len(search_buffer) and
                       current_index + temp_length < len(input_data) and
                       search_buffer[search_index + temp_length] == input_data[current_index + temp_length]):
                    temp_length += 1

                if temp_length > match_length:
                    match_length = temp_length
                    match_offset = len(search_buffer) - search_index

        if match_length > 0:
            next_char = input_data[current_index + match_length] if current_index + match_length < len(
                input_data) else ''
            encoded_output.append((match_offset, match_length, next_char))
            current_index += match_length + 1
        else:
            encoded_output.append((0, 0, input_data[current_index]))
            current_index += 1

    encoded_file_path = os.path.join(
        os.path.dirname(input_file_path),
        os.path.splitext(os.path.basename(input_file_path))[0] + '_LZ77_encoded.txt'
    )

    with open(encoded_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(str(encoded_output))

    return encoded_output


def lzw_encode(file_path):
    if not check_file_existence(file_path):
        return
    if not confirm_operation('закодировать'):
        return

    with open(file_path, 'r') as file:
        data = file.read()

    data = data.lower()
    sp_zn = []

    for i in data:
        if i not in sp_zn:
            sp_zn.append(i)

    sl = {x: sp_zn.index(x) for x in sp_zn}

    num = len(sl)
    current = data[0]
    cur_str = ''
    it_str = ''
    cur_str = current

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

    encoded_text = str(sl) + '\n' + it_str.strip()
    encoded_file_path = os.path.join(os.path.dirname(file_path),
                                     os.path.splitext(os.path.basename(file_path))[0] + '_LZW_encoded.txt')
    with open(encoded_file_path, 'w') as file:
        file.write(encoded_text)

    print(encoded_text)
