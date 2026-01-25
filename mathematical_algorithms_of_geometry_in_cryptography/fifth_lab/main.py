from typing import List, Tuple, Optional, Union


def mod_inv(n: int, p: int) -> int:
    """Вычисляет обратный элемент n^(-1) mod p."""
    if n == 0:
        raise ZeroDivisionError("division by zero")
    return pow(n, p - 2, p)


def find(a: int, b: int, p: int) -> List[Tuple[int, int]]:
    """Находит все точки эллиптической кривой y² ≡ x³ + ax + b (mod p)."""
    points: List[Tuple[int, int]] = []
    for x in range(p):
        x_res = (x ** 3 + a * x + b) % p
        for y in range(p):
            y_res = (y ** 2) % p
            if y_res == x_res:
                points.append((x, y))
    return points


def is_on_curve(P: Optional[Tuple[int, int]], a: int, b: int, p: int) -> bool:
    """Проверяет, принадлежит ли точка P эллиптической кривой."""
    if P is None:
        return True  # Точка на бесконечности
    x, y = P
    return (y ** 2 % p) == ((x ** 3 + a * x + b) % p)


def add(P: Optional[Tuple[int, int]], Q: Optional[Tuple[int, int]], 
        a: int, p: int) -> Optional[Tuple[int, int]]:
    """Выполняет сложение точек P и Q на эллиптической кривой."""
    if P is None:
        return Q
    if Q is None:
        return P
    if P == Q:
        return double(P, a, p)
    if P[0] == Q[0] and P[1] != Q[1]:
        return None

    denom = (Q[0] - P[0]) % p
    if denom == 0:
        return None
    lam = ((Q[1] - P[1]) * mod_inv(denom, p)) % p
    print(f"  λ = (({Q[1]} - {P[1]}) * inv({Q[0]} - {P[0]}) mod {p} = {lam}")
    x_r = (lam ** 2 - P[0] - Q[0]) % p
    print(f"  x₃ = λ² - x₁ - x₂ = {lam}² - {P[0]} - {Q[0]} mod {p} = {x_r}")
    y_r = (lam * (P[0] - x_r) - P[1]) % p
    print(f"  y₃ = λ(x₁ - x₃) - y₁ = {lam}({P[0]} - {x_r}) - {P[1]} mod {p} = {y_r}")
    return (x_r, y_r)


def double(P: Optional[Tuple[int, int]], a: int, p: int) -> Optional[Tuple[int, int]]:
    """Выполняет удвоение точки P на эллиптической кривой (2P = P + P)."""
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


def multiply_numb(k: int, P: Optional[Tuple[int, int]], a: int, p: int) -> Union[Optional[Tuple[int, int]], str]:
    """Выполняет скалярное умножение: kP."""
    if k == 0:
        return None
    if k == 1:
        return P
    if P is None:
        return None

    steps: List[Optional[Tuple[int, int]]] = [None] * (k + 1)
    steps[1] = P
    print(f"\nШаг 1: Берем P = {P}")

    for i in range(2, k + 1):
        if i % 2 == 0:
            prev_step = steps[i // 2]
            if prev_step is None:
                return None
            step_label = f"{i//2}P" if i != 2 else "P"
            print(f"\nШаг {i}: Удваиваем {step_label} → {i}P")
            steps[i] = double(prev_step, a, p)
            print(f"  Получили: {steps[i]}")
        else:
            step_a = steps[i // 2]
            step_b = steps[i // 2 + 1]
            if step_a is None or step_b is None:
                return None
            a_label = f"{i//2}P" if i != 2 and i != 3 else "P"
            b_label = f"{i//2+1}P"
            print(f"\nШаг {i}: Складываем {a_label} = {step_a} к {b_label} = {step_b} → {i}P")
            steps[i] = add(step_a, step_b, a, p)
            print(f"  Получили: {steps[i] if steps[i] is not None else 'O'}")
    
    result = steps[k]
    return result if result is not None else "O - бесконечно удаленная точка"


if __name__ == "__main__":
    try:
        a, b, p = map(int, input("Введите a, b, p: ").split())
        if p < 2:
            print("Ошибка: p должно быть >= 2")
            exit(1)
    except ValueError:
        print("Ошибка: введите три целых числа через пробел")
        exit(1)

    print(f"y² ≡ x³ + {a}x + {b} (mod {p})")
    points = find(a, b, p)
    print("Все точки", points, 'и О')

    while True:
        P_input = input("\nВведите координаты P (x y): ")
        if P_input.lower() == 'exit':
            exit(0)
        try:
            Px, Py = map(int, P_input.split())
            P: Optional[Tuple[int, int]] = (Px, Py)
            if is_on_curve(P, a, b, p):
                break
            print("Точка P не принадлежит кривой")
        except ValueError:
            print("Некорректный ввод: введите два целых числа")
        except Exception as e:
            print(f"Ошибка: {e}")

    while True:
        k_input = input("Введите k: ")
        try:
            k = int(k_input)
            if k > 0:
                break
            print("Скаляр должен быть положительным числом.")
        except ValueError:
            print("Некорректный ввод: введите целое число")
        except KeyboardInterrupt:
            print("\nВыход.")
            exit(0)

    result = multiply_numb(k, P, a, p)
    print(f"\n{k}P = {result}")
