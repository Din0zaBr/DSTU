from TchKa.first_lab.sixth import binary_euclid, final
from TchKa.third_lab.sixth import fi


def normalize_modulo(value, modulus):
    """Нормализует значение по модулю, приводя к диапазону [0, modulus)."""
    return value % modulus


def normalize_values_by_moduli(values, moduli):
    """Нормализует список значений по соответствующим модулям."""
    return [normalize_modulo(values[i], moduli[i]) for i in range(len(values))]


def normalize_moduli_list(moduli):
    """Приводит все модули к положительным значениям."""
    return [abs(m) for m in moduli]


def mod_inverse_by_euler(a, m):
    phi_m = fi(m)
    print(f"φ({m}) = {phi_m}")
    a_normalized = normalize_modulo(a, m)
    if a_normalized != a:
        print(f"Нормализуем основание: {a} mod {m} = {a_normalized}")
    degree = phi_m - 1
    print(f"a^(-1) ≡ a^(φ(m)-1) = {a_normalized}^({phi_m}-1) = {a_normalized}^{degree} (mod {m})")
    return pow(a_normalized, degree, m)


def solve_single_congruence(a, b, m):
    """
    Решает одно сравнение ax ≡ b (mod m).

    Алгоритм:
    1. Нормализует модуль и свободный член (приводит к положительным)
    2. Вычисляет НОД(a, m) = d с помощью бинарного алгоритма Евклида
    3. Проверяет делимость b на d - если не делится, решений нет
    4. Делит сравнение на d: (a/d)x ≡ (b/d) (mod m/d) при НОД > 1
    5. Находит обратный элемент по теореме Эйлера
    6. Приводит линейное сравнение к пригодному сравнению для китайской теоремы

    Возвращает: (с, возможно_новый_модуль, НОД) или None если решений нет
    """
    original_a, original_b, original_m = a, b, m

    m = abs(m)
    b = normalize_modulo(b, m)

    a_check, m_check, degree_2 = binary_euclid(abs(a), m)
    gcd = final(a_check, m_check, degree_2)

    print(f"Сравнение: {original_a}x ≡ {original_b} (mod {original_m})")
    print(f"НОД({abs(a)}, {m}) = {gcd} → количество решений = {gcd}")

    if b % gcd != 0:
        print(f"{b} не делится на {gcd} - решений нет\n")
        return None

    new_a = a // gcd
    new_b = b // gcd
    new_m = m // gcd
    print(f"Приводим к виду: x ≡ сᵢ (mod mᵢ)")

    new_a = normalize_modulo(new_a, new_m)

    print(f"\nИспользуем теорему Эйлера для нахождения обратного элемента:")
    inverse_result = mod_inverse_by_euler(new_a, new_m)

    c = normalize_modulo(inverse_result * new_b, new_m)
    print(f"x_0 ≡ {inverse_result} * {new_b} ≡ {c} (mod {new_m})")
    print(f"Пригодное сравнение для Китайской теоремы: x ≡ {c} (mod {new_m})\n")

    return c, new_m, gcd


def check_gcds(moduli):
    n = len(moduli)
    moduli = normalize_moduli_list(moduli)
    for i in range(n):
        for j in range(i + 1, n):
            a_check, b_check, degree_2 = binary_euclid(moduli[i], moduli[j])
            gcd = final(a_check, b_check, degree_2)
            if gcd != 1:
                print(f"Модули {moduli[i]} и {moduli[j]} не взаимно просты, НОД = {gcd}")
                return False
    return True


def solve_system_of_congruences(remainders, moduli):
    """
    Решает систему сравнений методом китайской теоремы об остатках.

    Алгоритм:
    1. Нормализует модули и остатки (приводит к положительным)
    2. Проверяет попарную взаимную простоту модулей
    3. Если модули не взаимно просты - система не имеет решения
    4. Вычисляет произведение всех модулей M
    5. Для каждого модуля вычисляет Mᵢ = M / mᵢ
    6. Находит обратные элементы Nᵢ = Mᵢ^(-1) mod mᵢ по теореме Эйлера
    7. Вычисляет базовое решение: x = Σ(aᵢ * Mᵢ * Nᵢ) mod M

    Возвращает: (базовое_решение, модуль)
    """
    if len(remainders) != len(moduli):
        raise ValueError("Количество остатков должно равняться количеству модулей")

    moduli = normalize_moduli_list(moduli)
    remainders = normalize_values_by_moduli(remainders, moduli)

    n = len(moduli)

    print("Проверка попарной взаимной простоты модулей:")
    if not check_gcds(moduli):
        print("Модули не попарно взаимно просты - система не имеет решения.")
        return None, None
    else:
        print("Все модули попарно взаимно просты.\n")

    M = 1
    for m in moduli:
        M *= m
    print(f"Произведение всех модулей M = {M}\n")

    M_i = []
    for i in range(n):
        M_i_value = M // moduli[i]
        M_i.append(M_i_value)
        print(f"M_{i + 1} = M / m_{i + 1} = {M} / {moduli[i]} = {M_i_value}")
    print()

    N_i = []
    for i in range(n):
        print(f"\nНаходим обратный элемент для M_{i + 1} = {M_i[i]} по модулю {moduli[i]}:")
        inverse = mod_inverse_by_euler(M_i[i], moduli[i])
        print(f"N_{i + 1} = (M_{i + 1})^(-1) ≡ {inverse} (mod {moduli[i]})")
        N_i.append(inverse)
    print()

    x = 0
    print("Вычисление решения:")
    print("x = ", end="")
    for i in range(n):
        term = remainders[i] * M_i[i] * N_i[i]
        x += term
        if i < n - 1:
            print(f"{remainders[i]} * {M_i[i]} * {N_i[i]} + ", end="")
        else:
            print(f"{remainders[i]} * {M_i[i]} * {N_i[i]}")

    x = normalize_modulo(x, M)
    print(f"\nx = {x} (mod {M})")

    return x, M


def solve_system_ax_equals_b(a_list, b_list, m_list):
    if len(a_list) != len(b_list) or len(b_list) != len(m_list):
        raise ValueError("Все списки должны иметь одинаковую длину")

    m_list = normalize_moduli_list(m_list)
    b_list = normalize_values_by_moduli(b_list, m_list)

    n = len(a_list)
    print("=" * 60)
    print("Шаг 1: Приведение каждого сравнения к виду x ≡ cᵢ (mod m'ᵢ)")
    print("=" * 60 + "\n")

    reduced_remainders = []
    reduced_moduli = []

    for i in range(n):
        result = solve_single_congruence(a_list[i], b_list[i], m_list[i])
        if result is None:
            print(f"Сравнение {i + 1} не имеет решений. Система несовместна.")
            return None, None

        c, m, gcd = result
        reduced_remainders.append(c)
        reduced_moduli.append(m)

    print("=" * 60)
    print("Шаг 2: Решение приведенной системы методом китайской теоремы об остатках")
    print("=" * 60 + "\n")
    print("Приведенная система:")
    for i in range(n):
        print(f"x ≡ {reduced_remainders[i]} (mod {reduced_moduli[i]})")
    print()

    result = solve_system_of_congruences(reduced_remainders, reduced_moduli)
    if result[0] is None:
        return None, None
    x, M = result
    return x, M


def main():
    Flag = 1
    while Flag:
        try:
            print("=" * 60)
            print("Решение системы сравнений первой степени")
            print("=" * 60)
            n = int(input("\nВведите количество сравнений в системе: "))
            a_list, b_list, m_list = [], [], []
            print("\nВведите систему сравнений:")
            print("aᵢx ≡ bᵢ (mod mᵢ)")
            for i in range(n):
                a, b, m = int(input(f"\na_{i + 1} = ")), int(input(f"b_{i + 1} = ")), int(input(f"m_{i + 1} = "))
                a_list.append(a), b_list.append(b), m_list.append(m)
                print(f"{a}x ≡ {b} (mod {m})")

            print("\n" + "=" * 60)
            print("Решение:")
            print("=" * 60 + "\n")

            x, M = solve_system_ax_equals_b(a_list, b_list, m_list)

            if x is not None:
                print("\n" + "=" * 60)
                print("РЕЗУЛЬТАТ:")
                print("=" * 60)
                print(f"Система имеет решение: x ≡ {x} (mod {M})")

                print("\n" + "=" * 60)
                print("Проверка решения:")
                print("=" * 60)
                print(f"\nx = {x}:")
                all_correct = True
                for i in range(len(a_list)):
                    m = m_list[i]
                    left = normalize_modulo(a_list[i] * x, m)
                    expected = normalize_modulo(b_list[i], m)
                    is_correct = left == expected
                    status = "✓" if is_correct else "✗"
                    if not is_correct:
                        all_correct = False
                    print(f"  {status} {a_list[i]} * {x} mod {m} = {left}, должно быть {expected}")
                if all_correct:
                    print(f"  Решение x = {x} корректно")
            else:
                print("\nСистема не имеет решений.")

            print()
            Flag = int(input("Если хотите прервать программу, введите 0: "))
            print()
        except ValueError as e:
            print(f"\nОшибка: {e}")
            print("Введите корректные целые числа\n")
        except Exception as e:
            print(f"\nОшибка: {e}\n")


if __name__ == "__main__":
    main()
