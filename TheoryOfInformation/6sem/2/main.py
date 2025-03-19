import PySimpleGUI as sg
from typing import List, Tuple
import re


def text_to_binary(text: str) -> str:
    """Переводит текст в двоичную строку (ASCII)"""
    return ''.join(f"{ord(c):08b}" for c in text)


def binary_to_text(binary_string: str) -> str:
    """Переводит двоичную строку обратно в текст (ASCII)"""
    chars: list = []
    for i in range(0, len(binary_string), 8):
        byte: str = binary_string[i:i + 8]
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)


def convolutional_encode(input_bits: str, polynomials: List[Tuple[int, ...]]) -> str:
    """Свёрточное кодирование"""
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
    """Алгоритм Витерби"""
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
    layout = [
        [sg.Text('Регистры для каждого сумматора (через запятую, разделенные новой строкой):')],
        [sg.Multiline(size=(80, 10), key='summators')],
        [sg.Text('Последовательность для кодирования:'), sg.InputText(key='sequence')],
        [sg.Button('Кодировать'), sg.Button('Декодировать')],
        [sg.Text('Результат:')],
        [sg.Output(size=(80, 20))]
    ]
    return layout


def main():
    layout = create_layout()

    window = sg.Window('Сверточное кодирование и декодирование', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'Кодировать':
            try:
                summators_input: str = values['summators'].strip().split('\n')

                summators: list = [tuple(map(int, line.split(','))) for line in summators_input]

                # Проверка на уникальность сумматоров (независимо от порядка)
                # unique_summators = set(frozenset(s) for s in summators)
                # if len(unique_summators) != len(summators):
                #     sg.popup_error('Сумматоры должны быть уникальными (независимо от порядка регистров).')
                #     continue

                sequence: str = values['sequence']

                if re.fullmatch(r'[01]+', sequence):
                    binary_data: str = sequence
                else:
                    binary_data: str = text_to_binary(sequence)

                encoded_data: str = convolutional_encode(binary_data, summators)
                print(f"Закодированные данные: {encoded_data}")
            except Exception as e:
                sg.popup_error(f'Ошибка при кодировании: {e}')

        if event == 'Декодировать':
            try:
                summators_input: str = values['summators'].strip().split('\n')

                summators: list = [tuple(map(int, line.split(','))) for line in summators_input]

                # Проверка на уникальность сумматоров (независимо от порядка)
                # unique_summators = set(frozenset(s) for s in summators)
                # if len(unique_summators) != len(summators):
                #     sg.popup_error('Сумматоры должны быть уникальными (независимо от порядка регистров).')
                #     continue

                encoded_sequence: str = values['sequence']

                decoded_data: str = viterbi_decode(encoded_sequence, summators)
                print(f"Декодированные данные (в бинарном виде): {decoded_data}")
                decoded_text: str = binary_to_text(decoded_data)
                print(f"Декодированные данные (не в бинарном виде): {decoded_text}")
                print()
            except Exception as e:
                sg.popup_error(f'Ошибка при декодировании: {e}')

    window.close()


if __name__ == "__main__":
    main()
