def mod_inv(n, p):
    if n % p == 0:
        return 0
    return pow(n, p - 2, p)

def is_on_curve(P, a, b, p):
    if P is None:
        return True
    x, y = P
    return (y**2 % p) == ((x**3 + a*x + b) % p)

def add_points(P, Q, a, p):
    if P is None or P == (0, 0):
        return Q
    if Q is None or Q == (0, 0):
        return P
    if P == Q:
        return double_point(P, a, p)
    if P[0] == Q[0] and P[1] != Q[1]:
        return (0, 0)

    lam = ((Q[1] - P[1]) * mod_inv(Q[0] - P[0], p)) % p
    x_r = (lam ** 2 - P[0] - Q[0]) % p
    y_r = (lam * (P[0] - x_r) - P[1]) % p
    return (x_r, y_r)


def find_period(sequence):
    for start in range(len(sequence)):
        for period in range(1, len(sequence) - start):
            if sequence[start:start + period] == sequence[start + period:start + 2 * period]:
                return period
    return None

def double_point(P, a, p):
    if P is None:
        return None
    if P[1] == 0:
        return None

    lam = ((3 * P[0] ** 2 + a) * mod_inv(2 * P[1], p)) % p
    x_r = (lam ** 2 - 2 * P[0]) % p
    y_r = (lam * (P[0] - x_r) - P[1]) % p
    return (x_r, y_r)

def scalar_multiply(k, P, a, p):
    R = None
    Q = P
    while k > 0:
        if k % 2 == 1:
            R = add_points(R, Q, a, p)
        Q = double_point(Q, a, p)
        k //= 2
    return R

def ec_congruential_generator(seed_point, c, P, a, p, count):
    sequence = [seed_point]
    Xi = seed_point
    for _ in range(count):
        try:
            Xi = add_points(scalar_multiply(c, Xi, a, p), P, a, p)
            sequence.append(Xi)
        except Exception as e:
            print(f"Ошибка при генерации элемента: {e}")
            sequence.append(None)
    return sequence

def inverse_point(P, p):
    if P is None:
        return None
    x, y = P
    return (x, (-y) % p)

def ec_inversive_generator(seed_point, c, P, a, p, count):
    sequence = [seed_point]
    Xi = seed_point
    for _ in range(count):
        neg_Xi = inverse_point(Xi, p)
        temp = add_points(scalar_multiply(c, neg_Xi, a, p), P, a, p)
        Xi = temp
        sequence.append(Xi)
    return sequence


def find_points(a, b, p):
    points = []
    for x in range(p):
        rhs = (x**3 + a*x + b) % p
        for y in range(p):
            if (y * y) % p == rhs:
                points.append((x, y))
    return points

a, b, p = map(int, input("Введите параметры (a b p): ").split())
print(f"\nЭК: y² ≡ x³ + {a}x + {b} (mod {p})")

all_points = find_points(a, b, p)
print("\nВсе точки ЭК:")
for pt in all_points:
    print(pt, end=' ')
print("\n")

while True:
    x0, y0 = map(int, input(" X0 (x y): ").split())
    X0 = (x0, y0)
    if is_on_curve(X0, a, b, p):
        break
    print("X0 не принадлежит кривой. Введите заново.")

while True:
    xP, yP = map(int, input(" P (x y): ").split())
    P = (xP, yP)
    if is_on_curve(P, a, b, p):
        break
    print("P не принадлежит кривой. Введите заново.")


c = int(input("Скаляр c: "))
count = int(input("Количество элементов: "))

if X0 not in all_points:
    print("X0 не принадлежит кривой!")
elif P not in all_points:
    print("P не принадлежит кривой!")
else:
    X_check = add_points(scalar_multiply(c, X0, a, p), P, a, p)
    if X_check == X0:
        print("Условие c*X0 + P != X0 не выполнено!")
    else:
        print("\nЛинейный генератор")
        lcg_seq = ec_congruential_generator(X0, c, P, a, p, p*100)
        print(lcg_seq[:count])
        plcg = find_period(lcg_seq)
        print("Период:", plcg)

        print("\nИнверсной генератор")
        ig_seq = ec_inversive_generator(X0, c, P, a, p, p*100)
        print(ig_seq[:count])
        pig = find_period(ig_seq)
        print("Период:", pig)
