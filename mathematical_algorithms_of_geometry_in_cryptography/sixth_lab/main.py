from math import ceil, sqrt


def mod_inv(n, p):
    return pow(n, p - 2, p)


def find_points(a, b, p):
    points = []
    for x in range(p):
        x_cubed = (x ** 3) % p
        ax = (a * x) % p
        rhs = (x_cubed + ax + b) % p
        y_values = []
        for y in range(p):
            lhs = (y ** 2) % p
            if lhs == rhs:
                y_values.append(y)
                points.append((x, y))
    return points


def is_on_curve(P, a, b, p):
    if P is None:
        return True
    x, y = P
    return (y ** 2 % p) == ((x ** 3 + a * x + b) % p)


def add_points(P, Q, a, p):
    if P is None:
        return Q
    if Q is None:
        return P
    if P == Q:
        return double_point(P, a, p)
    if P[0] == Q[0]:
        return None
    lam = ((Q[1] - P[1]) * mod_inv(Q[0] - P[0], p)) % p
    x_r = (lam ** 2 - P[0] - Q[0]) % p
    y_r = (lam * (P[0] - x_r) - P[1]) % p
    return (x_r, y_r)


def double_point(P, a, p):
    if P is None or P[1] == 0:
        return None
    lam = ((3 * P[0] ** 2 + a) * mod_inv(2 * P[1], p)) % p
    x_r = (lam ** 2 - 2 * P[0]) % p
    y_r = (lam * (P[0] - x_r) - P[1]) % p
    return (x_r, y_r)


def scalar_multiply(k, P, a, p):
    if k == 0:
        return None
    res = None
    curr = P
    while k > 0:
        if k % 2 == 1:
            res = add_points(res, curr, a, p)
        curr = double_point(curr, a, p)
        k = k // 2
    return res


def baby_step_giant_step(P, a, p, N=None):
    if P is None:
        return 1
    if N is None:
        N = p + 1 + 2 * sqrt(p)
    m = ceil(sqrt(N))
    print(f"\n1. Вычисляем m = ceil(sqrt({N})) = {m}")
    print("\n2. Cтроим таблицу {tP: t} для t = 1..m")
    table = {}
    current = None
    for t in range(1, m + 1):
        current = add_points(current, P, a, p)
        table[current] = t
    print("Таблица:")
    for point, t in table.items():
        print(f"{t}: {point}")
    print(f"\n3. Вычисляем Q = mP = {m}*{P}")
    Q = scalar_multiply(m, P, a, p)
    print(f"Q = {Q if Q != None else 'O'}")
    if Q is None:
        print(f"Нашли: {m}P = O")
        for n in sorted(get_divisors(m)):
            if scalar_multiply(n, P, a, p) is None:
                print(f"n = {n}")
                return n
    minus_Q = (Q[0], (-Q[1]) % p) if Q else None
    print(f"-Q = {minus_Q}")
    print("\n4. Ищем совпадение R = j*(-Q) в таблице")
    R = None
    for j in range(m + 1):
        print(f"\nИтерация j = {j}:")
        print(f"\tR = {R}")
        if R in table:
            i = table[R]
            n = j * m + i
            print(f"\tНашли R в таблице (i = {i}) → n = {j}*{m} + {i} = {n}")
            print(f"\tПроверяем {n}P = {scalar_multiply(n, P, a, p)}")
            if scalar_multiply(n, P, a, p) is None:
                print(f"Успех! {n}P = O → порядок точки = {n}")
                return n
            else:
                print("Не равно O, продолжаем поиск")
        else:
            print("\tR нет в таблице")
        print(f"\tОбновляем R = R + (-Q) = {R} + {minus_Q}")
        R = add_points(R, minus_Q, a, p)
    return None


def get_divisors(n):
    divisors = set()
    for i in range(1, int(sqrt(n)) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)
    return divisors


a, b, p = map(int, input("Введите a, b, p через пробел: ").split())
print(f"y² ≡ x³ + {a}x + {b} (mod {p})")
points = find_points(a, b, p)
print("Все точки:", points, 'и О')
while True:
    P_input = input("\nВведите координаты P (x y): ")
    if P_input.lower() == 'exit':
        exit()
    try:
        Px, Py = map(int, P_input.split())
        P = (Px, Py)
        if is_on_curve(P, a, b, p):
            break
        print("Точка P не принадлежит кривой")
    except:
        print("Некорректный ввод")
order = baby_step_giant_step(P, a, p)
print(f"Порядок точки {P}: {order}")
