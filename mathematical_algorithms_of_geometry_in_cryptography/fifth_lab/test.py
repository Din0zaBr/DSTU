def mod_inv(n, p):
    return pow(n, p - 2, p)

def find(a, b, p):
    points = []
    for x in range(p):
        x_res = (x ** 3 + a * x + b) % p
        for y in range(p):
            y_res = (y ** 2) % p
            if y_res == x_res:
                points.append((x, y))
    return points

def is_on_curve(P, a, b, p):
    if P is None:
        return True  # Точка на бесконечности
    x, y = P
    return (y**2 % p) == ((x**3 + a*x + b) % p)

def add(P, Q, a, p):
    if P is None:
        return Q
    if Q is None:
        return P
    if P == Q:
        return double(P, a, p)
    if P[0] == Q[0] and P[1] != Q[1]:
        return None

    lam = ((Q[1] - P[1]) * mod_inv(Q[0] - P[0], p)) % p
    print(f"  λ = (({Q[1]} - {P[1]}) * inv({Q[0]} - {P[0]}) mod {p} = {lam}")
    x_r = (lam ** 2 - P[0] - Q[0]) % p
    print(f"  x₃ = λ² - x₁ - x₂ = {lam}² - {P[0]} - {Q[0]} mod {p} = {x_r}")
    y_r = (lam * (P[0] - x_r) - P[1]) % p
    print(f"  y₃ = λ(x₁ - x₃) - y₁ = {lam}({P[0]} - {x_r}) - {P[1]} mod {p} = {y_r}")
    return (x_r, y_r)

def double(P, a, p):
    if P is None:
        return None
    if P[1] == 0:
        return None

    lam = ((3 * P[0] ** 2 + a) * mod_inv(2 * P[1], p)) % p
    print(f"  λ = (3x₁² + a) / (2y₁) = (3*{P[0]}² + {a}) * inv(2*{P[1]}) mod {p} = {lam}")
    x_r = (lam ** 2 - 2 * P[0]) % p
    print(f"  x₂ = λ² - 2x₁ = {lam}² - 2*{P[0]} mod {p} = {x_r}")
    y_r = (lam * (P[0] - x_r) - P[1]) % p
    print(f"  y₂ = λ(x₁ - x₂) - y₁ = {lam}({P[0]} - {x_r}) - {P[1]} mod {p} = {y_r}")
    return (x_r, y_r)

def multiply_numb(k, P, a, p):
    if k == 0:
        return None
    if k == 1:
        return P

    steps = [None] * (k + 1)
    steps[1] = P
    print(f"\nШаг 1: Берем P = {P}")

    for i in range(2, k + 1):
        if i % 2 == 0:
            prev_step = steps[i // 2]
            print(f"\nШаг {i}: Удваиваем {i//2 if i != 2 else ''}P → {i}P")
            steps[i] = double(prev_step, a, p)
            print(f"  Получили: {steps[i]}")
        else:
            step_a = steps[i // 2]
            step_b = steps[i // 2 + 1]
            print(f"\nШаг {i}: Складываем {i//2 if i != 2 and i != 3 else ''}P = {step_a} к {i//2+1}P = {step_b} → {i}P")
            steps[i] = add(step_a, step_b, a, p)
            print(f"  Получили: {steps[i] if steps[i] != None else 'O'}")
    return steps[k] if steps[k] != None else "O - бесконечно удаленная точка"

a, b, p = map(int, input("Введите a, b, p: ").split())
print(f"y² ≡ x³ + {a}x + {b} (mod {p})")
points = find(a, b, p)
print("Все точки", points, 'и О')

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

while True:
    k_input = input("Введите k: ")
    try:
        k = int(k_input)
        if k > 0:
            break
        print("Скаляр должен быть положительным числом.")
    except:
        print("Некорректный ввод")
result = multiply_numb(k, P, a, p)
print(f"\n{k}P = {result}")
