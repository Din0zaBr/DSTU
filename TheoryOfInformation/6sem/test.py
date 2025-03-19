import PySimpleGUI as sg

def text_to_binary(text):
    """Переводит текст в двоичную строку (ASCII)"""
    return ''.join(f"{ord(c):08b}" for c in text)

def binary_to_text(binary_str):
    """Переводит двоичную строку обратно в текст (ASCII)"""
    chars = []
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i + 8]
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def convolutional_encode(input_bits, polynomials) -> str:
    """Сверточное кодирование"""
    if not input_bits:
        return ''

    max_register = max(max(tup) for tup in polynomials)
    switch = [0] * (max_register + 1)
    encoded_data = []

    for bit in input_bits:
        switch.insert(0, int(bit))
        switch.pop()

        for tup in polynomials:
            xor = sum(switch[index] for index in tup) % 2
            encoded_data.append(str(xor))

    return ''.join(encoded_data)

def viterbi_decode(encoded_bits, polynomials) -> str:
    """Алгоритм Витерби"""
    if not encoded_bits:
        return ''

    bit_outputs = len(polynomials)
    max_register = max(max(tup) for tup in polynomials)
    count_bit_states = 2 ** max_register
    states = [format(i, f'0{max_register}b') for i in range(count_bit_states)]

    path_metrics = {s: float('inf') for s in states}
    path_metrics['0' * max_register] = 0
    paths = {s: [] for s in states}

    for step in range(0, len(encoded_bits) // bit_outputs):
        current_bits = encoded_bits[step * bit_outputs: (step + 1) * bit_outputs]
        new_metrics = {s: float('inf') for s in states}
        new_paths = {s: [] for s in states}

        for state in states:
            if path_metrics[state] == float('inf'):
                continue
            for input_bit in ['0', '1']:
                next_state = (input_bit + state)[:-1]
                switch = list(map(int, input_bit + state))

                expected_bits_list = []
                for tup in polynomials:
                    xor = sum(switch[index] for index in tup) % 2
                    expected_bits_list.append(str(xor))
                expected_str = ''.join(expected_bits_list)

                hammings_weight = sum(
                    1
                    for bit_in_current_bits, bit_in_expected_str in zip(current_bits, expected_str)
                    if bit_in_current_bits != bit_in_expected_str
                )
                total_hammings_weight = path_metrics[state] + hammings_weight

                if total_hammings_weight < new_metrics[next_state]:
                    new_metrics[next_state] = total_hammings_weight
                    new_paths[next_state] = paths[state] + [input_bit]

        path_metrics, paths = new_metrics, new_paths

    final_state = min(path_metrics, key=path_metrics.get)
    result = ''.join(paths[final_state])
    return result[:len(encoded_bits) // len(polynomials)]

def create_layout():
    layout = [
        [sg.Text('Количество сумматоров:'), sg.InputText(key='num_summators')],
        [sg.Text('Регистры для каждого сумматора (через запятую, разделенные новой строкой):')],
        [sg.Multiline(size=(40, 10), key='summators')],
        [sg.Text('Последовательность для кодирования:'), sg.InputText(key='sequence')],
        [sg.Button('Кодировать'), sg.Button('Декодировать')],
        [sg.Text('Результат:')],
        [sg.Output(size=(80, 20))]
    ]
    return layout

def main():
    max_summators = 10
    layout = create_layout()

    window = sg.Window('Сверточное кодирование и декодирование', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'Кодировать':
            try:
                num_summators = int(values['num_summators'])
                if num_summators > max_summators:
                    sg.popup_error(f'Максимальное количество сумматоров: {max_summators}')
                    continue

                summators_input = values['summators'].strip().split('\n')
                if len(summators_input) != num_summators:
                    sg.popup_error(
                        f'Количество введенных сумматоров ({len(summators_input)}) не совпадает с указанным количеством ({num_summators}).')
                    continue

                summators = [tuple(map(int, line.split(','))) for line in summators_input]

                # Проверка на уникальность сумматоров (независимо от порядка)
                # unique_summators = set(frozenset(s) for s in summators)
                # if len(unique_summators) != len(summators):
                #     sg.popup_error('Сумматоры должны быть уникальными (независимо от порядка регистров).')
                #     continue

                sequence = values['sequence']

                if all(c in '01' for c in sequence):
                    binary_data = sequence
                else:
                    binary_data = text_to_binary(sequence)

                encoded_data = convolutional_encode(binary_data, summators)
                print(f"Закодированные данные: {encoded_data}")
            except Exception as e:
                sg.popup_error(f'Ошибка при кодировании: {e}')

        if event == 'Декодировать':
            try:
                num_summators = int(values['num_summators'])
                if num_summators > max_summators:
                    sg.popup_error(f'Максимальное количество сумматоров: {max_summators}')
                    continue

                summators_input = values['summators'].strip().split('\n')
                if len(summators_input) != num_summators:
                    sg.popup_error(
                        f'Количество введенных сумматоров ({len(summators_input)}) не совпадает с указанным '
                        f'количеством ({num_summators}).')
                    continue

                summators = [tuple(map(int, line.split(','))) for line in summators_input]

                # Проверка на уникальность сумматоров (независимо от порядка)
                # unique_summators = set(frozenset(s) for s in summators)
                # if len(unique_summators) != len(summators):
                #     sg.popup_error('Сумматоры должны быть уникальными (независимо от порядка регистров).')
                #     continue

                encoded_sequence = values['sequence']

                decoded_data = viterbi_decode(encoded_sequence, summators)
                decoded_text = binary_to_text(decoded_data)
                print(f"Декодированные данные: {decoded_text}")
            except Exception as e:
                sg.popup_error(f'Ошибка при декодировании: {e}')

    window.close()

if __name__ == "__main__":
    main()
