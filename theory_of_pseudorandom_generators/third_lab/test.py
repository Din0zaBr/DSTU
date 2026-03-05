import numpy as np
def parse_polynomial(poly_str):
    poly_str = poly_str.replace(' ', '').replace('-', '+-')
    terms = poly_str.split('+')
    degrees = []
    for term in terms:
        if term == '1':
            degrees.append(0)
        elif 'x^' in term:
            degrees.append(int(term.split('^')[1]))
        elif term == 'x':
            degrees.append(1)
    N = max(degrees)
    coeffs = [0] * N
    for d in degrees:
        if d > 0:
            coeffs[N - d] = 1
    return coeffs, N
def build_transition_matrix(coeffs):
    N = len(coeffs)
    T = np.zeros((N, N), dtype=int)
    for i in range(N - 1):
        T[i][i + 1] = 1
    T[N - 1] = coeffs
    return T
def lfsr_matrix(poly_str, shift_k, initial_state=None):
    coeffs, N = parse_polynomial(poly_str)
    T = build_transition_matrix(coeffs)
    V = np.linalg.matrix_power(T, shift_k) % 2
    print(f"\nМногочлен: {poly_str}")
    print(f"Коэффициенты: {coeffs}")
    print(f"Длина регистра: {N}")
    print(f"Сдвиг k = {shift_k}")
    print(f"\nМатрица перехода T:\n{T}")
    print(f"\nМатрица V = T^{shift_k}:\n{V}")
    if initial_state is None:
        state = np.array([1] + [0] * (N - 1), dtype=int)
        print(f"\nНачальное состояние по умолчанию: {state.tolist()}")
    else:
        if len(initial_state) != N:
            print(f"Ошибка: длина начального состояния должна быть {N}")
            return
        state = np.array(initial_state, dtype=int).flatten()
    history = []
    sequence = []
    print("\nПромежуточные состояния:")
    while list(state) not in history:
        history.append(list(state))
        sequence.append(state[0])
        print(''.join(map(str, state)))
        state = V.dot(state) % 2
    print("\nГенерация завершена.")
    print(f"Фактический период: {len(history)}")
    print(f"Максимально возможный период: {2**N - 1}")
    if len(history) == 2**N - 1:
        print("Получен максимальный период.")
    else:
        print("Период меньше максимального.")
    while True:
        try:
            reg_index = int(input(f"\nВведите номер регистра (от 1 до {N}), который вывести: "))
            if 1 <= reg_index <= N:
                break
            else:
                print(f"Введите число от 1 до {N}.")
        except ValueError:
            print(" Введите целое число.")

    selected_column = [int(state[reg_index - 1]) for state in history]
    print(f"\nЗначения регистра q{reg_index}(t):")
    print(selected_column)
    return sequence
default_poly = "x^5 + x^3 + 1"
default_k = 2
default_state = [1, 0, 0, 0, 0]
poly_str = input(f"Введите примитивный многочлен [по умолчанию: {default_poly}]: ").strip()
if not poly_str:
    poly_str = default_poly
shift_k_input = input(f"Введите сдвиг k [по умолчанию: {default_k}]: ").strip()
shift_k = int(shift_k_input) if shift_k_input else default_k
initial_input = input("Введите начальное состояние (например: 1 0 0 0 0 или 10000), или Enter для значения по умолчанию: ").strip()
if initial_input:
    try:
        if ' ' in initial_input:
            initial_state = list(map(int, initial_input.split()))
        else:
            initial_state = [int(b) for b in initial_input.strip()]
    except ValueError:
        print("Ошибка: допустимы только 0 и 1.")
        exit()
else:
    initial_state = default_state
lfsr_matrix(poly_str, shift_k, initial_state)
