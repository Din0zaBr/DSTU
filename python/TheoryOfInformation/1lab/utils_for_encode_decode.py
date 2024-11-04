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
    # Read the file and calculate frequency of each character
    with open(file_path, 'r') as file:
        text = file.read()
    frequency = {}
    for char in text:
        if char not in frequency:
            frequency[char] = 0
        frequency[char] += 1

    # Build the Huffman tree
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

    # Create the Huffman coding table
    huffman_table = dict(heapq.heappop(heap)[1:])

    # Encode the text
    encoded_text = ''
    for char in text:
        encoded_text += huffman_table[char]

    # Save the encoded text to a file
    with open(file_path + '.huffman', 'w') as file:
        file.write(encoded_text)

    # Print the Huffman coding table
    print('Huffman coding table:')
    for char, code in huffman_table.items():
        print(f'{char}: {code}')


def huffman_decode(file_path):
    # Read the encoded text from the file
    with open(file_path, 'r') as file:
        encoded_text = file.read()

    # Build the Huffman decoding table
    huffman_table = {}
    with open(os.path.splitext(file_path)[0], 'r') as file:
        for line in file:
            char, code = line.strip().split(': ')
            huffman_table[code] = char

    # Decode the text
    decoded_text = ''
    current_code = ''
    for bit in encoded_text:
        current_code += bit
        if current_code in huffman_table:
            decoded_text += huffman_table[current_code]
            current_code = ''

    # Save the decoded text to a file
    with open(os.path.splitext(file_path)[0] + '.decoded', 'w') as file:
        file.write(decoded_text)

    # Print the decoded text
    print('Decoded text:')
    print(decoded_text)


def lz77_encode(file_path):
    pass


def lzw_encode(file_path):
    pass
