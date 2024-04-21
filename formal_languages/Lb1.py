import re
from PySimpleGUI import *


def examination(textl, textr):
    """
    Проверяет тип грамматики на основе данного ввода.

    Параметры:
        textl (str): Левая текстовая строка для проверки.
        textr (str): Правая текстовая строка для проверки.

    Возвращает:
        str: Тип грамматики на основе входных данных. Возможные значения:
            - 'Тип 3': Если textl соответствует шаблону pattern1 и pattern2.
            - 'Тип 2': Если textl соответствует шаблону pattern1, но не соответствует pattern2.
            - 'Тип 1': Если textl не соответствует шаблону pattern1 и длина textr равна длине textl.
            - 'Тип 0': Если ни одно из вышеуказанных условий не выполняется.
    """
    pattern1 = r'^[A-Z]$'  # Паттерн для одной заглавной буквы
    pattern2 = r'^[a-z][A-Z]$|^[A-Z][a-z]$'
    # Паттерн для двух букв, одна из которых - нижняя заглавная, а другая - верхняя заглавная, или наоборот

    test1 = re.match(pattern1, textl)
    test2 = re.match(pattern2, textl)
    test3 = len(textr) == len(textl)

    if test1 and test2:
        return 'Type 3'
    elif test1 and not test2:
        return 'Type 2'
    elif not test1 and test3:
        return 'Type 1'
    else:
        return 'Type 0'


def defense1(text):
    """
    Проверяет, является ли переданный текст допустимым положительным целым числом.

    Параметры:
        text (str): Текст для проверки.

    Возвращает:
        bool: True, если текст является допустимым положительным целым числом, False в противном случае.
    """
    pattern = r'^\d+$'

    text = re.match(pattern, text)

    if not text:
        return False

    return True


def defense2(array):  # Проверка на корректность ввода
    """
    Проверка корректности ввода массива.

    Параметры: array (список): Список кортежей, каждый из которых содержит два элемента. Каждый элемент представляет
    собой строку, которая будет проверена на соответствие регулярному выражению.

    Возвращает:
        bool: True, если все элементы в массиве проходят тест регулярного выражения, False в противном случае.
    """
    pattern = r'^[A-Za-z]|\s+$'
    flag = True

    for element in array:
        test1 = re.match(pattern, element[0])
        test2 = re.match(pattern, element[1])

        if bool(test1) == False or bool(test2) == False:
            flag = False
            break
    if flag:
        return True
    else:
        return False


def interface1():
    """
    Функция, предоставляющая интерфейс для ввода количества правил и корректной длины.

    Параметры:
    None

    Возвращает:
    int: Количество правил, введенное пользователем, если ввод является корректным.
    """
    flag = True
    while True:
        if flag:
            layout = [[Text('Введите количество правил: '), Input()],
                      [Button('Далее'), Button('Выход')]]
        else:
            layout = [[Text('Введите количество правил: '), Input()],
                      [Text('Введите корректную длину')],
                      [Button('Далее'), Button('Выход')]]

        window = Window('Лабораторная работа №1', layout)
        event, values = window.read()

        if event in (WIN_CLOSED, 'Выход'):
            exit()
        window.close()

        if event == 'Далее':
            if not defense1(str(values[0])) or int(values[0]) <= 0:
                flag = False
                continue
            else:
                return int(values[0])


def interface2(rule_number):
    """
    Функция `interface2` предоставляет графический интерфейс для ввода правил пользователем.
    Она принимает параметр `rule_number`, который указывает количество правил для ввода.

    Параметры:
    - rule_number (int): Количество правил для ввода.

    Возвращает:
    - list: Список правил, введенных пользователем. Каждое правило представлено списком из двух элементов.
            Первый элемент является вводом для первой части правила, а второй элемент - для второй части правила.
            Если пользователь вводит некорректные правила, функция возвращает `None`.

    Эта функция отображает окно с полями ввода для правил. Количество полей ввода зависит от параметра `rule_number`.
    Пользователь может вводить правила, заполняя значениями полей ввода. После того как пользователь ввел правила,
    он может нажать кнопку "Далее", чтобы продолжить. Если введенные правила являются некорректными,
    функция отображает дополнительное поле ввода, предлагая пользователю ввести правильные правила.
    """
    flag = True
    while True:
        if flag:
            layout = [[Input(), Text('->'), Input()] for _ in range(0, rule_number * 2, 2)]
            layout.insert(0, [Text('Введите правила')])
            layout += [[Button('Далее'), Button('Выход')]]
        else:
            layout = [[Input(), Text('->'), Input()] for _ in range(0, rule_number * 2, 2)]
            layout.insert(0, [Text('Введите правила')])
            layout.insert(2, [Text('Введите корректные правила')])
            layout += [[Button('Далее'), Button('Выход')]]

        window = Window('Лабораторная работа №1', layout)
        event, values = window.read()

        if event in (WIN_CLOSED, 'Выход'):
            exit()
        window.close()

        if event == 'Далее':
            temp = []

            for i in range(0, len(values), 2):
                temp.append([values[i], values[i + 1]])

            if defense2(temp):
                return temp
            else:
                flag = False


def verification(array):
    """
    Проверяет тип грамматики на основе входного массива.

    Параметры: array (list): Список кортежей, каждый содержит два элемента. Каждый элемент представляет собой строку,
    которая будет проверена на соответствие регулярному выражению.

    Возвращает:
        str: Тип грамматики на основе входных данных. Возможные значения:
            - 'Тип 3': Если array[i][0] совпадает с pattern1 и pattern2.
            - 'Тип 2': Если array[i][0] совпадает с pattern1, но не совпадает с pattern2.
            - 'Тип 1': Если array[i][0] не совпадает с pattern1, но длина array[i][1] равна длине array[i][0].
            - 'Тип 0': Если не выполняется ни одно из вышеперечисленных условий.
    """
    temp_gram = []

    for i in range(len(array)):
        temp_gram.append(examination(array[i][0], array[i][1]))

    for i in range(4, 0, -1):
        if temp_gram.count(f'Тип {i}') == 0:
            continue
        else:
            return f'Тип {i}'


def replace_elements_in_string(s, replacements):
    """
    Заменяет элементы в строке на основе списка замен.

    Параметры:
        s (str): Входная строка.
        replacements (list): Список кортежей, содержащих элементы для замены и их замены.

    Возвращает:
        str: Модифицированная строка с примененными заменами.
    """
    temp = []
    for old, new in replacements:
        temp.append(s.count(old))

    for i in range(len(replacements)):
        old = replacements[i][0]
        new = replacements[i][1]
        if temp[i] > 0:
            for _ in range(temp[i]):
                s = s.replace(old, new)
    s = s.replace(' ', '')
    return s


def interface3(array):
    """
    Функция `interface3` принимает массив в качестве входных данных и выполняет серию операций для определения типа
    грамматики и генерации цепочки строк.

    Параметры: - array (list): Список кортежей, представляющих правила входных данных. Каждый кортеж содержит две
    строки, представляющие первый и второй части правила.

    Возвращает:
    - None

    Функция сначала вызывает функцию `verification`, чтобы определить тип грамматики на основе входного массива.
    Затем она инициализирует строку `Str` со значением 'S' и строку `output` со значением 'S -> '.

    Функция вводит цикл while и повторно заменяет элементы в строке `Str` с помощью функции `replace_elements_in_string`
    и входного массива. Она отслеживает количество итераций в переменной `count`.

    Если переменная `count` равна 3, функция создает пустой массив `temp_array` и фильтрует элементы из входного
    массива, которые не присутствуют в `temp_array`. Затем она добавляет элементы из входного массива в `temp_array`,
    если второй элемент кортежа является пустой строкой.

    Функция добавляет измененную строку `Str` в строку `output` и вводит другой цикл while. В этом цикле она повторно
    заменяет элементы в строке `Str` с помощью функции `replace_elements_in_string` и массива `temp_array`. Если в
    строке `Str` нет ни одного символа в верхнем регистре, она добавляет измененную строку `Str` в строку `output` и
    выходит из цикла.

    Если в строке `Str` есть символы в верхнем регистре, функция заменяет элементы в строке `Str` с помощью функции
    `replace_elements_in_string` и массива `res`. Затем она добавляет измененную строку `Str` в строку `output`.

    После выхода из внутреннего цикла while функция выходит из внешнего цикла while.
    """
    typ = verification(array)
    Str = 'S'
    output = 'S -> '
    count = 0
    while True:
        Str = replace_elements_in_string(Str, array)
        if count == 3:
            temp_array = []
            res = [item for item in array if item not in temp_array]

            for i in range(len(array)):
                if array[i][1] == ' ':
                    temp_array.append(array[i])

            output += Str + ' -> '

            while True:
                Str = replace_elements_in_string(Str, temp_array)

                if not any(c.isupper() for c in Str):
                    output += Str
                    break

                Str = replace_elements_in_string(Str, res)
                output += Str

            break
        else:
            output += Str + ' -> '
            count += 1

    while True:
        layout = [
            [Text(f'Тип грамматики: {typ}')],
            [Text(f'Цепочка: {output}')],
            [Button('Выход')]]

        window = Window('Лабораторная работа №1', layout)
        event, values = window.read()

        if event in (WIN_CLOSED, 'Выход'):
            exit()
        window.close()


def main():
    while True:
        count_rule = interface1()
        array = interface2(count_rule)
        interface3(array)


main()
