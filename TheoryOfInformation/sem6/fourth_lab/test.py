# g_x = list(G[0])  # первая строка матрицы G - это g(x)
# g_x = [int(i) for i in g_x]
def gf2_polynomial_division(
        dividend,
        divisor
):
    """
    Делит полином dividend на divisor в поле GF(2).

    Параметры
    ----------
    dividend : Sequence[int]
        Список бит полинома от старшей степени к младшей (len = n).
    divisor : Sequence[int]
        Список бит порождающего полинома от старшей степени к младшей (len = m+1).

    Возвращает
    -------
    quotient : List[int]
        Коэффициенты частного (len = n-m+1).
    remainder : List[int]
        Остаток степени < m (len = m).
    """
    while divisor[-1] == 0:
        divisor.pop()
    divisor = divisor[::-1]
    print(f'divisor', divisor)
    dividend = dividend[::-1]
    print(f'dividend', dividend)

    a = list(dividend)
    n, m = len(a), len(divisor)
    if n < m:
        return [0], a.copy()

    quotient = [0] * (n - m + 1)
    for i in range(n - m + 1):
        if a[i]:
            quotient[i] = 1
            # вычитание в GF(2) = XOR
            for j in range(m):
                a[i + j] ^= divisor[j]
    # остаток — последние m бит
    remainder = a[-m:] if m > 0 else []
    return quotient[::-1], remainder[::-1]


def multiply_by_x(polynomial):
    """
    Умножает полином на x в поле GF(2).
    """
    length_pol = len(polynomial)
    while len(polynomial) < 7:
        polynomial.append(0)
    res = [0] + polynomial[:-1]
    res = res[:length_pol]
    return res


g_x = [1, 1, 0, 1, 0, 0, 0]
print(g_x)

# bin_array = []
# for i in range(0, len(text), n):
#     bin_array.append([int(el) for el in text[i:i + n]])  # c-шечки все
output_text_temp = ''

bin_array = [[1, 1, 0, 0, 1, 1, 0]]
e_array = [[0, 0, 0, 1, 0, 0, 0]]
S_array = [[0, 0, 1, 1]]
i_array = [[0, 0, 0, 0],
           [0, 0, 0, 1],
           [0, 0, 1, 0],
           [0, 0, 1, 1],
           [0, 1, 0, 0],
           [0, 1, 0, 1],
           [0, 1, 1, 0],
           [0, 1, 1, 1],
           [1, 0, 0, 0],
           [1, 0, 0, 1],
           [1, 0, 1, 0],
           [1, 0, 1, 1],
           [1, 1, 0, 0],
           [1, 1, 0, 1],
           [1, 1, 1, 0],
           [1, 1, 1, 1]]
c_array = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 1], [0, 0, 1, 1, 0, 1, 0], [0, 0, 1, 0, 1, 1, 1],
           [0, 1, 1, 0, 1, 0, 0], [0, 1, 1, 1, 0, 0, 1], [0, 1, 0, 1, 1, 1, 0], [0, 1, 0, 0, 0, 1, 1],
           [1, 1, 0, 1, 0, 0, 0], [1, 1, 0, 0, 1, 0, 1], [1, 1, 1, 0, 0, 1, 0], [1, 1, 1, 1, 1, 1, 1],
           [1, 0, 1, 1, 1, 0, 0], [1, 0, 1, 0, 0, 0, 1], [1, 0, 0, 0, 1, 1, 0], [1, 0, 0, 1, 0, 1, 1]]
# c_array = [1, 1, 0, 0, 1, 1, 0]
# # Пример использования функции для вычисления Si(x)
# S_1 = gf2_polynomial_division(c_array, g_x)[1]  # Пример 1ого синдрома, получится x^2, т.е. [0, 0, 1, 0]
# print(S_1)
#
# # Умножение остатка на x
# temp_x = multiply_by_x(S_1) # = x^2
# print("Результат умножения на x:", temp_x)
# print()
# S_2 = gf2_polynomial_division(temp_x, g_x)[1] # x^2 mod g(x) = x^2
# print("S_2(x) = ", S_2)
# print()
#
# # Умножение остатка ещё раз на x
# temp_x = multiply_by_x(temp_x) # = x^3
# print("Результат умножения на x:", temp_x)
# print()
# S_3 = gf2_polynomial_division(temp_x, g_x)[1] # x^3 mod g(x) = x + 1, т.е. [1, 1, 0, 0]
# print("S_3(x) = ", S_3)
# print()

for el in bin_array:
    print(el)
    print(gf2_polynomial_division(el, g_x))
    S_1 = gf2_polynomial_division(el, g_x)[1]
    print(f'S_1(x) = ', S_1)
    x = [0 for i in range(len(el))]
    x[1] = 1
    print(x)
    for i in range(1, len(el)):
        print(f"i={i}", "="*20)
        print("Результат умножения на x:", x, "=", multiply_by_x(S_1))
        S_i = gf2_polynomial_division(multiply_by_x(S_1), g_x)
        print(S_i)
        print(S_array)
        if S_i in S_array:
            index_S = i
            print("index_S = ", index_S)
            e_new = [0 for i in range(len(el) - index_S)]
            e_new[-1] = 1
            print()
            print(f'e_new = ', e_new)
            xn_1 = [0 for i in range(len(el))]
            xn_1[0] = 1
            print()
            print(f'xn_1 = ', xn_1)
            print()
            e_new_new = gf2_polynomial_division(e_new, xn_1)[1]
            print(f'e_new_new = ', e_new_new)
            c_x = el + e_new_new
            print(c_x)
#             S_temp_index = S_array.index(S_i)
#             e_temp = e_array[S_temp_index]
#             for index_el in range(len(el)):
#                 el[index_el] = el[index_el] ^ e_temp[index_el]
#             index_i = c_array.index([int(i) for i in el])
#             output_text_temp += ''.join([str(i) for i in i_array[index_i]])
#             x = multiply_by_x(x)
#         else:
#             index_i = c_array.index(el)
#             output_text_temp += ''.join([str(i) for i in i_array[index_i]])
#             x = multiply_by_x(x)
#
# binary_word = ''.join(map(str, [int(i) for i in output_text_temp]))
#
# bity_chunks = [binary_word[i:i + 8] for i in range(len(binary_word) % 8, len(binary_word), 8)]
#
# byte_array = bytearray(int(byte, 2) for byte in bity_chunks)
#
# output_text = ''.join(char for char in byte_array.decode('utf-8') if char.isprintable())
#
# print(output_text)
