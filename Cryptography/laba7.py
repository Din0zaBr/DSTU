from laba1_bin import binary_gcd_chain
import math
from laba3 import Mod_Reduction


def main():
    """Главная функция"""
    a = int(input("Введите число a: "))
    b = int(input("Введите число b: "))
    m = int(input("Введите число m: "))
    print(f"Вы ввели {a}x ≡ {b} mod {m}")
    print(f"Перепишем сравнение в виде диофантова уравнения: {a}x - {m}y = {b}")
    g, steps = binary_gcd_chain(a, m)

    if g == 1 and b % g == 0:
        print(f"Так как НОД({a},{m}) = {g} и {b}/ {g}, следовательно решение существует.")
        coeffs = razloshenie(a, m)
        print(f"Коэффициенты: {coeffs}")
        print(f"Вычислим все подходящие дроби")
        table_data = table(coeffs)
        last_k = table_data['last_k']
        p_values = table_data['p_values']
        q_values = table_data['q_values']
        p_km1 = p_values[last_k]  # P_{k-1}
        q_km1 = q_values[last_k]  # Q_{k-1}
        print(
            f"Так как k = {last_k}, следовательно P_k-1 = P_{last_k - 1} = {p_km1} и Q_k-1 = Q_{last_k - 1} = {q_km1}")
        print(f"НОД({a},{m}) = {g}")
        if g == 1:
            print(f"Вычислим значение x по формуле:")
            print(f"x = (-1)^k-1 * b/НОД(a, m) * Q_k-1 (mod m)")
            print(f"x = (-1)^{last_k - 1} * {b}/{g} * {q_km1} (mod {m})")
            ras = pow(-1, last_k - 1)
            ras1 = b / g
            result = ras * ras1 * q_km1
            print(f"x = {int(result)} (mod {m})")
            result = Mod_Reduction(result, m)
            print(f"x = {int(result)} (mod {m})")
            print("*" * 50)
            raschet = result * a
            raschet1 = Mod_Reduction(raschet, m)
            print(f"Проверка: {int(result)} * {a} = {int(raschet1)} ≡ {b} (mod {m})")

    elif g != 1 and b % g == 0:
        print(f"Так как НОД({a},{m}) = {g} и {b} делится на {g}, следовательно решение существует.")
        print(f"Упрощаем уравнение, деля все коэффициенты на НОД:")
        a1 = int(a / g)
        b1 = int(b / g)
        m1 = int(m / g)
        print(f"После деления на {g}: {a1}x ≡ {b1} mod {m1}")
        print()
        print(f"Решаем новое уравнение: {a1}x ≡ {b1} mod {m1}")
        coeffs = razloshenie(a1, m1)
        print(f"Коэффициенты: {coeffs}")
        print(f"Вычислим все подходящие дроби")
        table_data = table(coeffs)
        last_k = table_data['last_k']
        p_values = table_data['p_values']
        q_values = table_data['q_values']
        p_km1 = p_values[last_k]
        q_km1 = q_values[last_k]
        print(
            f"Так как k = {last_k}, следовательно P_k-1 = P_{last_k - 1} = {p_km1} и Q_k-1 = Q_{last_k - 1} = {q_km1}")

        print(f"Вычислим значение x по формуле:")
        print(f"x = (-1)^k-1 * b/НОД(a, m) * Q_k-1 (mod m)")
        print(f"x = (-1)^{last_k - 1} * {b}/{g} * {q_km1} (mod {m})")
        ras = pow(-1, last_k - 1)
        ras1 = b / g
        result_new = ras * ras1 * q_km1
        result_new = Mod_Reduction(result_new, m)
        print(f"x ≡ {int(result_new)} mod {m}")
        print()

        print(f"Теперь возвращаемся к исходному уравнению {a}x ≡ {b} mod {m}:")
        print(f"Множество решений этого сравнения состоит из {g} классов вычетов по модулю {m}.")
        print(f"Если x₀ = {int(result_new)} - одно из решений, но все другие решения:")
        print(f"x₀ + m₁,x₀ + 2m₁,... где m₁ = m/d = {m}/{g} = {m1}")
        print()

        print(f"Все {g} решений по модулю {m}:")
        solutions = []
        for t in range(g):
            solution = result_new + t * m1
            solution = Mod_Reduction(solution, m)
            solutions.append(int(solution))
            print(f"x ≡ {int(solution)} (mod {m})")

        print()
        print("*" * 50)
        print("Проверка решений:")
        for solution in solutions:
            check = Mod_Reduction(solution * a, m)
            print(f"{solution} * {a} ≡ {int(check)} mod {m} - ", end="")
            if int(check) == b:
                print("✓ верно")
            else:
                print("✗ неверно")

    else:
        print(f"Решения не существует, так как b = {b} не делится на НОД({a},{m}) = {g}")


def razloshenie(a, m):
    """Разложение в формате, возвращающее коэффициенты"""
    coefficients = []
    q = a // m
    coefficients.append(q)
    a = a % m
    while a != 0:
        a, m = m, a
        q = a // m
        coefficients.append(q)
        a = a % m
    return coefficients


def table(a_coeffs):
    """
    Построение таблицы в виде горизонтальных строк: k, a_k, p_k, q_k
    """
    n = len(a_coeffs)

    k_values = [-1, 0] + list(range(1, n))
    a_values = ['-']
    p_values = [1]
    q_values = [0]

    P_prev2, P_prev1 = 1, a_coeffs[0]
    Q_prev2, Q_prev1 = 0, 1

    a_values.append(a_coeffs[0])
    p_values.append(P_prev1)
    q_values.append(Q_prev1)

    for k in range(1, n):
        a_k = a_coeffs[k]
        P_k = a_k * P_prev1 + P_prev2
        Q_k = a_k * Q_prev1 + Q_prev2

        a_values.append(a_k)
        p_values.append(P_k)
        q_values.append(Q_k)

        P_prev2, P_prev1 = P_prev1, P_k
        Q_prev2, Q_prev1 = Q_prev1, Q_k
        last_k = k

    print("k      ", end='')
    for val in k_values:
        print(f"{val:>6}", end=' ')
    print()

    print("a_k    ", end='')
    for val in a_values:
        print(f"{val:>6}", end=' ')
    print()

    print("p_k    ", end='')
    for val in p_values:
        print(f"{val:>6}", end=' ')
    print()

    print("q_k    ", end='')
    for val in q_values:
        print(f"{val:>6}", end=' ')
    print()
    return {
        'last_k': last_k,
        'p_values': p_values,
        'q_values': q_values,
        'a_values': a_values,
        'k_values': k_values
    }

if __name__ == "__main__":
    main()