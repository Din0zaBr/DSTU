from math import gcd
from sympy import primefactors


def linear_congruential_generator(a, b, m, x0, n=200):
    sequence = []
    x = x0
    for _ in range(n):
        x = (a * x + b) % m
        sequence.append(x)
    return sequence


def calculate_full_period(a, b, m, x0):
    seen = {}
    x = x0
    index = 0
    while x not in seen:
        seen[x] = index
        x = (a * x + b) % m
        index += 1
    return index - seen[x]


def check_maximal_period_conditions(a, b, m):
    coprime = gcd(b, m) == 1
    prime_factors = primefactors(m)
    divisible_by_primes = all((a - 1) % p == 0 for p in prime_factors)
    divisible_by_4 = True if m % 4 != 0 else (a - 1) % 4 == 0
    return coprime and divisible_by_primes and divisible_by_4


print("Введите параметры линейного конгруэнтного генератора или нажмите Enter для использования базовых значений.")
a = input("Введите a (множитель, по умолчанию 106): ")
b = input("Введите b (сдвиг, по умолчанию 1283): ")
m = input("Введите m (модуль, по умолчанию 6075): ")
x0 = input("Введите x0 (начальное значение, по умолчанию 1): ")
n = input("Введите количество чисел для генерации (по умолчанию 200): ")
a = int(a) if a else 106
b = int(b) if b else 1283
m = int(m) if m else 6075
x0 = int(x0) if x0 else 1
n = int(n) if n else 200
sequence = linear_congruential_generator(a, b, m, x0, n)
full_period = calculate_full_period(a, b, m, x0)
maximal_period = check_maximal_period_conditions(a, b, m)
print("\nСгенерированная последовательность:")
print(sequence)
print(f"\nПолный период последовательности: {full_period}")
if maximal_period:
    print("Выбранные параметры удовлетворяют условиям для максимального периода.")
else:
    print("Выбранные параметры НЕ удовлетворяют условиям для максимального периода.")
print("\nПромежуточные результаты:")
for i, num in enumerate(sequence):
    print(f"x[{i}] = {num}")
with open("lcg_sequence.txt", "w") as file:
    file.write("Сгенерированная последовательность:\n")
    file.writelines(f"x[{i}] = {num}\n" for i, num in enumerate(sequence))
print("\nПоследовательность сохранена в файл 'lcg_sequence.txt'.")
