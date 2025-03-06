def text_to_binary(text):
    """Переводит текст в двоичную строку (ASCII)"""
    return ''.join(f"{ord(c):08b}" for c in text)


def convolutional_encode(input_bits, polynomials):
    """Сверточное кодирование"""
    if not input_bits:
        return ''
    print(input_bits)

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
            xor = 0
            for index in poly:
                xor ^= switch[index]
            encoded_data.append(str(xor))

    return ''.join(encoded_data)


raw_data: str = input()
#  i to bin
polynom = ((0, 1, 2), (0, 2))

# Определение типа входных данных
if all(c in '01' for c in raw_data):
    binary_data = raw_data
else:
    binary_data = text_to_binary(raw_data)

print(convolutional_encode(binary_data, polynom))
