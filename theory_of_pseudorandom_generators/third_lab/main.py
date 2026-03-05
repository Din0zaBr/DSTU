import numpy as np
import datetime


def generate_matrix(poly_taps, n, k):
    """Строит матрицу перехода LFSR и возводит её в степень k (mod 2)."""
    matrix = np.zeros((n, n), dtype=int)
    # Сдвиг: следующая строка получает значение предыдущей ячейки
    for i in range(n - 1):
        matrix[i + 1][i] = 1
    # Обратные связи по тапам примитивного многочлена
    for tap in poly_taps:
        matrix[0][tap - 1] = 1
    return np.linalg.matrix_power(matrix, k) % 2


def lfsr_sequence(seed, matrix, length, output_bit_index):
    """Генерирует последовательность бит по LFSR с данной матрицей и выходным битом."""
    state = np.array(seed, dtype=int)
    output = []
    seen = []
    # Пошаговый вывод: каждое состояние регистра на каждом такте
    print("\nПромежуточные состояния (пошагово):")
    for _ in range(length):
        key = tuple(state)
        if key in seen:
            break
        seen.append(key)
        output.append(state[output_bit_index])
        print(state)  # этап: текущее состояние перед переходом
        state = np.dot(matrix, state) % 2
    print("Генерация завершена.")
    return output


def main():
    # Ввод параметров (пустой Enter — подстановка значений по умолчанию)
    default_poly = "5 3 1"   # x^5 + x^3 + 1 -> порядок 5, тапы 3 и 1
    default_k = 2
    default_seed = "1 0 0 0 0"
    default_out_bit = 1

    poly_input = input(f"Коэффициенты примитивного многочлена [по умолчанию {default_poly}]: ").strip() or default_poly
    k_input = input(f"Сдвиг k [по умолчанию {default_k}]: ").strip()
    k = int(k_input) if k_input else default_k
    seed_input = input(f"Начальное состояние [по умолчанию {default_seed}]: ").strip() or default_seed
    out_bit_input = input(f"Номер выходного бита (1..n) [по умолчанию {default_out_bit}]: ").strip()
    output_bit = (int(out_bit_input) if out_bit_input else default_out_bit) - 1

    poly_taps = list(map(int, poly_input.split()))
    n = poly_taps[0]
    seed = list(map(int, seed_input.split()))
    T_max = 2 ** n - 1

    # Проверка длины начального состояния
    if len(seed) != n:
        print("Ошибка: длина начального состояния должна быть равна порядку многочлена:", n)
        return

    # Построение матрицы перехода в степени k
    matrix = generate_matrix(poly_taps[1:], n, k)
    print(f"\nМатрица перехода в степени {k}:")
    print(matrix)

    # Генерация последовательности с пошаговым выводом состояний
    sequence = lfsr_sequence(seed, matrix, T_max, output_bit)
    period = len(sequence)

    # Итоги: последовательность и период
    print("\nСгенерированная последовательность:", sequence)
    print("Фактический период:", period)
    print("Максимальный период (2^n - 1):", T_max)
    if period == T_max:
        print("Период максимальный.")
    else:
        print("Период не максимальный.")

    # Сохранение последовательности в файл с временной меткой
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"lfsr_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(sequence))
    print(f"\nПоследовательность сохранена в {filename}")


if __name__ == "__main__":
    main()
