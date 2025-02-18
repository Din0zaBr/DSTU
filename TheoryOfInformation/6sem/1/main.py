import PySimpleGUI as sg
import re


def is_prime(num):
    """
    Сразу фильтрует чётные числа (кроме 2)
    Проверяет только нечётные делители
    Останавливается при достижении квадратного корня из числа
    :param num:
    :return:
    """
    if num % 2 == 0:  # Проверяем, является ли число чётным
        return num == 2  # Если да, то оно простое только если равно 2
    d = 3  # Начинаем проверку с 3
    while d * d <= num and num % d != 0:  # Проверяем нечётные делители + : 3
        d += 2  # Переходим к следующему нечётному числу
    return d * d > num  # Если не нашли делитель, число простое


def extended_gcd(a, b):
    """Расширенный алгоритм Евклида для нахождения обратного элемента."""
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x


def mod_inverse(a, mod):
    """Нахождение мультипликативного обратного элемента в поле."""
    g, x, _ = extended_gcd(a, mod)
    if g != 1:
        raise ValueError(f"Обратный элемент для {a} по модулю {mod} не существует.")
    else:
        return x % mod


def evaluate_expression(expression, mod):
    """Вычисление выражения в поле."""
    # (\d+) - первая группа: число перед символом возведения в степень
    # (\d+) - вторая группа: показатель степени
    # m.group(1) получает основание
    # [m.group(1)] * int(m.group(2)) создаёт список повторений числа
    # '*'.join(...) объединяет их операторами умножения
    # Пример: 2^3 → 2*2*2

    # Заменяем возведение в степень на умножение
    expression = re.sub(r'(\d+)\^(\d+)', lambda m: '*'.join([m.group(1)] * int(m.group(2))), expression)

    # (\d+) - первая группа: делимое
    # (\d+) - вторая группа: делитель
    # Лямбда-функция:
    # m.group(1) получает делимое
    # mod_inverse(int(m.group(2)), mod) вычисляет модульную обратную величину делителя
    # Результат объединяется оператором умножения
    # Пример: 6/2 → 6*3 (если mod=7, так как 2*3 ≡ 1 (mod 7))

    # Заменяем деление на умножение на обратный элемент
    expression = re.sub(r'(\d+)\/(\d+)', lambda m: f"{m.group(1)}*{mod_inverse(int(m.group(2)), mod)}", expression)

    # Вычисляем выражение с учетом модуля
    return eval(expression) % mod


def calculate(window, values):
    """Функция для обработки ввода и вычисления результата."""
    expression = values['expression']
    mod_str = values['mod']

    if not expression or not mod_str:
        sg.popup_error("Пожалуйста, введите выражение и модуль.")
        return

    try:
        mod = int(mod_str)
        if mod <= 0:
            sg.popup_error("Модуль должен быть положительным числом.")
            return
        if not is_prime(mod):
            sg.popup_error("Модуль должен быть простым числом.")
            return

        # Убираем возможные пробелы в выражении
        expression = expression.replace(" ", "")

        # Проверяем, есть ли в выражении модуль (modX)
        if re.search(r'\(mod\d+\)', expression):
            sg.popup_error("Модуль указывается в отдельном поле.")
            return

        result = evaluate_expression(expression, mod)
        window['result'].update(f"Результат: {result} (mod{mod})")
    except ValueError as e:
        sg.popup_error(str(e))
    except Exception as e:
        sg.popup_error(f"Ошибка при вычислении выражения: {e}")


layout = [
    [sg.Text('Введите выражение:')],
    [sg.Input(key='expression')],
    [sg.Text('Введите поле:')],
    [sg.Input(key='mod')],
    [sg.Button('Вычислить')],
    [sg.Text('', key='result')]
]

window = sg.Window('ТИ 1Л 6С', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Вычислить':
        calculate(window, values)

window.close()
