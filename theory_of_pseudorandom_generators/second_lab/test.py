from math import gcd
from sympy import primefactors


def quadratic_congruential_generator(m, a1, a2, b, x0, num_terms):
    sequence = []
    x = x0
    for _ in range(num_terms):
        x = (a2 * x ** 2 + a1 * x + b) % m
        sequence.append(x)
    return sequence


def find_full_period(m, a1, a2, b, x0):
    seen = {}
    x = x0
    index = 0
    while True:
        if x in seen:
            return index - seen[x]
        seen[x] = index
        x = (a2 * x ** 2 + a1 * x + b) % m
        index += 1


def needed_stepen_of_two(n):
    return (n != {0, 1}) and (n & (n - 1)) == 0


def check_max_period_conditions(m, a1, a2, b, full_period):
    condition1 = gcd(b, m) == 1
    primes = [p for p in primefactors(m) if p != 2]
    condition2 = all((a1 - 1) % p == 0 and a2 % p == 0 for p in primes)
    condition3 = True
    if m % 4 == 0:
        condition3 = a2 % 2 == 0 and a2 % 4 == (a1 - 1) % 4
    elif m % 2 == 0:
        condition3 = a2 % 2 == 0 and a2 % 2 == (a1 - 1) % 2
    condition4 = True
    if needed_stepen_of_two(m):
        condition4 = (b % 2 != 0) and (a2 % 2 == 0) and (a1 % 2 != 0) and (a1 % 4 == (a2 + 1) % 4)
    elif m % 9 == 0:
        condition4 = a2 % 9 != (3 * b) % 9

    return {
        "НОД(b, m) = 1": condition1,
        "a1 - 1, a2 кратны всем нечетным простым делителям m": condition2,
        "a2 четное и a2 сравнимо с a1 - 1 (mod 4/2)": condition3,
        "Если модуль равен степени двойки, то a1 сравнимо с (a2 + 1) (mod 4) и а1,b - нечётные, а2 - четное": condition4,
    }


def main():
    print("Введите параметры для генерации последовательности:")
    m = int(input("Модуль (m > 0): "))
    if m <= 0:
        raise ValueError("m должно быть положительным числом.")
    a1 = int(input(f"Коэффициент a1 (0 <= a1 < {m}): "))
    if not (0 <= a1 <= m):
        raise ValueError(f"a1 должно быть в диапазоне от 0 до {m}.")
    a2 = int(input(f"Коэффициент a2 (0 <= a2 < {m}): "))
    if not (0 <= a2 <= m):
        raise ValueError(f"a2 должно быть в диапазоне от 0 до {m}.")
    b = int(input(f"Приращение (0 <= b < {m}): "))
    if not (0 <= b <= m):
        raise ValueError(f"b должно быть в диапазоне от 0 до {m}.")
    x0 = int(input(f"Начальное значение (0 <= x0 < {m}): "))
    if not (0 <= x0 <= m):
        raise ValueError(f"x0 должно быть в диапазоне от 0 до {m}.")
    num_terms = int(input("Количество чисел для генерации (> 0): "))
    if num_terms <= 0:
        raise ValueError("Количество чисел должно быть положительным.")
    sequence = quadratic_congruential_generator(m, a1, a2, b, x0, num_terms)
    full_period = find_full_period(m, a1, a2, b, x0)
    conditions = check_max_period_conditions(m, a1, a2, b, full_period)
    print("\nСгенерированная последовательность:")
    print(sequence)
    print(f"Полный период последовательности: {full_period}")
    print("\nПроверка условий для максимального периода:")
    for condition, result in conditions.items():
        print(f"{condition}: {'Да' if result else 'Нет'}")


if __name__ == "__main__":
    main()
