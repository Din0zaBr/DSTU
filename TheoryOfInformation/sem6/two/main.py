import PySimpleGUI as sg
from typing import List, Tuple
import re


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


def main():
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


if __name__ == "__main__":
    main()