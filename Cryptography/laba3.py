import math

def is_prime(n): # Проверка простоты числа (Решето Эратосфена)
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False

    return True

def prime_factors(n): # Простые делители числа (Почти решето Эратосфена)
    factors = []

    while n % 2 == 0:
        factors.append(2)
        n = n // 2

    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n = n // i
        i += 2

    if n > 1:
        factors.append(n)

    return factors

def Euler_Function(m): # Функция Эйлера
    unique_prime_divisors = prime_factors(m)

    if is_prime(m) == True:
        phi = Euler_For_Prime(m)
        return phi
    else:
        phi = Euler_For_Composite(unique_prime_divisors, m)
        return phi

def Euler_For_Prime(n):
    if n == 1:
        return 1
    else:
        phi = n - 1
        return phi

def Euler_For_Composite(divisors_list, m):
    unique_divisors = sorted(set(divisors_list))
    phi = m

    for divisor in unique_divisors:
        phi *= divisor-1
        phi //= divisor

    return phi

def Mod_Reduction(n, m):
    n %= m
    return n

def Simplify_Expression(a, power, b, m):
    a = Mod_Reduction(a, m)
    b = Mod_Reduction(b, m)

    remainder = 1

    if power % 2 == 0:
        while power % 2 == 0 and power != 0:
            remainder *= 2
            power //= 2

        print(f'Вычисляем: ({a}^{remainder})^{power} * {b} (mod {m})')

        a = Mod_Reduction(a**remainder, m)

        print(f'Упрощаем: {a}^{power} * {b} (mod {m})')

        a = Mod_Reduction(a**power, m)

        print(f'Возводим в степень: {a} * {b} (mod {m})')

        result = Mod_Reduction(a*b, m)

        print(f'Получаем: {result} (mod {m})')

        return result

    else:
        multiplier = a
        power -= 1
        print(f'Раскладываем: {multiplier} * {a}^{power} * {b} (mod {m})')

        remainder = 1
        while power % 2 == 0 and power != 0:
            remainder *= 2
            power //= 2

        print(f'Группируем: {multiplier} * ({a}^{remainder})^{power} * {b} (mod {m})')

        new_b = Mod_Reduction(multiplier * b, m)
        a = Mod_Reduction(a**remainder, m)

        print(f'Умножаем: {a}^{power} * {new_b} (mod {m})')

        a = Mod_Reduction(a ** power, m)

        print(f'Вычисляем степень: {a} * {new_b} (mod {m})')

        result = Mod_Reduction(a * new_b, m)

        print(f'Результат: {result} (mod {m})')

        return result


def Solve_Comparison(a, b, m):
    d = math.gcd(a, m)

    if b % d != 0:
        return 'Уравнение не имеет решений'

    if d > 1:
        new_a = a // d
        new_b = b // d
        new_m = m // d

        print(f"Сокращаем на НОД={d}")
        print(f"Получаем: {new_a} * x ≡ {new_b} (mod {new_m})")

        x0 = Solve_Comparison(new_a, new_b, new_m)

        if isinstance(x0, str):
            return x0

        solutions = []
        for base_solution in x0:
            for k in range(d):
                xi = (base_solution + k * new_m) % m
                print(f'Решение x{k} = {xi}')
                solutions.append(xi)

        print(f"Находим все решения для модуля {m}:")
        print(f"Базовое решение: {x0[0]} (mod {new_m})")
        print(f"Полный набор решений: {solutions} (mod {m})")

        return solutions

    else:
        print(f'Уравнение имеет единственное решение')
        print('Применяем теорему Эйлера:')
        print('Формула решения: x = a^(φ(m)-1) * b (mod m)')

        phi = Euler_Function(m)
        print(f'φ({m}) = {phi}')
        print(f'x = {a}^({phi}-1) * {b} (mod {m})')

        exponent = phi - 1
        print(f'x = {a}^{exponent} * {b} (mod {m})')

        x0 = Simplify_Expression(a, exponent, b, m)

        print(f"Найденное решение: x ≡ {x0} (mod {m})")
        return [x0]

def main():
    print('Лабораторная работа №3')
    print('Решение линейных сравнений')
    a_val = int(input('Введите коэффициент a: '))
    b_val = int(input('Введите коэффициент b: '))
    modulus = int(input('Введите модуль m: '))

    print(f'Решаем уравнение: {a_val} * x ≡ {b_val} (mod {modulus})')

    if b_val < 0:
        b_val += modulus

    answer = Solve_Comparison(a_val, b_val, modulus)


    print('Проверка решений:')

    if isinstance(answer, str):
        print(answer)
        return

    for solution in answer:
        if (a_val * solution) % modulus == b_val:
            print(f'✓ {a_val} * {solution} ≡ {b_val} (mod {modulus}) - верно')
        else:
            print('✗ Ошибка в проверке!')

if __name__ == '__main__':
    main()