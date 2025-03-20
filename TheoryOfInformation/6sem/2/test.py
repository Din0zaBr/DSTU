def text_to_binary(text):
    """Переводит текст в двоичную строку (ASCII)"""
    return ''.join(f"{ord(c):08b}" for c in text)


def convolutional_encode(input_bits, polynomials) -> str:
    """Сверточное кодирование"""
    if not input_bits:
        return ''
    # print(input_bits)

    max_register: int = max(max(tup) for tup in polynomials)
    switch: list = [0] * (max_register + 1)
    # print(switch)
    encoded_data: list = []

    # реализация движения по коммутатору
    for bit in input_bits:
        switch.insert(0, int(bit))
        switch.pop()
        # print(switch)

        # реализация xor по каждому полиному
        for tup in polynomials:
            # print(tup)
            # print(switch)
            xor = sum(switch[index] for index in tup) % 2
            encoded_data.append(str(xor))

    return ''.join(encoded_data)


def viterbi_decode(encoded_bits, polynomials) -> str:
    """Алгоритм Витерби"""
    if not encoded_bits:
        return ''
    # Количество выходных битов за один такт равно количеству полиномов, используемых в свёрточном кодере.
    # Другими словами, результат битов от каждого сумматора
    bit_outputs: int = len(polynomials)

    max_register: int = max(max(tup) for tup in polynomials)

    # Определяем количество состояний (count_bit_states), которое равно 2^max_register
    #  , где max_register — это максимальная длина регистра, используемого в полиномах.
    count_bit_states: int = 2 ** max_register

    # Например, если у нас есть 2 регистра, то возможные состояния могут быть представлены как: 00, 01, 10, 11
    # число i должно быть представлено в двоичном виде (b) с дополнением нулями до длины max_register.
    states: list = [format(i, f'0{max_register}b') for i in range(count_bit_states)]

    # Создаем словарь path_metrics, который хранит метрики путей для каждого состояния.
    path_metrics: dict = {s: float('inf') for s in states}
    path_metrics['0' * max_register] = 0

    # Словарь paths хранит пути (последовательности битов), которые ведут к каждому состоянию.
    # Эти пути представляют собой последовательности входных битов, которые привели к текущему состоянию кодера.
    # В конце алгоритма Витерби мы используем этот словарь,
    # чтобы восстановить наиболее вероятную последовательность исходных битов.
    paths: dict = {s: [] for s in states}

    # Закодированные данные: 11010100
    # bit_outputs 2
    # max_register 2
    # bit_states 4
    # states ['00', '01', '10', '11']
    # path_metrics {'00': 0, '01': inf, '10': inf, '11': inf}
    # paths {'00': [], '01': [], '10': [], '11': []}

    # на блоки
    for step in range(0, len(encoded_bits) // bit_outputs):

        current_bits: list = encoded_bits[step * bit_outputs: (step + 1) * bit_outputs]
        print()
        print(f'------------------- current_bits:', current_bits, '-------------------')
        print()

        # Создаем новые словари new_metrics и new_paths для хранения обновленных метрик и путей.
        new_metrics: dict = {s: float('inf') for s in states}
        print(f'new_metrics', new_metrics)
        new_paths: dict = {s: [] for s in states}
        print(f'new_paths', new_paths)

        # Для каждого состояния (state) и каждого возможного входного бита (input_bit):
        print(f'path_metrics', path_metrics)
        for state in states:
            if path_metrics[state] == float('inf'):
                continue
            print(f'!!!state!!!', state)
            for input_bit in ['0', '1']:
                print()
                print("for input_bit", input_bit)
                # вычисляем следующее состояние, добавляя входной бит к текущему состоянию и удаляя последний бит.
                next_state: str = (input_bit + state)[:-1]
                print(f'next_state', next_state)
                switch: list = list(map(int, input_bit + state))
                print(f'switch', switch)

                # Вычисляем ожидаемые выходные биты (expected_bits_list) для текущего состояния и входного бита.
                expected_bits_list: list = []
                for tup in polynomials:
                    print(f'tup', tup)
                    xor = sum(switch[index] for index in tup) % 2
                    expected_bits_list.append(str(xor))
                expected_str = ''.join(expected_bits_list)
                print(f'expected_str {expected_str} ({current_bits})')

                # Вычисляем метрику Хэмминга (hammings_weight) между ожидаемыми и фактическими битами.
                hammings_weight: int = sum(
                    1
                    for bit_in_current_bits, bit_in_expected_str in zip(current_bits, expected_str)
                    if bit_in_current_bits != bit_in_expected_str
                )
                print(f'hammings_weight', hammings_weight)
                # Обновляем метрику пути (total_hammings_weight) как сумму текущей метрики пути и метрики Хэмминга.
                total_hammings_weight: int = path_metrics[state] + hammings_weight
                print(f'total_hammings_weight', total_hammings_weight)
                # Если новая метрика меньше текущей метрики для следующего состояния, обновляем метрику и путь.
                if total_hammings_weight < new_metrics[next_state]:
                    new_metrics[next_state] = total_hammings_weight
                    new_paths[next_state] = paths[state] + [input_bit]

        # Обновляем path_metrics и paths новыми значениями
        path_metrics, paths = new_metrics, new_paths
        print()
        print(f'path_metrics', path_metrics)
        print(f'paths', paths)
        print("Обновили", step)

    # Находим состояние с минимальной метрикой).
    final_state: int = min(path_metrics, key=path_metrics.get)

    # Восстанавливаем последовательность исходных битов (result) из пути, ведущего к этому состоянию.
    result = ''.join(paths[final_state])
    print(result)
    return result[:len(encoded_bits) // len(polynomials)]


def main():
    raw_data: str = input("Введите текст или двоичную строку для кодирования: ")
    polynom: tuple = ((1, 2), (0, 2))

    # Определение типа входных данных
    if all(c in '01' for c in raw_data):
        binary_data = raw_data
    else:
        binary_data = text_to_binary(raw_data)

    encoded_data: str = convolutional_encode(binary_data, polynom)
    print(f"Закодированные данные: {encoded_data}")

    decoded_data: str = viterbi_decode(encoded_data, polynom)
    print(f"Декодированные данные: {decoded_data}")


if __name__ == "__main__":
    main()
