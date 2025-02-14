# def is_prime(num):
#     if num % 2 == 0:
#         return num == 2
#     d = 3
#     while d * d <= num and num % d != 0:
#         d += 2
#     return d * d > num
#
#
# p = int(input("Введите простое число: e = "))  # Пример: 65537
# while not is_prime(e):
#     print(f"Число {e} не простое")
#     e = int(input("Введите простое число: e = "))

import PySimpleGUI as sg


def is_prime(n):
    """Проверка числа на простоту."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def mod_inverse(a, p):
    """Вычисление мультипликативной инверсии по модулю p."""
    if a > 0:
        return a % p
    elif a < 0 and abs(a) <= p:
        return p + a
    else:
        test = abs(a) // p
        return a + p * test


def evaluate_expression(expression, p):
    try:
        # Заменяем дроби на умножение с использованием мультипликативной инверсии
        expression = expression.replace('/', '!')
        print(expression)

        # Вычисляем выражение в конечном поле
        result = eval(expression)
        print(result)
        mod_inverse(result, p)
        return result
    except Exception as e:
        return str(e)


def main():
    sg.theme('LightBlue')

    layout = [
        [sg.Text('Введите простое целое число p:')],
        [sg.InputText(key='-P-')],
        [sg.Text('Введите выражение:')],
        [sg.InputText(key='-EXPRESSION-')],
        [sg.Button('Вычислить'), sg.Button('Выход')],
        [sg.Text('', size=(40, 1), key='-OUTPUT-')]
    ]

    window = sg.Window('Конечное поле', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Выход':
            break
        if event == 'Вычислить':
            p = int(values['-P-'])
            expression = values['-EXPRESSION-']

            if not is_prime(p):
                window['-OUTPUT-'].update(f'{p} не является простым числом.')
            else:
                result = evaluate_expression(expression, p)
                window['-OUTPUT-'].update(f'Результат: {result}')

    window.close()


if __name__ == '__main__':
    main()
