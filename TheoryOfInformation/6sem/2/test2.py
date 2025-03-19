def text_to_binary(text: str) -> str:
    """Переводит текст в двоичную строку (ASCII)"""
    return ''.join(f"{ord(c):08b}" for c in text)

# Пример использования
binary_data = text_to_binary("12a")
print(binary_data)  # Ожидаемый вывод: 001100010011001001100001

def convolutional_encode(input_bits: str, polynomials) -> str:
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

# Пример использования
polynomials = [(0, 1, 2), (0, 2)]
encoded_data = convolutional_encode(binary_data, polynomials)
print(encoded_data)  # Ожидаемый вывод: закодированная строка

def viterbi_decode(encoded_bits: str, polynomials) -> str:
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

# Пример использования
decoded_data = viterbi_decode(encoded_data, polynomials)
print(decoded_data)  # Ожидаемый вывод: декодированная строка

def binary_to_text(binary_string: str) -> str:
    """Переводит двоичную строку обратно в текст (ASCII)"""
    chars: list = []
    for i in range(0, len(binary_string), 8):
        byte: str = binary_string[i:i + 8]
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

# Пример использования
decoded_text = binary_to_text(decoded_data)
print(decoded_text)  # Ожидаемый вывод: "12a"
