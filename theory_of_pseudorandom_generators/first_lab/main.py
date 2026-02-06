from math import gcd
from sympy import primefactors


def generate_sequence(m, a, b, x0, n):
    seq = []
    x = x0
    for _ in range(n):
        x = (a * x + b) % m
        seq.append(x)
    return seq


def find_full_period(m, a, b, x0):
    """
    seen - словарь «значение: номер шага, т.е. при каком i мы впервые увидели данное x.
    """
    seen = {}
    x = x0
    i = 0
    while True:
        if x in seen:
            return i - seen[x]
        seen[x] = i
        x = (a * x + b) % m
        i += 1


def check_max_period_conditions(m, a, b):
    primes = primefactors(m)
    return {
        "НОД(b, m) = 1": gcd(b, m) == 1,
        "a - 1 кратно всем простым делителям m": all((a - 1) % p == 0 for p in primes),
        "Если m кратно 4, то a - 1 кратно 4": (m % 4 != 0) or ((a - 1) % 4 == 0),
    }


def read_int(prompt, lo=None, hi=None, error="Некорректное значение"):
    while True:
        try:
            val = int(input(prompt))
            if lo is not None and val < lo:
                print(f"{error} (мин. {lo})")
                continue
            if hi is not None and val > hi:
                print(f"{error} (макс. {hi})")
                continue
            return val
        except ValueError:
            print("Введите целое число.")


def main():
    print("Введите параметры для генерации последовательности:")
    m = read_int("Модуль (m > 0): ", lo=1, error="m должно быть положительным")
    a = read_int(f"Множитель (0 <= a < {m}): ", lo=0, hi=m - 1, error="a вне диапазона")
    b = read_int(f"Приращение (0 <= b < {m}): ", lo=0, hi=m - 1, error="b вне диапазона")
    x0 = read_int(f"Начальное значение (0 <= x0 < {m}): ", lo=0, hi=m - 1, error="x0 вне диапазона")
    n = read_int("Количество чисел (> 0): ", lo=1, error="Количество должно быть положительным")

    sequence = generate_sequence(m, a, b, x0, n)
    period = find_full_period(m, a, b, x0)
    conditions = check_max_period_conditions(m, a, b)

    print("\nРезультаты:")
    print(f"Сгенерированная последовательность (первые {n} чисел):\n{sequence}")
    print(f"Полный период: {period}")
    print("\nПроверка условий для максимального периода:")
    for name, ok in conditions.items():
        print(f"  {name}: {'Да' if ok else 'Нет'}")

    with open("generated_sequence.txt", "w") as f:
        f.write("\n".join(map(str, sequence)))
    print("\nПоследовательность сохранена в 'generated_sequence.txt'.")


if __name__ == "__main__":
    main()
