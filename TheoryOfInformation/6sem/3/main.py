import os
import numpy as np
from PIL import Image
import PySimpleGUI as sg


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
    image = Image.open(image_path)
    # Convert the image to a numpy array of pixels
    pixel_array = np.array(image)
    # Convert pixel values to binary (8 bits)
    binary_array = np.unpackbits(np.array(pixel_array, dtype=np.uint8), axis=-1)
    # Reshape binary array to have 8-bit chunks
    binary_array = binary_array.reshape(-1, 8)
    # Convert each 8-bit chunk to a hexadecimal string
    hex_array = [''.join(map(str, chunk)) for chunk in binary_array]

    # Encode the hexadecimal array using Huffman coding
    return hex_array
def main():
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
                encoded_text, huffman_dict, image = image_to_binary(image_path)
                window['binary_array'].update(encoded_text[:1000])  # Display first 1000 characters of encoded text
            else:
                sg.popup_error('Ошибка', 'Файл не найден или путь некорректен.')

    window.close()

if __name__ == '__main__':
    main()
