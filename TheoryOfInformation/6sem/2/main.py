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
        for poly in polynomials:
            # print(poly)
            # print(switch)
            xor: int = 0
            for index in poly:
                xor ^= switch[index]
            encoded_data.append(str(xor))

    return ''.join(encoded_data)


def viterbi_decode(encoded_bits, polynomials) -> str:
    """Алгоритм Витерби"""
    if not encoded_bits:
        return ''
    # Количество выходных битов за один такт равно количеству полиномов, используемых в свёрточном кодере.
    n_outputs: int = len(polynomials)

    max_register: int = max(max(tup) for tup in polynomials)
    # Определяем количество состояний (n_states), которое равно 2^max_register
    #  , где max_register — это максимальная длина регистра, используемого в полиномах.
    n_states: int = 2 ** max_register

    # Например, если у нас есть 2 регистра, то возможные состояния могут быть представлены как
    # 00, 01, 10, 11
    states: list = [format(i, f'0{max_register}b') for i in range(n_states)]

    # Создаем словарь path_metrics, который хранит метрики путей для каждого состояния.
    # - начальная метрика для состояния '0' * max_register устанавливается в 0
    # - для всех остальных состояний — в бесконечность (float('inf')).
    path_metrics: dict = {s: float('inf') for s in states}
    path_metrics['0' * max_register] = 0

    # Словарь paths хранит пути (последовательности битов), которые ведут к каждому состоянию.
    # Эти пути представляют собой последовательности входных битов, которые привели к текущему состоянию кодера.
    # В конце алгоритма Витерби мы используем этот словарь,
    # чтобы восстановить наиболее вероятную последовательность исходных битов.
    paths: dict = {s: [] for s in states}

    # Закодированные данные: 11010100
    # n_outputs 2
    # max_register 2
    # n_states 4
    # states ['00', '01', '10', '11']
    # path_metrics {'00': 0, '01': inf, '10': inf, '11': inf}
    # paths {'00': [], '01': [], '10': [], '11': []}
    for step in range(0, len(encoded_bits) // n_outputs):

        # Для каждого шага (step) извлекаем текущие биты (current_bits) из закодированной последовательности.
        current_bits: list = encoded_bits[step * n_outputs: (step + 1) * n_outputs]  # срезы 0:2 , 2:4, 4:6
        print(current_bits)

        # Создаем новые словари new_metrics и new_paths для хранения обновленных метрик и путей.
        new_metrics: dict = {s: float('inf') for s in states}
        print(f'new_metrics', new_metrics)
        new_paths: dict = {s: [] for s in states}
        print(f'new_paths', new_paths)

        # Для каждого состояния (state) и каждого возможного входного бита (input_bit):
        print(path_metrics)
        for state in states:
            if path_metrics[state] == float('inf'):
                continue
            print(f'!!!state!!!', state)
            for input_bit in ['0', '1']:

                # Вычисляем следующее состояние (next_state)
                next_state: str = (input_bit + state)[:-1]
                print(f'next_state', next_state)
                tmp_registers: list = list(map(int, input_bit + state))
                print(f'tmp_registers', tmp_registers)

                # Вычисляем ожидаемые выходные биты (expected) для текущего состояния и входного бита.
                expected = []
                for poly in polynomials:
                    xor = sum(tmp_registers[idx] for idx in poly) % 2
                    expected.append(str(xor))
                expected_str = ''.join(expected)
                print(f'expected_str', expected_str)

                # Вычисляем метрику Хэмминга (metric) между ожидаемыми и фактическими битами.
                metric: int = sum(1 for a, b in zip(current_bits, expected_str) if a != b)
                print(f'metric', metric)
                # Обновляем метрику пути (total_metric) как сумму текущей метрики пути и метрики Хэмминга.
                total_metric: int = path_metrics[state] + metric
                print(f'total_metric', total_metric)
                # Если новая метрика меньше текущей метрики для следующего состояния, обновляем метрику и путь.
                if total_metric < new_metrics[next_state]:
                    new_metrics[next_state] = total_metric
                    new_paths[next_state] = paths[state] + [input_bit]

        # Обновляем path_metrics и paths новыми значениями
        path_metrics, paths = new_metrics, new_paths
        print(path_metrics, paths)

    # Находим состояние с минимальной метрикой (final_state).
    final_state: int = min(path_metrics, key=path_metrics.get)

    # Восстанавливаем последовательность исходных битов (result) из пути, ведущего к этому состоянию.
    result = ''.join(paths[final_state])

    return result[:len(encoded_bits) // len(polynomials)]


def main():
    raw_data: str = input("Введите текст или двоичную строку для кодирования: ")
    polynom: tuple = ((0, 2, 3), (1, 2), (0, 3))

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
