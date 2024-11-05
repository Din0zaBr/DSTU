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
        file_content = file.read()

    char_frequencies = []
    unique_characters = []
    file_content = file_content.lower()

    for char in file_content:
        if char not in unique_characters:
            char_frequencies.append(1)
            unique_characters.append(char)
        else:
            index = unique_characters.index(char)
            char_frequencies[index] += 1
    # вычисляю общую длину текста и нормализую частоты,
    # деля каждую частоту на общую длину текста, чтобы получить долю каждого символа
    total_length = len(file_content)
    char_frequencies = [freq / total_length for freq in char_frequencies]

    # Сортировка по убыванию частоты
    for i in range(len(char_frequencies) - 1):
        for j in range(i + 1, len(unique_characters)):
            if char_frequencies[i] < char_frequencies[j]:
                char_frequencies[i], char_frequencies[j] = char_frequencies[j], char_frequencies[i]
                unique_characters[i], unique_characters[j] = unique_characters[j], unique_characters[i]

    num_unique_chars = len(unique_characters)
    huffman_codes = {}
    # Мы останавливаемся на num_unique_chars - 1,
    # потому что в итоге останется только один символ, который будет корнем дерева Хаффмана
    for i in range(num_unique_chars - 1):
        # Два символа с наим. частотой
        combined_frequency = char_frequencies[-1] + char_frequencies[-2]
        char_frequencies = char_frequencies[:(len(char_frequencies) - 2)]
        # переворачиваем список, чтобы легче было найти место для вставки новой частоты.
        char_frequencies.reverse()
        # используем бинарный поиск для нахождения индекса,
        # где новая частота должна быть вставлена, чтобы сохранить порядок по возрастанию.
        insert_index = bisect_left(char_frequencies, combined_frequency)
        char_frequencies.insert(insert_index, combined_frequency)
        # снова переворачиваем список обратно в исходный порядок
        char_frequencies.reverse()
        # комбинирую их и продолжаю процесс до тех пор, пока не останется один символ.

        # проходим по всем символам, которые были объединены
        for char in unique_characters[-1]:
            # присваиваем им код '0'. Если символ уже имеет код, мы добавляем '0' к существующему коду.
            huffman_codes[char] = huffman_codes.get(char, '') + '0'
        for char in unique_characters[-2]:
            huffman_codes[char] = huffman_codes.get(char, '') + '1'

        # создаем новую строку, которая представляет собой комбинацию двух последних символов.
        combined_chars = unique_characters[-1] + unique_characters[-2]
        unique_characters = unique_characters[:(len(unique_characters) - 2)]
        unique_characters.reverse()
        unique_characters.insert(insert_index, combined_chars)
        # вставляем новую строку в список на найденное ранее место.
        unique_characters.reverse()

    #  После завершения алгоритма инвертирую коды Хаффмана, чтобы они соответствовали правильному формату
    #  (короткие коды для более частых символов).
    for key in huffman_codes.keys():
        huffman_codes[key] = huffman_codes[key][::-1]

    encoded_text = str(huffman_codes) + "n"
    for char in file_content:
        encoded_text += huffman_codes[char]

    encoded_file_path = os.path.join(os.path.dirname(file_path),
                                     os.path.splitext(os.path.basename(file_path))[0] + '_Huffman_encoded' +
                                     os.path.splitext(os.path.basename(file_path))[-1])
    with open(encoded_file_path, 'w') as file:
        file.write(encoded_text)


def huffman_decode(file_path):
    if not check_file_existence(file_path):
        return
    if not confirm_operation('декодировать'):
        return

    with open(file_path, 'r') as encoded_file:
        encoded_text = encoded_file.read()

    try:
        code_dict_str, encoded_string = encoded_text.split('n')
        # Преобразует строку, представляющую словарь, в настоящий словарь Python
        code_dictionary = ast.literal_eval(code_dict_str)

        # ключи - закодированные строки, а значения — исходные символы
        reverse_code_dictionary = {value: key for key, value in code_dictionary.items()}

        decoded_text = ''
        current_code = ''

        # Декодирование
        for char in encoded_string:
            current_code += char
            if current_code in reverse_code_dictionary:
                # добавляет соответствующий символ в decoded_text
                decoded_text += reverse_code_dictionary[current_code]
                current_code = ''

        decoded_file_path = os.path.join(
            os.path.dirname(file_path),
            os.path.splitext(os.path.basename(file_path))[0] + '_Huffman_decoded' +
            os.path.splitext(os.path.basename(file_path))[-1]
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

    encoded_output = []  # Список для хранения закодированных данных
    current_index = 0  # Текущий индекс в данных

    while current_index < len(input_data):
        match_length = 0
        match_offset = 0

        # Буфер - все символы перед текущим индексом
        search_buffer = input_data[:current_index]

        # Поиск совпадений
        for search_index in range(len(search_buffer)):
            # Проверяем, совпадает ли символ в текущем индексе с символом в поисковом окне
            if search_buffer[search_index] == input_data[current_index]:
                # Находим длину совпадения
                temp_length = 0
                while (search_index + temp_length < len(search_buffer) and
                       current_index + temp_length < len(input_data) and
                       search_buffer[search_index + temp_length] == input_data[current_index + temp_length]):
                    temp_length += 1

                # Если длина совпадения больше, чем текущее максимальное совпадение, обновляем
                if temp_length > match_length:
                    match_length = temp_length
                    match_offset = len(search_buffer) - search_index

        # Если найдено совпадение, добавляем его в выходной список
        if match_length > 0:
            next_char = input_data[current_index + match_length] if current_index + match_length < len(
                input_data) else ''
            encoded_output.append((match_offset, match_length, next_char))
            current_index += match_length + 1
        else:
            # Если совпадение не найдено, добавляем текущий символ
            encoded_output.append((0, 0, input_data[current_index]))
            current_index += 1

    # Формирование пути для сохранения закодированного файла
    encoded_file_path = os.path.join(
        os.path.dirname(input_file_path),
        os.path.splitext(os.path.basename(input_file_path))[0] + '_LZ77_encoded' +
        os.path.splitext(os.path.basename(input_file_path))[-1]
    )

    # Запись закодированных данных в файл
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
