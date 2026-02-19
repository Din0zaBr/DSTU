"""
Квадратичный конгруэнтный генератор псевдослучайных чисел.
Рекуррентная формула: x_next = (a2 * x^2 + a1 * x + b) mod m
"""
from math import gcd
from sympy import primefactors


def next_value(m, a1, a2, b, x):
    """Один шаг генератора: следующее значение по текущему x."""
    return (a2 * x * x + a1 * x + b) % m


def quadratic_congruential_generator(m, a1, a2, b, x0, num_terms):
    """Генерирует последовательность из num_terms чисел."""
    sequence = []
    x = x0
    for _ in range(num_terms):
        x = next_value(m, a1, a2, b, x)
        sequence.append(x)
    return sequence


def find_full_period(m, a1, a2, b, x0):
    """Находит длину полного периода последовательности."""
    seen = {}
    x = x0
    index = 0
    while True:
        if x in seen:
            return index - seen[x]
        seen[x] = index
        x = next_value(m, a1, a2, b, x)
        index += 1


def is_power_of_two(n):
    """Проверяет, является ли n степенью двойки (n >= 2)."""
    return n >= 2 and (n & (n - 1)) == 0


def check_max_period_conditions(m, a1, a2, b):
    """
    Проверяет условия максимального периода для квадратичного генератора.
    Возвращает словарь: название условия -> выполнено (True/False).
    """
    condition1 = gcd(b, m) == 1

    primes = [p for p in primefactors(m) if p != 2]
    condition2 = all((a1 - 1) % p == 0 and a2 % p == 0 for p in primes)

    condition3 = True
    if m % 4 == 0:
        condition3 = a2 % 2 == 0 and (a2 % 4) == ((a1 - 1) % 4)
    elif m % 2 == 0:
        condition3 = a2 % 2 == 0 and (a1 - 1) % 2 == 0

    condition4 = True
    if is_power_of_two(m):
        condition4 = (
                b % 2 != 0
                and a2 % 2 == 0
                and a1 % 2 != 0
                and (a1 % 4) == ((a2 + 1) % 4)
        )
    elif m % 9 == 0:
        condition4 = (a2 % 9) != (3 * b) % 9

    return {
        "НОД(b, m) = 1": condition1,
        "a1 - 1, a2 кратны всем нечётным простым делителям m": condition2,
        "a2 чётное и a2 ≡ (a1 - 1) (mod 4 или mod 2)": condition3,
        "Для степени двойки: a1, b нечётные, a2 чётное, a1 ≡ (a2+1) (mod 4)": condition4,
    }


def read_int(prompt, default=None, min_val=None, max_val=None):
    """Ввод целого числа с опциональным значением по умолчанию и проверками."""
    if default is not None:
        prompt = f"{prompt} (Enter = {default}): "
    s = input(prompt).strip()
    if default is not None and s == "":
        return default
    value = int(s)
    if min_val is not None and value < min_val:
        raise ValueError(f"Значение должно быть не меньше {min_val}.")
    if max_val is not None and value > max_val:
        raise ValueError(f"Значение должно быть не больше {max_val}.")
    return value


def main():
    # Логика как в test.py: квадратичный генератор + проверка периода и условий
    print("Квадратичный конгруэнтный генератор")
    print("Формула: x_next = (a2·x² + a1·x + b) mod m")
    print("Введите параметры или нажмите Enter для значения по умолчанию.\n")

    m = read_int("Модуль m", default=256, min_val=1)
    a1 = read_int("Коэффициент a1", default=1, min_val=0, max_val=m)
    a2 = read_int("Коэффициент a2", default=2, min_val=0, max_val=m)
    b = read_int("Приращение b", default=1, min_val=0, max_val=m)
    x0 = read_int("Начальное значение x0", default=1, min_val=0, max_val=m)
    num_terms = read_int("Количество чисел", default=20, min_val=1)

    sequence = quadratic_congruential_generator(m, a1, a2, b, x0, num_terms)
    full_period = find_full_period(m, a1, a2, b, x0)
    conditions = check_max_period_conditions(m, a1, a2, b)

    print("\nСгенерированная последовательность:")
    print(sequence)
    print(f"\nПолный период последовательности: {full_period}")

    # Промежуточные результаты по элементам (как в wtf.py), если чисел немного
    if num_terms <= 50:
        print("\nПромежуточные результаты:")
        for i, num in enumerate(sequence):
            print(f"  x[{i}] = {num}")

    print("\nПроверка условий для максимального периода:")
    for name, ok in conditions.items():
        print(f"  {name}: {'Да' if ok else 'Нет'}")

    all_ok = all(conditions.values())
    if all_ok:
        print("\nВыбранные параметры удовлетворяют условиям для максимального периода.")
    else:
        print("\nВыбранные параметры НЕ удовлетворяют условиям для максимального периода.")

    # Сохранение в файл (логика из wtf.py)
    save = input("\nСохранить последовательность в файл? (y/n, Enter = n): ").strip().lower()
    if save in ("y", "да"):
        filename = "quadratic_sequence.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("Сгенерированная последовательность (квадратичный генератор):\n")
            for i, num in enumerate(sequence):
                f.write(f"x[{i}] = {num}\n")
        print(f"Последовательность сохранена в файл '{filename}'.")


if __name__ == "__main__":
    main()
