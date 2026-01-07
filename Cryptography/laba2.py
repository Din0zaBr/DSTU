import math

def NOD(a, b, k=1):
    # Бинарный алгоритм Евклида
    if a == 0:
        return b * k
    if b == 0:
        return a * k
    if a == b:
        return a * k
    if a % 2 == 0 and b % 2 == 0:
        return NOD(a // 2, b // 2, k * 2)
    if a % 2 == 0 and b % 2 != 0:
        return NOD(a // 2, b, k)
    if a % 2 != 0 and b % 2 == 0:
        return NOD(a, b // 2, k)
    if a % 2 != 0 and b % 2 != 0:
        if a > b:
            return NOD(a - b, b, k)
        else:
            return NOD(a, b - a, k)

def is_prime(n):
    # Проверка простоты числа
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

def prime_factors(n):
    # Разложение числа на простые множители
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2
    if n > 1:
        factors.append(n)
    return factors

def Funct_Ailer(m):
    # Функция Эйлера
    if is_prime(m):
        return Funct_Ailera_prost_chisla(m)
    else:
        spisok = prime_factors(m)
        return Funct_Ailera_sost(spisok, m)

def Funct_Ailera_prost_chisla(n):
    return 1 if n == 1 else n - 1

def Funct_Ailera_sost(spisok, m):
    deliteli_ynik = sorted(set(spisok))
    fi = m
    for i in deliteli_ynik:
        fi *= (i - 1)
        fi //= i
    return fi

def ostatok(a, stepen, m):
    # Нахождение a^stepen mod m
    flag = True
    if a < 0:
        flag = (stepen % 2 == 0)
        a = abs(a)

    d = NOD(a, m)

    # --- Случай 1: НОД = 1 ---
    if d == 1:
        print(f"НОД({a}, {m}) = 1")
        if is_prime(m):
            print(f"Так как {m} — простое, используем малую теорему Ферма:")
            p = m - 1
            print(f"{a}^{p} ≡ 1 (mod {m})")
            ost = stepen % p
            meloch = stepen // p
        else:
            print(f"Так как {m} — составное, используем теорему Эйлера:")
            p = Funct_Ailer(m)
            print(f"{a}^{p} ≡ 1 (mod {m})")
            ost = stepen % p
            meloch = stepen // p

        print(f"{a}^{stepen} mod {m}")
        if stepen > p:
            print(f"({a}^{p})^{meloch} * {a}^{ost} mod {m}")
        print(f"{a}^{ost} mod {m}")
        print(f"{a ** ost} mod {m}")

        vivod = (a ** ost) % m
        if not flag:
            print("Домножаем на -1")
            vivod = (m - vivod) % m
        return vivod

    # --- Случай 2: НОД ≠ 1 ---
    else:
        print(f"НОД({a}, {m}) = {d} ≠ 1")
        new_a, new_m = a // d, m // d
        print(f"Разложим: {a} = {d} * {new_a}, {m} = {d} * {new_m}")

        pomexa = 1
        if new_a != a:
            pomexa = new_a
            stepen -= 1
            new_a = a
            print(f"Вычисляем: {pomexa} * ({new_a})^{stepen} mod {new_m}")

        part_result = (ostatok(new_a, stepen, new_m) * pomexa) % new_m
        print(f"Результат: {pomexa} * ({new_a})^{stepen} ≡ {part_result} mod {new_m}")
        stepen += 1
        final_result = (d * part_result) % m
        print(f"Итог: ({a})^{stepen} ≡ {final_result} mod {m}")

        if not flag:
            print("Домножаем на -1")
            final_result = (m - final_result) % m
        return final_result

# --- Новый main ---
def main():
    print("Лабораторная работа №2 ТЧМК")
    expr = input("Введите выражение (например: 7^20 или 5^50+13^100): ")
    m = int(input("Введите поле (mod m): "))

    print(f"\nВы ввели: {expr} mod {m}\n")

    # Разбиваем на слагаемые
    terms = expr.split("+")
    total = 0

    for term in terms:
        if "^" not in term:
            print(f"Ошибка: '{term}' не содержит ^")
            continue
        base, power = term.split("^")
        base, power = int(base.strip()), int(power.strip())
        print(f"\n--- Считаем {base}^{power} mod {m} ---")
        val = ostatok(base, power, m)
        print(f"Результат: {base}^{power} ≡ {val} (mod {m})\n")
        total = (total + val) % m

    print("=" * 50)
    print(f"Итоговый ответ: {expr} ≡ {total} (mod {m})")

if __name__ == "__main__":
    main()