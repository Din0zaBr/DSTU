"""
Вспомогательные функции для работы с числами
"""


def algorithmEuclid(a, b):
    """
    Бинарный алгоритм Евклида для нахождения НОД
    Реализация основана на first_lab/sixth.py
    :param a: первое число
    :param b: второе число
    :return: НОД(a, b)
    """
    # Приводим к положительным значениям
    a, b = abs(a), abs(b)
    
    # Проверка граничных случаев
    if a == 0:
        return b
    if b == 0:
        return a
    if a == 1 or b == 1:
        return 1
    if a == b:
        return a
    
    # Бинарный алгоритм Евклида
    two_degrees = 0
    c, d = a, b
    
    # Основной цикл бинарного алгоритма
    while 1 < c != d > 1:
        if c % 2 == 0 and d % 2 == 0:
            # Оба четные
            c = c // 2
            d = d // 2
            two_degrees += 1
        elif c % 2 == 0:
            # c четное, d нечетное
            c = c // 2
        elif d % 2 == 0:
            # c нечетное, d четное
            d = d // 2
        else:
            # Оба нечетные
            if c > d:
                c = c - d
            else:
                d = d - c
    
    # Определяем результат
    # После цикла одно из чисел будет 0, 1 или они будут равны
    if c == d:
        result = c
    elif c == 0:
        result = d
    elif d == 0:
        result = c
    elif c == 1:
        result = 1
    elif d == 1:
        result = 1
    else:
        # Если цикл завершился, но числа не равны 0 или 1, продолжаем
        result = c if c != 0 else d
    
    # Умножаем на степень двойки
    return result * (2 ** two_degrees)


def razlosh(n):
    """
    Разложение числа на простые множители
    Пример: {2: 4, 3: 2} для 144
    :param n: число для разложения
    :return: словарь {простое_число: степень}
    """
    if n <= 0:
        return {}
    if n == 1:
        return {}
    
    sl = {}
    delitel = 2
    while delitel * delitel <= n:
        if n % delitel == 0:
            sl[delitel] = 0
            while n % delitel == 0:
                n //= delitel
                sl[delitel] += 1
        delitel += 1
    
    if n > 1:
        sl[n] = 1
    
    return sl


def razlozhenie(n):
    """
    Разложение числа на множители (старая версия для совместимости)
    Используется в euler_criterion.py
    """
    sl = {}
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            sl[i] = 0
            while n % i == 0:
                n //= i
                sl[i] += 1
    return sl

