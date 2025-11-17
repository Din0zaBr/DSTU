"""
Модуль для вычисления символа Лежандра через свойства
"""

from utils import razlosh


def _apply_property_1_reduction(a, p):
    """
    Свойство 1: Приведение по модулю
    (a + kp)/p = (a mod p)/p
    """
    if a >= p:
        k = a // p
        remainder = a % p
        print(f'\n  [Свойство 1: Приведение по модулю]')
        print(f'  ({a}/{p}) = ({p}·{k} + {remainder}/{p}) = ({remainder}/{p})', end='')
        return remainder
    return a


def _apply_property_2_square_extraction(a, p, factors):
    """
    Свойство 2: Вынесение полных квадратов
    (a * b^2)/p = a/p
    """
    # Проверяем, есть ли множители со степенью >= 2
    has_squares = any(power >= 2 for power in factors.values())
    if not has_squares:
        return a, False
    
    # Сохраняем знак
    sign = 1 if a >= 0 else -1
    
    # Выносим полные квадраты
    square_part = 1
    new_a = 1
    
    for prime, power in factors.items():
        if power >= 2:
            # Выносим полный квадрат: если power = 4, выносим 2^2, остается 1
            # Если power = 3, выносим 2^1, остается 2^1
            squares_to_extract = power // 2
            remaining_power = power % 2
            
            square_part *= (prime ** squares_to_extract)
            if remaining_power > 0:
                new_a *= (prime ** remaining_power)
        else:
            # Степень < 2, оставляем как есть
            new_a *= (prime ** power)
    
    # Восстанавливаем знак
    new_a = sign * new_a
    
    print(f'\n  [Свойство 2: Вынесение полных квадратов]')
    print(f'  ({a}/{p}) = ({new_a}·{square_part}²/{p}) = ({new_a}/{p})', end='')
    return new_a, True


def _apply_property_3_multiplicativity(a, p, factors):
    """
    Свойство 3: Мультипликативность
    (a * b)/p = (a/p) * (b/p)
    """
    if len(factors) == 0 or (len(factors) == 1 and a in factors and factors[a] == 1):
        return None
    
    # Разбиваем на простые множители
    primes = list(factors.keys())
    symbols = [f'({prime}/{p})' for prime in primes]
    print(f'\n  [Свойство 3: Мультипликативность]')
    print(f'  ({a}/{p}) = {" · ".join(symbols)}')
    print(f'  Вычисляем каждый символ:')
    
    result = 1
    values = []
    for i, prime in enumerate(primes, 1):
        print(f'    {i}. ({prime}/{p})', end='')
        # Рекурсивный вызов для каждого простого множителя
        symbol_value = symbol_Lezh(prime, p)
        values.append(symbol_value)
        result *= symbol_value
        if i < len(primes):
            print(f' = {symbol_value} (продолжаем...)')
        else:
            print(f' = {symbol_value}')
    
    print(f'  Итого: ({a}/{p}) = {" · ".join(str(v) for v in values)} = {result}')
    return result


def _apply_property_4_minus_one(p):
    """
    Свойство 4: Символ Лежандра для -1
    (-1/p) = 1, если p ≡ 1 (mod 4)
    (-1/p) = -1, если p ≡ 3 (mod 4)
    """
    print(f'\n  [Свойство 4: Символ для -1]')
    if p % 4 == 1:
        print(f'  p = {p} ≡ 1 (mod 4) → (-1/{p}) = 1')
        return 1
    elif p % 4 == 3:
        print(f'  p = {p} ≡ 3 (mod 4) → (-1/{p}) = -1')
        return -1


def _apply_property_6_two(p):
    """
    Свойство 6: Символ Лежандра для 2
    (2/p) = 1, если p ≡ ±1 (mod 8)
    (2/p) = -1, если p ≡ ±3 (mod 8)
    """
    print(f'\n  [Свойство 6: Символ для 2]')
    p_mod_8 = p % 8
    if p_mod_8 == 1 or p_mod_8 == 7:
        print(f'  p = {p} ≡ {p_mod_8} (mod 8) → (2/{p}) = 1')
        return 1
    elif p_mod_8 == 3 or p_mod_8 == 5:
        print(f'  p = {p} ≡ {p_mod_8} (mod 8) → (2/{p}) = -1')
        return -1


def _apply_property_7_reciprocity(a, p):
    """
    Свойство 7: Закон квадратичной взаимности
    (a/p) = (-1)^((a-1)/2 * (p-1)/2) * (p/a)
    """
    print(f'\n  [Свойство 7: Закон квадратичной взаимности]')
    exp_a = (a - 1) // 2
    exp_p = (p - 1) // 2
    exponent = exp_a * exp_p
    sign = (-1) ** exponent
    
    print(f'  ({a}/{p}) = (-1)^(({a}-1)/2 · ({p}-1)/2) · ({p}/{a})')
    print(f'           = (-1)^({exp_a} · {exp_p}) · ({p}/{a})')
    print(f'           = (-1)^{exponent} · ({p}/{a})')
    print(f'           = {sign} · ({p}/{a})')
    print(f'  Вычисляем ({p}/{a}):')
    
    # Рекурсивный вызов
    reciprocal_value = symbol_Lezh(p, a)
    result = sign * reciprocal_value
    
    print(f'  Итого: ({a}/{p}) = {sign} · {reciprocal_value} = {result}')
    return result


def symbol_Lezh(a, p):
    """
    Функция для подсчета символа Лежандра с использованием свойств
    
    Свойства символа Лежандра:
    1. Приведение по модулю: (a + kp)/p = (a mod p)/p
    2. Вынесение: (a * b^2)/p = a/p
    3. Мультипликативность: (a * b)/p = (a/p) * (b/p)
    4. Символ для -1: (-1/p) зависит от p mod 4
    6. Символ для 2: (2/p) зависит от p mod 8
    7. Закон взаимности: (a/p) = (-1)^((a-1)/2 * (p-1)/2) * (p/a)
    
    :param a: числитель
    :param p: простое число в знаменателе
    :return: значение символа Лежандра (a/p)
    """
    while True:
        # Свойство 4: Символ для 1
        if a == 1:
            print(f'\n  [Свойство 4: Символ для 1]')
            print(f'  (1/{p}) = 1')
            return 1
        
        # Свойство 4: Символ для -1
        if a == -1:
            return _apply_property_4_minus_one(p)
        
        # Свойство 6: Символ для 2
        if a == 2:
            return _apply_property_6_two(p)
        
        # Свойство 1: Приведение по модулю
        old_a = a
        a = _apply_property_1_reduction(a, p)
        if a == 0:
            return 0
        if a != old_a:
            # Применено свойство 1, продолжаем с новым значением
            continue
        
        # Разложение на множители (используем abs для отрицательных чисел)
        factors = razlosh(abs(a))
        
        # Свойство 2: Вынесение полных квадратов
        a, square_extracted = _apply_property_2_square_extraction(a, p, factors)
        if square_extracted:
            # Продолжаем с упрощенным значением
            continue
        
        # Обновляем разложение после возможных изменений
        factors = razlosh(abs(a))
        
        # Свойство 7: Закон взаимности (если a - простое число)
        if len(factors) == 1 and abs(a) in factors and factors[abs(a)] == 1:
            return _apply_property_7_reciprocity(abs(a), p)
        
        # Свойство 3: Мультипликативность
        # Применяем только если есть несколько простых множителей
        if len(factors) > 1:
            result = _apply_property_3_multiplicativity(abs(a), p, factors)
            if result is not None:
                return result
        
        # Если дошли сюда и a - простое число, применяем свойство 7
        if len(factors) == 1 and abs(a) in factors and factors[abs(a)] == 1:
            return _apply_property_7_reciprocity(abs(a), p)
        
        # Если ни одно свойство не применилось, это ошибка
        raise ValueError(f"Не удалось вычислить символ Лежандра для ({a}/{p})")

