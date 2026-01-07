import random
import math
from typing import Optional


def Miller_Rubbin(n: int, a: int) -> bool:
    """
    Выполняет один раунд теста Миллера-Рабина для числа n с основанием a.
    
    Args:
        n: Число для проверки на простоту
        a: Основание (witness) для теста
    
    Returns:
        True, если число прошло тест (вероятно простое)
        False, если число не прошло тест (составное)
    """
    # Представляем n-1 как 2^s * t, где t - нечетное
    t = n - 1
    s = 0
    while t % 2 == 0:
        t //= 2
        s += 1
    print(f"Шаг 1.  n-1 = {n-1} = 2^s*t = 2^{s} * {t}")

    # Шаг 2: Выбор основания a (уже выбрано при вызове функции)
    print(f"Шаг 2. Выбрано основание a = {a}")

    # Шаг 3: Проверка взаимной простоты n и a
    gcd_value = math.gcd(n, a)
    print(f"Шаг 3. НОД({a}, {n}) = {gcd_value}")
    if gcd_value != 1:
        print(f"НОД({a}, {n}) != 1. Завершить тест.")
        return False

    # Вычисляем a^t mod n
    b = pow(a, t, n)
    print(f"Шаг 4. b = a^t (mod n) = {a}^{t} (mod {n}) = {b}")

    # Если b == 1 или b == n-1, число проходит тест
    if b in (1, n - 1):
        print("Выполнилось условие шага 4. b == 1 или b == n - 1. Конец алгоритма.")
        return True

    # Проверяем последовательность b^2, b^4, ..., b^(2^(s-1))
    for k in range(s - 1):
        print("Не выполнилось условие шага 4. b != 1 или b != n - 1")
        b = pow(b, 2, n)
        print(f"Шаг 5. Вычислить b = b^2 (mod n) = {b}, K={k}")
        print(f"Шаг 6. Проверка: b == n-1? {b} == {n - 1}?")
        if b == n - 1:
            print("Шаг 6. Условие b == n-1 выполнено. Конец алгоритма.")
            return True
        print(f"Шаг 7. Условие b == n-1 не выполнилось. Возвращаемся к предущим шагам если {k+2} < {s}")
    return False


def miller_rabin_test(n: int, num_tests: int = 5) -> Optional[bool]:
    """
    Проводит тест Миллера-Рабина для числа n с несколькими случайными основаниями.
    
    Args:
        n: Число для проверки на простоту
        num_tests: Количество раундов теста (по умолчанию 5)
    
    Returns:
        True, если число вероятно простое
        False, если число составное
        None, если число недопустимо для теста
    """
    if n < 5:
        print("Это значение не допустимо.")
        return None

    for i in range(num_tests):
        a = random.randint(2, n - 2)
        print("=" * 30)
        print(f"Попытка {i + 1}: a = {a}")
        
        if not Miller_Rubbin(n, a):
            print(f"Число {n} не прошло тест Миллера – Рабина при a = {a}")
            print(f"Число {n} составное.")
            return False
        
        print(f"Число {n} прошло тест Миллера – Рабина при a = {a}")
        print("=" * 30)

    print(f"Число {n} вероятно простое.")
    return True


def main() -> None:
    """Основная функция программы для проверки чисел на простоту."""
    while True:
        try:
            n = int(input("Введите число для проверки на простоту: "))
            miller_rabin_test(n)
        except ValueError:
            print("Ошибка: введите целое число")
        except KeyboardInterrupt:
            print("\nПрограмма завершена.")
            break


if __name__ == "__main__":
    main()
