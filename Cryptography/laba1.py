def extended_gcd_table(a, b):

    r = [b, a]
    x = [0, 1]   # r0 = a*0 + b*1, r1 = a*1 + b*0
    y = [1, 0]
    q = [None]

    # пока последний остаток != 0, делаем шаг
    while r[-1] != 0:
        qi = r[-2] // r[-1]
        r_new = r[-2] - qi * r[-1]
        x_new = x[-2] - qi * x[-1]
        y_new = y[-2] - qi * y[-1]

        q.append(qi)
        r.append(r_new)
        x.append(x_new)
        y.append(y_new)

    # последний элемент r == 0, убираем его из печати
    n = len(r) - 1  # индекс последнего ненулевого r = n-1
    # печать таблицы
    print(f"{'i':>2} | {'r_i':>6} | {'x_i':>6} | {'y_i':>6} | {'q_i':>3}")
    print("-" * 36)
    for i in range(n):
        q_print = '-' if q[i] is None else str(q[i])
        print(f"{i:>2} | {r[i]:>6} | {x[i]:>6} | {y[i]:>6} | {q_print:>3}")

    gcd = r[n-1]
    x_res = x[n-1]
    y_res = y[n-1]
    return gcd, x_res, y_res


if __name__ == "__main__":
    a, b = 2120, 4399
    g, x, y = extended_gcd_table(a, b)
    print("\nРасширенный алгоритм Евклида:")
    print(f"НОД = {g}, x = {x}, y = {y}")
    print(f"Проверка: {a}*{x} + {b}*{y} = {a*x + b*y}")
