import numpy as np

def image_to_binary(pixel_array):
    """
    Преобразует массив пикселей в бинарный формат и кодирует его методом блочного кода.
    """
    # Преобразуем значения пикселей в бинарный вид (8 бит)
    binary_array = np.unpackbits(np.array(pixel_array, dtype=np.uint8), axis=-1)

    # Reshape binary array to have 8-bit chunks
    binary_array = binary_array.reshape(-1, 8)

    # Конвертируем каждый 8-битный чанк в строку
    hex_array = [''.join(map(str, chunk)) for chunk in binary_array]

    # Преобразуем массив строк в одну длинную строку
    binary_string = ''.join(hex_array)
    return binary_string

def main():
    encoded_text = image_to_binary(array)
    print("Encoded Text:", encoded_text)

array = np.array(
    [[[21, 22, 17],
      [17, 18, 13],
      [25, 24, 19],
      [56, 52, 49],
      [56, 53, 48],
      [56, 53, 48]],

     [[24, 25, 20],
      [17, 18, 13],
      [21, 20, 15],
      [56, 52, 49],
      [55, 52, 47],
      [55, 52, 47]]])

main()
