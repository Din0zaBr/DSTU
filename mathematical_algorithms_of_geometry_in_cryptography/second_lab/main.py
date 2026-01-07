import math
from typing import Optional


def pollard_rho(
    n: int,
    c: int,
    f: str,
    max_iterations: int = 1000
) -> Optional[int]:
    """
    Находит нетривиальный делитель числа n с помощью ρ-метода Полларда.
    
    Args:
        n: Число для факторизации
        c: Начальное значение (константа)
        f: Функция f(x) в виде строки (например, 'x**2 + 1')
        max_iterations: Максимальное количество итераций
    
    Returns:
        Нетривиальный делитель числа n или None, если не найден
    """
    # Проверка на четность
    if n % 2 == 0:
        print(f"Число {n} четное. Нетривиальный делитель: 2")
        return 2
    
    # Функция для вычисления f(x) mod n
    def g(x: int) -> int:
        """Вычисляет f(x) mod n из строкового представления."""
        return eval(f, {'x': x, 'math': math}) % n
    
    print(f"Начальные значения: c = {c}, f(x) = {f}, n = {n}")
    print("=" * 50)
    
    # Инициализация: x = y = c
    x = c
    y = c
    d = 1
    iteration = 1
    
    # Основной цикл алгоритма
    while d == 1 and iteration <= max_iterations:
        print(f"Итерация {iteration}:")
        print(f"  a = {x}, b = {y}")
        
        # Шаг 1: x = f(x) mod n
        x = g(x)
        # Шаг 2: y = f(f(y)) mod n (двигаемся в 2 раза быстрее)
        y = g(g(y))
        
        print(f"  После применения f(x):")
        print(f"    a = f(a) (mod n) = {x}")
        print(f"    b = f(f(b)) (mod n) = {y}")
        
        # Шаг 3: Вычисляем НОД(|x - y|, n)
        d = math.gcd(abs(x - y), n)
        print(f"  d = НОД(|a - b|, n) = НОД({abs(x - y)}, {n}) = {d}")
        
        # Проверка результата
        if 1 < d < n:
            print(f"  Найден нетривиальный делитель (1 < d < n): {d}")
            print("=" * 50)
            return d
        elif d == n:
            print(f"  d = n. Метод не сработал для данных параметров.")
            print("=" * 50)
            return None
        else:
            print(f"  d = 1 => Продолжаем итерации")
            print("=" * 50)
            iteration += 1
    
    # Достигнуто максимальное количество итераций
    print(f"Достигнуто максимальное количество итераций ({max_iterations})")
    return None


def validate_function(f_str: str) -> bool:
    """
    Проверяет корректность строкового представления функции.
    
    Args:
        f_str: Строка с функцией
    
    Returns:
        True, если функция корректна, False иначе
    """
    try:
        test_x = 2
        eval(f_str, {'x': test_x, 'math': math})
        return True
    except Exception:
        return False


def main() -> None:
    """Основная функция программы для факторизации числа ρ-методом Полларда."""
    print("=" * 50)
    print("ρ-метод Полларда для поиска нетривиального делителя")
    print("=" * 50)
    
    try:
        # Ввод данных
        n = int(input("Введите число n: "))
        if n < 2:
            print("Ошибка: n должно быть больше 1")
            return
        
        c = int(input("Введите начальное значение c: "))
        
        print("\nВведите функцию f(x) (например, 'x**2 + 1' или 'x*x + 1'):")
        print("Доступные операции: +, -, *, **, //, %, math.*")
        f_str = input("f(x) = ")
        
        # Валидация функции
        if not validate_function(f_str):
            print("Ошибка: введено некорректное уравнение для f(x).")
            print("Примеры корректных функций: 'x**2 + 1', 'x*x - 20', 'x**2 + x + 1'")
            return
        
        # Выполнение алгоритма
        divisor = pollard_rho(n, c, f_str)
        
        # Вывод результата
        print("\n" + "=" * 50)
        if divisor:
            print(f"ОТВЕТ: Нетривиальный делитель числа {n}: {divisor}")
            print(f"Проверка: {n} = {divisor} * {n // divisor}")
        else:
            print(f"ОТВЕТ: Нетривиальный делитель числа {n} не найден.")
            print("Попробуйте изменить параметры c или f(x).")
        print("=" * 50)
        
    except ValueError:
        print("Ошибка: введите корректные целые числа для n и c.")
    except KeyboardInterrupt:
        print("\n\nПрограмма завершена пользователем.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
