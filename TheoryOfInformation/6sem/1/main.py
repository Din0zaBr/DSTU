import PySimpleGUI as sg
import re


def is_prime(num):
    if num % 2 == 0:
        return num == 2
    d = 3
    while d * d <= num and num % d != 0:
        d += 2
    return d * d > num


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
    # Заменяем возведение в степень на умножение
    expression = re.sub(r'(\d+)\^(\d+)', lambda m: '*'.join([m.group(1)] * int(m.group(2))), expression)

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

window = sg.Window('Калькулятор выражений в полях', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Вычислить':
        calculate(window, values)

window.close()
