def inverse_mod(k, p):
    if k == 0:
        raise ZeroDivisionError("division by zero")
    return pow(k, -1, p)


def legendre_symbol(a, p):
    return pow(a, (p - 1) // 2, p)


def sqrt_mod(n, p):
    """Квадратный корень из n mod p (Тонелли–Шэнкс). None если вычета нет."""
    if n == 0:
        return 0
    if p == 2:
        return n
    if legendre_symbol(n, p) != 1:
        return None
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)

    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    for z in range(2, p):
        if legendre_symbol(z, p) == p - 1:
            break
    c = pow(z, q, p)
    x = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    while t != 1:
        i = 1
        temp = pow(t, 2, p)
        while temp != 1:
            temp = pow(temp, 2, p)
            i += 1
            if i == m:
                return None
        b = pow(c, 2 ** (m - i - 1), p)
        x = (x * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        m = i
    return x


def find_curve_points(a, b, p, show_table=True):
    """Точки кривой y² ≡ x³ + ax + b (mod p). O в конце."""
    points = []
    if show_table:
        print("----------------------------------------------")
        print("|   x   | x³ + ax + b ||   y   |   y² mod p  |")
        print("----------------------------------------------")

    for x in range(p):
        x_res = (x ** 3 + a * x + b) % p
        y_sqrt = sqrt_mod(x_res, p)
        if y_sqrt is not None:
            points.append((x, y_sqrt))
            if y_sqrt != 0:
                y2 = (p - y_sqrt) % p
                points.append((x, y2))
        if show_table:
            x_str = f"{x:4}"
            y_squared_str = (x ** 2) % p
            print(f"| {x_str:5} | {x_res:7}     || {x_str:5} | {y_squared_str:7}     |")
    if show_table:
        print("----------------------------------------------")
    return points + ['O']


def is_on_curve(P, a, b, p):
    if P == 'O':
        return True
    x, y = P
    return (y ** 2 % p) == ((x ** 3 + a * x + b) % p)


def point_add(P, Q, a, p, show_steps=False):
    if P == 'O':
        return Q
    if Q == 'O':
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return 'O'
    if P != Q:
        denom = (x2 - x1) % p
        if denom == 0:
            return None
        m = ((y2 - y1) * inverse_mod(denom, p)) % p
    else:
        if y1 == 0:
            return 'O'
        m = ((3 * x1 ** 2 + a) * inverse_mod(2 * y1, p)) % p

    x3 = (m ** 2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    if show_steps:
        print(f"  λ = {m}")
        if P == Q:
            print(f"  x_4 = {x3}")
            print(f"  y_4 = {y3}")
        else:
            print(f"  x_3 = {x3}")
            print(f"  y_3 = {y3}")
    return (x3, y3)


def point_double(P, a, p, show_steps=False):
    return point_add(P, P, a, p, show_steps)


def get_point_from_user(points, prompt, a, b, p):
    while True:
        try:
            s = input(f"\n{prompt} (индекс, 'list', 'O' или 'x y'): ").strip()
            if s.lower() == 'list':
                for i, pt in enumerate(points):
                    print(f"  {i}: {pt}")
                continue
            if s.upper() == 'O':
                return 'O'
            try:
                idx = int(s)
                if 0 <= idx < len(points):
                    return points[idx]
                print("Некорректный индекс.")
                continue
            except ValueError:
                pass
            parts = s.split()
            if len(parts) == 2:
                x, y = int(parts[0]), int(parts[1])
                P = (x, y)
                if is_on_curve(P, a, b, p):
                    return P
                print("Точка не на кривой.")
                continue
            print("Введите индекс, 'O' или 'x y'.")
        except ValueError:
            print("Введите целые числа.")
        except KeyboardInterrupt:
            print("\nВыход.")
            exit(0)


# === Основная программа ===
if __name__ == "__main__":
    print("Эллиптическая кривая: y² ≡ x³ + ax + b (mod p)")
    inp = input("Введите a, b, p (через пробел): ").split()
    if len(inp) == 3:
        a, b, p = int(inp[0]), int(inp[1]), int(inp[2])
    else:
        a = int(input("a = "))
        b = int(input("b = "))
        p = int(input("p = "))

    print(f"\ny² ≡ x³ + {a}x + {b} (mod {p})")
    points = find_curve_points(a, b, p, show_table=True)
    print(f"\nВсе точки: {points[:-1]} и O")
    print(f"ПЭК = {len(points)}")

    if len(points) == 1 and points[0] == 'O':
        print("На кривой только O.")
        exit(0)

    P = get_point_from_user(points, "Точка P", a, b, p)
    Q = get_point_from_user(points, "Точка Q", a, b, p)

    print(f"\nP = {P},  Q = {Q}")
    print("\nP + Q:")
    R = point_add(P, Q, a, p, show_steps=True)
    print(f"R = P + Q = {R}")
    print("\n2P:")
    D = point_double(P, a, p, show_steps=True)
    print(f"2P = {D}")
