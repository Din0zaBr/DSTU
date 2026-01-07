from functools import reduce
from TchKa.first_lab.sixth import binary_euclid, final


def factorization(n):
    """
    Разлагает число n на простые множители.
    
    Возвращает словарь, где ключи - простые числа, значения - их степени.
    """
    factors = {}
    temp_n = n
    for i in range(2, temp_n // 2 + 1):
        if temp_n % i == 0:
            factors[i] = 0
            while temp_n % i == 0:
                temp_n //= i
                factors[i] += 1
    return factors


def compute_gcd(a, b):
    """
    Вычисляет НОД двух чисел с помощью бинарного алгоритма Евклида.
    """
    a_check, b_check, degree_2 = binary_euclid(abs(a), abs(b))
    return final(a_check, b_check, degree_2)


def legendre_symbol(a, p):
    """
    Вычисляет символ Лежандра (a/p) используя свойства символа Лежандра.
    
    Свойства:
    1. Если a >= p, то (a/p) = (a mod p / p)
    2. Если a имеет квадратичные множители, их можно вынести
    3. Мультипликативность: (ab/p) = (a/p) * (b/p)
    4. (-1/p) = 1, если p ≡ 1 (mod 4), иначе -1
    5. (1/p) = 1
    6. (2/p) = 1, если p ≡ ±1 (mod 8), иначе -1
    7. Квадратичный закон взаимности: (a/p) = (-1)^((a-1)/2 * (p-1)/2) * (p/a)
    """
    while True:
        factors = factorization(a)
        
        # Свойство 5: (1/p) = 1
        if a == 1:
            print(' =4= 1')
            return 1
        
        # Свойство 4: (-1/p)
        elif a == -1:
            if p % 4 == 1:
                print(' =4= 1')
                return 1
            elif p % 4 == 3:
                print(' =4= -1')
                return -1
        
        # Свойство 6: (2/p)
        elif a == 2:
            if p % 8 == 1 or p % 8 == 7:
                print(' =6= 1')
                return 1
            elif p % 8 == 3 or p % 8 == 5:
                print(' =6= -1')
                return -1
        
        # Свойство 2: вынесение квадратичных множителей
        elif sum(factors.values()) > len(factors):
            square_factor = 1
            for prime, power in factors.items():
                if power >= 2:
                    square_factor *= prime
                    a //= prime ** 2
            print(f' =2= (({a} * {square_factor}^2)/{p}) = ({a}/{p})', end='')
        
        # Свойство 1: приведение по модулю
        elif a >= p:
            remainder = a % p
            quotient = a // p
            print(f' =1= (({p} * {quotient} + {remainder})/{p}) = ({remainder}/{p})', end='')
            a = remainder
        
        # Свойство 7: квадратичный закон взаимности (когда a простое)
        elif len(factors) == 0:
            exponent = ((a - 1) // 2) * ((p - 1) // 2)
            sign = (-1) ** exponent
            print(f' =7= (-1)^(({a} - 1)/2 * ({p} - 1)/2) * ({p}/{a}) = '
                  f'(-1)^({(a - 1) // 2} * {(p - 1) // 2}) * ({p}/{a}) = {sign} * ({p}/{a}) = [')
            print(f'    ({p}/{a})', end='')
            result = legendre_symbol(p, a)
            print(f'  ] = {sign} * {result} = {sign * result}')
            return sign * result
        
        # Свойство 3: мультипликативность
        else:
            answer = 1
            factors_list = []
            for prime in factors.keys():
                factors_list.append(f'({prime}/{p})')
            print(' =3= ' + ' * '.join(factors_list) + ' = [')
            for prime in factors.keys():
                print(f'    ({a}/{prime})', end='')
                symbol_value = legendre_symbol(prime, p)
                answer *= symbol_value
            print(f'  ] = {answer}')
            return answer


def jacobi_symbol(a, p):
    """
    Вычисляет символ Якоби (a/p), где p может быть составным числом.
    
    Символ Якоби вычисляется через разложение p на простые множители
    и применение символа Лежандра к каждому множителю.
    """
    factors = factorization(p)
    prime_factors = []
    
    # Разложение p на простые множители (с учетом кратности)
    for prime, power in factors.items():
        for _ in range(power):
            prime_factors.append(prime)
    
    if len(prime_factors) == 0:
        # p простое - используем символ Лежандра
        return legendre_symbol(a, p)
    else:
        # p составное - используем символ Якоби
        results = []
        for prime in prime_factors:
            print(f'  ({a}/{prime})', end='')
            result = legendre_symbol(a, prime)
            results.append(result)
            print()
        return reduce(lambda x, y: x * y, results, 1)


def main():
    """
    Основная функция для вычисления символа Лежандра/Якоби.
    
    Предлагает пользователю выбрать способ вычисления:
    1. Через критерий Эйлера
    2. При помощи свойств символа Лежандра
    """
    print('=' * 60)
    print('Вычисление символа Лежандра/Якоби')
    print('=' * 60)
    
    try:
        a = int(input('Введите число a >> '))
        p = int(input('Введите число p >> '))
        print()
        
        # Проверка взаимной простоты
        gcd = compute_gcd(abs(a), p)
        if gcd != 1:
            print(f'НОД({abs(a)}, {p}) = {gcd}')
            print(f'({a}/{p}) = 0')
            return
        
        # Определение типа символа
        factors = factorization(p)
        prime_factors = []
        if len(factors) != 0:
            print('Для нахождения ответа определяем символ Якоби')
            for prime, power in factors.items():
                for _ in range(power):
                    prime_factors.append(prime)
        else:
            print('Для нахождения ответа определим символ Лежандра')
            prime_factors = [p]
        print()
        
        # Выбор способа вычисления
        method = int(input('Выберите способ подсчёта:\n'
                          '1. Через критерий Эйлера\n'
                          '2. При помощи свойств\n'
                          'Введите число >> '))
        print()
        
        # Обработка отрицательного a
        print(f'({a}/{p})', end='')
        answer = []
        if a < 0:
            abs_a = abs(a)
            print(f'= (-1/{p}) * ({abs_a}/{p}) = ', end='')
            if p % 4 == 1:
                print(f'[(-1/{p}) =(4)= 1] = ({abs_a}/{p}) (=)')
                answer.append(1)
            elif p % 4 == 3:
                answer.append(-1)
                print(f'[(-1/{p}) =(4)= -1] = (-1) * ({abs_a}/{p}) (=)')
            a = abs_a
        else:
            print(' (=)')
        print()
        
        # Вычисление символа
        if method == 1:
            # Метод 1: Критерий Эйлера
            print('Используем критерий Эйлера:')
            print('(a/p) ≡ a^((p-1)/2) (mod p)')
            print()
            for prime in prime_factors:
                exponent = (prime - 1) // 2
                # Вычисляем a^exponent mod prime
                value = pow(a, exponent, prime)
                # Приводим к диапазону [-1, 1] для символа Лежандра
                if value > prime // 2:
                    value -= prime
                answer.append(value)
                print(f'({a}/{prime}) ≡ {a}^({exponent}) ≡ {value} (mod {prime})')
        elif method == 2:
            # Метод 2: Свойства символа Лежандра
            print('Используем свойства символа Лежандра:')
            print()
            for prime in prime_factors:
                answer.append(legendre_symbol(a, prime))
                print()
        
        # Финальный результат
        final_answer = reduce(lambda x, y: x * y, answer, 1)
        print('=' * 60)
        print('РЕЗУЛЬТАТ:')
        print('=' * 60)
        print(f'({a}/{p}) = {int(final_answer)}')
        
    except ValueError:
        print('\nОшибка: Введите корректные целые числа')
    except Exception as e:
        print(f'\nОшибка: {e}')


if __name__ == '__main__':
    main()

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
    # Проверяем, является ли p простым числом
    # Простое число: разложение содержит только само число в степени 1
    is_prime = len(r) == 1 and p in r and r[p] == 1
    
    if is_prime:
        print(f'p = {p} - простое число')
        print(f'→ Используем символ Лежандра')
        znam = [p]
    else:
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

