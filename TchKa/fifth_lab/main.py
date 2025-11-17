"""
Главный модуль для вычисления символа Лежандра/Якоби
"""

from functools import reduce
from utils import algorithmEuclid, razlosh
from euler_criterion import legendre_by_euler
from legendre_properties import symbol_Lezh


def main():
    """
    Главная функция для вычисления символа Лежандра/Якоби
    """
    print("=" * 60)
    print(" " * 15 + "СИМВОЛ ЛЕЖАНДРА/ЯКОБИ")
    print("=" * 60)
    print()
    print("Программа вычисляет символ Лежандра (a/p) или символ Якоби")
    print("для заданных чисел a и p.")
    print()
    
    a = int(input('Введите число a >> '))
    p = int(input('Введите число p >> '))
    print()

    print("┌─ Проверка взаимной простоты ─┐")
    nod = algorithmEuclid(abs(a), p)
    print(f'НОД({abs(a)}, {p}) = {nod}')
    if nod != 1:
        print(f'└────────────────────────────────┘')
        print()
        print(f'НОД({abs(a)}, {p}) ≠ 1')
        print(f'Символ Лежандра ({a}/{p}) = 0')
        return
    print(f'└────────────────────────────────┘')
    print()

    r = razlosh(p)
    znam = []
    print("┌─ Определение типа символа ─┐")
    if len(r) != 0:
        print(f'p = {p} - составное число')
        print(f'Разложение: p = ', end='')
        factors_str = []
        for key, item in r.items():
            for _ in range(item):
                znam.append(key)
            if item == 1:
                factors_str.append(str(key))
            else:
                factors_str.append(f'{key}^{item}')
        print(' · '.join(factors_str))
        print(f'Используем символ Якоби')
    else:
        print(f'p = {p} - простое число')
        print(f'→ Используем символ Лежандра')
        znam = [p]
    print(f'└──────────────────────────────┘')
    print()

    print("┌─ Выбор метода вычисления ─┐")
    print("Доступные методы:")
    print("  1. Критерий Эйлера")
    print("     (a/p) = a^((p-1)/2) (mod p)")
    print("  2. Свойства символа Лежандра")
    print("     (применение свойств 1-7)")
    print(f'└─────────────────────────────┘')
    ch = int(input('\nВыберите метод (1 или 2) >> '))
    print()

    print("=" * 60)
    print(f"НАЧАЛО ВЫЧИСЛЕНИЯ: ({a}/{p})")
    print("=" * 60)
    answer = []
    if a < 0:
        a_abs = abs(a)
        print()
        print("┌─ Обработка отрицательного числа ─┐")
        print(f'  ({a}/{p}) = (-1/{p}) · ({a_abs}/{p})')
        if p % 4 == 1:
            print(f'  (-1/{p}) = 1 (так как p = {p} ≡ 1 (mod 4))')
            print(f'  → ({a}/{p}) = 1 · ({a_abs}/{p}) = ({a_abs}/{p})')
            answer.append(1)
        elif p % 4 == 3:
            print(f'  (-1/{p}) = -1 (так как p = {p} ≡ 3 (mod 4))')
            print(f'  → ({a}/{p}) = -1 · ({a_abs}/{p}) = -({a_abs}/{p})')
            answer.append(-1)
        print(f'└──────────────────────────────────┘')
        a = a_abs
        print()
    if ch == 1:
        # Вычисление через критерий Эйлера
        print("=" * 60)
        print("ВЫЧИСЛЕНИЕ ЧЕРЕЗ КРИТЕРИЙ ЭЙЛЕРА")
        print("=" * 60)
        for i in znam:
            print(f'\n┌─ Вычисляем ({a}/{i}) ─┐')
            znach = legendre_by_euler(a, i)
            # Обработка случая, когда функция вернула None
            if znach is None:
                print(f'\n Ошибка: НОД({a}, {i}) != 1, символ Лежандра не определен')
                return
            answer.append(znach)
            print(f'└─ Результат: ({a}/{i}) = {znach} ─┘')
    elif ch == 2:
        print("=" * 60)
        print("ВЫЧИСЛЕНИЕ ЧЕРЕЗ СВОЙСТВА СИМВОЛА ЛЕЖАНДРА")
        print("=" * 60)
        for i in znam:
            print(f'\n┌─ Вычисляем ({a}/{i}) ─┐')
            znach = symbol_Lezh(a, i)
            answer.append(znach)
            print(f'└─ Результат: ({a}/{i}) = {znach} ─┘')
    
    # Финальный результат
    print()
    print("=" * 60)
    print("ИТОГОВЫЙ РЕЗУЛЬТАТ")
    print("=" * 60)
    if len(znam) > 1:
        print(f'({a}/{p}) = ', end='')
        for i, z in enumerate(znam):
            if i > 0:
                print(' · ', end='')
            print(f'({a}/{z})', end='')
        print(' = ', end='')
        for i, val in enumerate(answer):
            if i > 0:
                print(' · ', end='')
            print(f'{val}', end='')
        print(f' = {reduce(lambda x, y: x * y, answer, 1)}')
    else:
        print(f'({a}/{p}) = {answer[0]}')
    print("=" * 60)


if __name__ == '__main__':
    main()

