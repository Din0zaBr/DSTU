def mod_inv(n, p):
    return pow(n, p - 2, p)

def find(a, b, p):
    points = []
    print("----------------------------------------------")
    print("|   x   | x³ + ax + b ||   y   |   y² mod p  |")
    print("----------------------------------------------")

    for x in range(p):
        x_res = (x ** 3 + a * x + b) % p
        for y in range(p):
            y_res = (y ** 2) % p
            if y_res == x_res:
                points.append((x, y))
        x_str = f"{x:4}"
        y_squared_str = (x ** 2) % p
        print(f"| {x_str:5} | {x_res:7}     || {x_str:5} | {y_squared_str:7}     |")
    print("----------------------------------------------")
    return points

def is_on_curve(P, a, b, p):
    x, y = P
    return (y**2 % p) == ((x**3 + a*x + b) % p)

def add(P, Q, a, p):
    if P == Q:
        return double(P, a, p)
    if P[0] == Q[0] and P[1] != Q[1]:
        return None
    print(f'({Q[1]} - {P[1]}) *  {mod_inv(Q[0] - P[0], p)}) % {p} {Q[0]}{P[0]}')
    lam = ((Q[1] - P[1]) * mod_inv(Q[0] - P[0], p)) % p
    print("λ =", lam)
    print(f'({lam ** 2} (** 2) - {P[0]} - {Q[0]}) % {p}')
    x_r = (lam ** 2 - P[0] - Q[0]) % p
    print("x_3 =", x_r)
    print(f'({lam} * ({P[0]} - {x_r}) - {P[1]}) % {p}')
    y_r = (lam * (P[0] - x_r) - P[1]) % p
    print("y_3 =", y_r)
    return (x_r, y_r)

def double(P, a, p):
    if P[1] == 0:
        return None
    lam = ((3 * P[0] ** 2 + a) * mod_inv(2 * P[1], p)) % p
    print("λ =", lam)
    x_r = (lam ** 2 - 2 * P[0]) % p
    print("x_4 =", x_r)
    y_r = (lam * (P[0] - x_r) - P[1]) % p
    print("y_4 =", y_r)
    return (x_r, y_r)

a, b, p = map(int, input("Введите a, b, p: ").split())
print(f"y² ≡ x³ + {a}x + {b} (mod {p})")
points = find(a, b, p)
print("Все точки:", points, 'и О')
print("ПЭК =", len(points)+1)

while True:
    Px, Py = map(int, input("\nВведите координаты P (x y): ").split())
    P = (Px, Py)
    if is_on_curve(P, a, b, p):
        break
    print("Точка P не принадлежит кривой. Введите заново.")

while True:
    Qx, Qy = map(int, input("Введите координаты Q (x y): ").split())
    Q = (Qx, Qy)
    if is_on_curve(Q, a, b, p):
        break
    print("Точка Q не принадлежит кривой. Введите заново.")

sum_PQ = add(P, Q, a, p)
print(f"R = P + Q = {sum_PQ}\n")
double_P = double(P, a, p)
print(f"2P = {double_P}")
