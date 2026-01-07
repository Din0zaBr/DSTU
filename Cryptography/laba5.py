from sympy import isprime
from laba1_bin import binary_gcd_chain
from laba3 import prime_factors


def legendre_symbol(a, p):
    """Вычисление символа Лежандра (a/p)"""
    if a % p == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def jacobi_symbol(a, n):
    """Вычисление символа Якоби через разложение на простые множители"""
    factors = prime_factors(n)
    print(f"Простые множители {n}: {factors}")
    result = 1
    for p in factors:
        s = legendre_symbol(a, p)
        print(f"Символ Лежандра ({a}/{p}) = {s}")
        result *= s
    return result


def quadratic_residue(a,p):
    g, steps = binary_gcd_chain(a, p)
    print(f"НОД({a},{p}) = {g}")

    if g != 1:
        print("Числа не взаимно просты, символ не определён.")
        return

    if isprime(p):
        print(f"Так как число {p} простое, то определяем символ Лежандра, используя критерий Эйлера для вычисления ({a}/{p})")
        symbol = legendre_symbol(a, p)
    else:
        print(f"Так как число {p} составное, то определяем символ Якоби, раскладывая на символы Лежандра для вычисления ({a}/{p})")
        symbol = jacobi_symbol(a, p)

    if symbol == 1:
        print(f"Так как ({a}/{p}) = 1, следовательно квадратичное сравнение разрешимо и имеет два решения")
    elif symbol == -1:
        print(f"Так как ({a}/{p}) = -1, следовательно квадратичное сравнение неразрешимо")
        exit()
    else:
        print(f"{a} делится на {p}, символ = 0")
        exit()
    print()

