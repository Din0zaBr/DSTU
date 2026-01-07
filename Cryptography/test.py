def legendre_symbol(a, p):
    """Вычисляет символ Лежандра (a/p)."""
    ls = pow(a, (p - 1) // 2, p)
    return 1 if ls == 1 else (-1 if ls == p - 1 else 0)


def solve_quadratic_congruence():
    print("=" * 60)
    print("x^2 = a (mod p)")
    print("=" * 60)
    print("Введите значения")

    try:
        a = int(input("a >> "))
        p = int(input("p >> "))
    except ValueError:
        print("Ошибка: введите целые числа")
        return

    # Проверка простоты
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    if not is_prime(p):
        print(f"Ошибка: {p} должно быть простым числом > 2")
        return

    print("\n" + "=" * 60)
    print("ШАГ 1: Проверяем разрешимость через символ Лежандра")
    print("=" * 60)

    ls = legendre_symbol(a, p)
    print(f"Вычислим символ Лежандра ({a}/{p}):")
    print(f"({a}/{p}) = {a}^(({p}-1)/2) mod {p} = {a}^{{(p-1)//2}} mod {p}")

    exponent = (p - 1) // 2
    result = pow(a, exponent, p)
    print(f"= {result} mod {p}")

    if result == p - 1:
        result_display = -1
    else:
        result_display = result

    print(f"({a}/{p}) = {result_display}")

    if ls != 1:
        print(f"\nТак как (a/p) = {result_display} => система неразрешима")
        return []

    print(f"\nТак как (a/p) = 1 => система разрешима и имеет ровно 2 решения")

    # Случай 1: p ≡ 3 (mod 4)
    if p % 4 == 3:
        print("\n" + "=" * 60)
        print("ШАГ 2: Используем специальный случай p ≡ 3 (mod 4)")
        print("=" * 60)

        print(f"\n{p} mod 4 = {p % 4} => {p} ≡ 3 (mod 4)")
        print("Используем формулу: x = ±a^((p+1)/4) mod p")

        print(f"\nНаходим число m, представив модуль как p = 4m + 3:")
        m = (p - 3) // 4
        print(f"{p} = 4 * {m} + 3")
        print(f"m = {m}")

        exponent = (p + 1) // 4
        print(f"\nВычисляем x = a^(m+1) mod p = {a}^({m}+1) mod {p} = {a}^{exponent} mod {p}")

        # Показываем вычисление по шагам
        print(f"\nВычисление {a}^{exponent} mod {p}:")
        solution = pow(a, exponent, p)
        print(f"= {solution} mod {p}")

        x1 = solution
        x2 = p - solution

        print(f"\nПолучаем два решения:")
        print(f"x1 = {solution} mod {p}")
        print(f"x2 = {p} - {solution} = {x2} mod {p}")

    # Случай 2: p ≡ 5 (mod 8)
    elif p % 8 == 5:
        print("\n" + "=" * 60)
        print("ШАГ 2: Используем специальный случай p ≡ 5 (mod 8)")
        print("=" * 60)

        print(f"\n{p} mod 8 = {p % 8} => {p} ≡ 5 (mod 8)")

        print(f"\nНаходим число m, представив модуль как p = 8m + 5:")
        m = (p - 5) // 8
        print(f"{p} = 8 * {m} + 5")
        print(f"m = {m}")

        # Проверяем a^(2m+1) mod p
        check_exp = 2 * m + 1
        print(f"\nШАГ 2.1: Проверяем a^(2m+1) mod p:")
        print(f"Вычисляем {a}^(2*{m}+1) mod {p} = {a}^{check_exp} mod {p}")
        check = pow(a, check_exp, p)
        print(f"= {check} mod {p}")

        if check == 1:
            print(f"\nПоскольку {a}^(2m+1) ≡ 1 mod {p}, используем формулу:")
            print("x = a^(m+1) mod p")

            exp1 = m + 1
            print(f"\nВычисляем x = {a}^({m}+1) mod {p} = {a}^{exp1} mod {p}")
            x1 = pow(a, exp1, p)
            print(f"= {x1} mod {p}")

        else:  # check == p-1
            print(f"\nПоскольку {a}^(2m+1) ≡ -1 mod {p}, используем формулу:")
            print("x = a^(m+1) * 2^(2m+1) mod p")

            exp1 = m + 1
            exp2 = 2 * m + 1
            print(f"\nВычисляем:")
            print(f"Часть 1: {a}^({m}+1) mod {p} = {a}^{exp1} mod {p}")
            part1 = pow(a, exp1, p)
            print(f"= {part1} mod {p}")

            print(f"Часть 2: 2^(2*{m}+1) mod {p} = 2^{exp2} mod {p}")
            part2 = pow(2, exp2, p)
            print(f"= {part2} mod {p}")

            print(f"\nОбъединяем: x = {part1} * {part2} mod {p}")
            x1 = (part1 * part2) % p
            print(f"= {x1} mod {p}")

        x2 = p - x1
        print(f"\nВторое решение: x2 = {p} - {x1} = {x2} mod {p}")

    # Случай 3: p ≡ 1 (mod 8) - алгоритм Тонелли-Шэнкса
    else:
        print("\n" + "=" * 60)
        print("ШАГ 2: Используем алгоритм Тонелли-Шэнкса (p ≡ 1 mod 8)")
        print("=" * 60)

        print(f"\n{p} mod 8 = {p % 8} => {p} ≡ 1 (mod 8)")
        print("Используем общий алгоритм Тонелли-Шэнкса")

        # Шаг 2.1: Разложение p-1 = Q * 2^S
        print(f"\nШАГ 2.1: Разложение {p}-1 = Q * 2^S")
        Q = p - 1
        S = 0
        steps = []
        temp = p - 1
        while Q % 2 == 0:
            steps.append(f"{temp} = {Q} * 2^{S}")
            Q //= 2
            S += 1
            temp = Q * (2 ** S)

        # Добавляем последний шаг
        steps.append(f"{p - 1} = {Q} * 2^{S}")

        for i, step in enumerate(steps):
            print(f"Шаг {i + 1}: {step}")

        print(f"\nИтог: {p}-1 = {Q} * 2^{S}")
        print(f"Q = {Q}, S = {S}")

        # Шаг 2.2: Поиск квадратичного невычета z
        print(f"\nШАГ 2.2: Находим квадратичный невычет z")
        print("(ищем z такое, что z^((p-1)/2) ≡ -1 mod p)")

        z = 2
        attempts = []
        while True:
            result = pow(z, (p - 1) // 2, p)
            attempts.append(f"z={z}: {z}^{(p - 1) // 2} mod {p} = {result} {'(невычет!)' if result == p - 1 else ''}")
            if result == p - 1:
                break
            z += 1

        for attempt in attempts:
            print(f"  Проверяем {attempt}")

        print(f"\nНайден квадратичный невычет: z = {z}")

        # Шаг 2.3: Инициализация
        print(f"\nШАГ 2.3: Инициализация переменных")
        print(f"c = z^Q mod p = {z}^{Q} mod {p}")
        c = pow(z, Q, p)
        print(f"c = {c}")

        print(f"\nt = a^Q mod p = {a}^{Q} mod {p}")
        t = pow(a, Q, p)
        print(f"t = {t}")

        print(f"\nR = a^((Q+1)/2) mod p = {a}^{((Q + 1) // 2)} mod {p}")
        R = pow(a, (Q + 1) // 2, p)
        print(f"R = {R}")

        M = S
        print(f"\nM = S = {M}")

        # Шаг 2.4: Основной цикл
        print(f"\nШАГ 2.4: Основной цикл алгоритма")
        iteration = 1

        if t == 1:
            print(f"t = 1 уже на старте! Алгоритм завершён.")
        else:
            print(f"Начальные значения: t = {t}, M = {M}")

        while t != 1:
            print(f"\n--- Итерация {iteration} ---")

            # Находим наименьшее i
            print(f"Ищем наименьшее i (0 < i < {M}), такое что t^(2^i) ≡ 1 mod {p}")
            i = 1
            while pow(t, 2 ** i, p) != 1:
                i += 1
            print(f"Нашли i = {i}")

            # Вычисляем b
            print(f"\nВычисляем b = c^(2^(M-i-1)) mod p")
            print(f"b = {c}^(2^({M}-{i}-1)) mod {p}")
            b = pow(c, 2 ** (M - i - 1), p)
            print(f"b = {b}")

            # Обновляем значения
            print(f"\nОбновляем переменные:")
            old_R = R
            R = (R * b) % p
            print(f"R = R * b mod p = {old_R} * {b} mod {p} = {R}")

            old_t = t
            t = (t * b * b) % p
            print(f"t = t * b² mod p = {old_t} * {b}² mod {p} = {t}")

            old_c = c
            c = (b * b) % p
            print(f"c = b² mod p = {b}² mod {p} = {c}")

            old_M = M
            M = i
            print(f"M = i = {M}")

            iteration += 1

        print(f"\nШАГ 2.5: Завершение алгоритма")
        print(f"t = 1, значит R = {R} - искомый корень")

        x1 = R
        x2 = p - R
        print(f"\nВторой корень: {p} - {R} = {x2}")

    print("\n" + "=" * 60)
    print("ОТВЕТ")
    print("=" * 60)
    print(f"x ≡ {x1} (mod {p})")
    print(f"x ≡ {x2} (mod {p})")

    print("\n" + "=" * 60)
    print("ПРОВЕРКА")
    print("=" * 60)
    check1 = pow(x1, 2, p)
    check2 = pow(x2, 2, p)
    print(f"{x1}² mod {p} = {check1}")
    print(f"{x2}² mod {p} = {check2}")

    if check1 == a % p and check2 == a % p:
        print("✓ Проверка пройдена успешно!")
    else:
        print("✗ Ошибка в вычислениях!")

    return [x1, x2]


# Тестовые примеры
if __name__ == "__main__":
    # Пример 1: p ≡ 3 (mod 4)
    print("\n" + "=" * 60)
    print("ПРИМЕР 1: x² ≡ 13 (mod 23)")
    print("=" * 60)
    # Ввод: 13, 23

    # Пример 2: p ≡ 5 (mod 8)
    print("\n" + "=" * 60)
    print("ПРИМЕР 2: x² ≡ 34 (mod 37)")
    print("=" * 60)
    # Ввод: 34, 37

    # Пример 3: p ≡ 1 (mod 8)
    print("\n" + "=" * 60)
    print("ПРИМЕР 3: x² ≡ 8 (mod 73)")
    print("=" * 60)
    # Ввод: 8, 73

    # Запуск интерактивного режима
    solve_quadratic_congruence()