import numpy as np
import datetime


def generate_matrix(poly_taps, n, k):
    matrix = np.zeros((n, n), dtype=int)
    for i in range(n - 1):
        matrix[i + 1][i] = 1
    for tap in poly_taps:
        matrix[0][tap - 1] = 1
    matrix_power = np.linalg.matrix_power(matrix, k) % 2
    return matrix_power


def fibonacci_lfsr_from_matrix(seed, matrix, length, output_bit):
    state = np.array(seed, dtype=int)
    output = []
    seen_states = []
    for _ in range(length):
        if any(np.array_equal(state, s) for s in seen_states):
            break
        seen_states.append(state.copy())
        output.append(state[output_bit])
        print(state)
        state = np.dot(matrix, state) % 2

    return output


poly_input = input("Введите коэффициенты примитивного многочлена через пробел: ")
k = int(input("Введите сдвиг k: "))
seed_input = input("Введите начальное состояние через пробел: ")
output_bit = int(input("Введите индекс выходного бита: ")) - 1
poly_taps = list(map(int, poly_input.split()))
n = poly_taps[0]
seed = list(map(int, seed_input.split()))
T = 2 ** n - 1
if len(seed) != n:
    raise ValueError("Длина начального состояния должна соответствовать порядку многочлена.")

matrix = generate_matrix(poly_taps[1:], n, k)
print(f"Матрица перехода в степени {k}:")
print(matrix)
print("Диаграмма:")
sequence = fibonacci_lfsr_from_matrix(seed, matrix, T, output_bit)
print("Сгенерированная последовательность:", sequence)
print("Максимальный период последовательности:", T)
print("Период данной последователности максимален" if len(
    sequence) == T else "Период данной последователности не является максимальным")
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"{timestamp}.txt"
with open(filename, "w", encoding="utf-8") as file:
    file.write(str(sequence))
