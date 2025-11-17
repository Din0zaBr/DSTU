"""
Модуль для вычисления символа Лежандра через критерий Эйлера
(a/p) = a^((p-1)/2) (mod p)
"""

from functools import reduce
from utils import algorithmEuclid, razlozhenie


def func_Eilera(m):
    """
    Функция Эйлера φ(m)
    """
    if m == 1:
        print(f'ф({m}) = 1')
        return 1
    sl = razlozhenie(m)
    if len(sl) == 0:
        print(f'ф({m}) = {m - 1}')
        return m - 1
    else:
        zn = m
        st = f'ф({m}) = {zn}'
        for i in sl.keys():
            zn *= (1 - 1 / i)
            st += f' * (1 - 1/{i})'
        st += f' = {int(zn)}'
        print(st)
        return int(zn)


def t_Pherma(m):
    """
    Теорема Ферма: для простого m, φ(m) = m - 1
    """
    print('Используем теорему Ферма')
    return m - 1


def t_Eilera(m):
    """
    Теорема Эйлера: вычисление функции Эйлера для составного m
    """
    print('Используем теорему Эйлера')
    return func_Eilera(m)


def compute_power_mod(a, m, st):
    """
    Вычисление a^st (mod m) с подробным выводом
    :param a: основание
    :param m: модуль
    :param st: степень
    :return: a^st (mod m)
    """
    if a < 0:
        while a < 0:
            a += m

    print()
    print("┌─ Шаг 1: Проверка взаимной простоты ─┐")
    nod = algorithmEuclid(a, m)
    print(f'НОД({a}, {m}) = {nod}')
    if nod != 1:
        print('Введены некорректные данные, попробуйте ещё раз')
        return None
    print("└──────────────────────────────────────┘")
    print()

    # Определяем теорему
    print("┌─ Шаг 2: Определение теоремы ─┐")
    if len(razlozhenie(m)) == 0:
        n_st = t_Pherma(m)
    else:
        n_st = t_Eilera(m)
    print(f'→ {a}^{n_st} ≡ 1 (mod {m})')
    print("└──────────────────────────────────────┘")
    print()

    # Упрощаем степень
    print("┌─ Шаг 3: Упрощение степени ─┐")
    c_st = st % n_st
    if st != c_st:
        print(f'{a}^{st} (mod {m}) = ({a}^{n_st})^{st // n_st} * {a}^{c_st} (mod {m})')
        print(f'         = 1^{st // n_st} * {a}^{c_st} (mod {m})')
        print(f'         = {a}^{c_st} (mod {m})')
    else:
        print(f'Степень {st} уже упрощена: {a}^{c_st} (mod {m})')
    print("└─────────────────────────────┘")
    print()

    # Приведение основания по модулю
    if a >= m:
        print("┌─ Шаг 4: Приведение основания ─┐")
        old_a = a
        a = a % m
        print(f'{old_a} ≡ {a} (mod {m})')
        print(f'→ {old_a}^{c_st} (mod {m}) = {a}^{c_st} (mod {m})')
        print("└───────────────────────────────┘")
        print()

    # Быстрое возведение в степень
    print("┌─ Шаг 5: Быстрое возведение в степень ─┐")
    mn = []
    step_num = 1
    current_power = c_st
    current_base = a

    while current_power != 1:
        if current_power % 2 != 0:
            print(f'  Шаг {step_num}.1: Степень нечетная → выносим множитель {current_base}')
            mn.append(current_base)
            current_power -= 1
        else:
            print(f'  Шаг {step_num}.1: Степень четная → можно возвести в квадрат')

        print(f'  Шаг {step_num}.2: ({current_base}²)^{current_power // 2} (mod {m})')
        squared = current_base ** 2
        if squared >= m:
            squared_mod = squared % m
            print(f'            = [{squared} ≡ {squared_mod} (mod {m})]')
            print(f'            = {squared_mod}^{current_power // 2} (mod {m})')
        else:
            print(f'            = {squared}^{current_power // 2} (mod {m})')

        current_base = (current_base ** 2) % m
        current_power //= 2
        step_num += 1

    # Финальное вычисление
    if mn:
        print(f'  Финальный шаг: Перемножаем вынесенные множители')
        print(f'    {current_base}', end='')
        for i in mn:
            print(f' * {i}', end='')
        print()
        result = reduce(lambda x, y: x * y, mn, current_base)
    else:
        result = current_base

    final_result = result % m
    print(f'  Результат: {result} ≡ {final_result} (mod {m})')
    print("└───────────────────────────────────────┘")
    print()

    return final_result


def legendre_by_euler(a, p):
    """
    Вычисление символа Лежандра через критерий Эйлера
    (a/p) = a^((p-1)/2) (mod p)
    :param a: числитель
    :param p: простое число в знаменателе
    :return: значение символа Лежандра (a/p) ∈ {-1, 0, 1}
    """
    print(f"Критерий Эйлера: ({a}/{p}) = {a}^(({p}-1)/2) (mod {p})")
    print(f"                 = {a}^{(p - 1) // 2} (mod {p})")
    print()

    exponent = (p - 1) // 2
    result = compute_power_mod(a, p, exponent)

    if result is None:
        return None

    # Приводим результат к диапазону [-1, 1]
    print("┌─ Шаг 6: Приведение к символу Лежандра ─┐")
    if result == 1:
        print(f'{result} ≡ 1 (mod {p}) → ({a}/{p}) = 1')
    elif result == p - 1:
        print(f'{result} ≡ -1 (mod {p}) → ({a}/{p}) = -1')
    else:
        print(f'{result} (mod {p})')
        if result > 1:
            result -= p
            print(f'→ {result + p} ≡ {result} (mod {p}) → ({a}/{p}) = {result}')
    print("└─────────────────────────────────────────┘")
    print()

    return result
