from itertools import chain

massT = str(input("Множество терминалов: ")).split()  # massT - всё кроме строчных латинских (a,b,c,12,1,-,$,|
massN = str(input("Множество нетерминалов: ")).split()  # massN - прописные латинские (A,B,C)
S = str(input("Введите стартовый символ: "))
n = int(input("Количество правил: "))
print("Введите правила по типу: Aa = Rpppp\n"
      "Если из левой части есть несколько переходов, пропишите их через пробел слева\n"
      "В качестве пустой цепочки выступает точка (.)\n")


def check_KS():
    """
        Предлагает пользователю ввести последовательность строк, представляющих контекстно-свободную грамматику.
        Анализирует каждую введенную строку и сохраняет разобранное представление в списке списков под названием `rooles`.
        Проверяет, присутствуют ли все символы в первой строке каждого ввода в заранее определенном списке под названием `massN`.
        Если какие-либо символы отсутствуют, увеличивает счетчик под названием `count`.
        Если `count` равно нулю, устанавливает строку результата равной "Введена КС-грамматика" и устанавливает флаг в 1.
        В противном случае устанавливает строку результата равной "Введенная грамматика не является КС-грамматикой" и устанавливает флаг в 0.
        Возвращает кортеж, содержащий строку результата, флаг и список `rooles`.
    """
    count = 0
    rules = []
    pravila = input().split(", ")
    for pravilo in pravila:
        current_rule = str(pravilo).split()
        a = current_rule[0]  # roole_n = ['S', '=', 'X|Y|Z'] -> 'S'
        b = current_rule[2]  # roole_n = ['S', '=', 'X|Y|Z'] -> 'X|Y|Z'
        rules.append([a, b])  # [['S', ['X|Y|Z']]]
        if a not in massN:  # Проверка, что слева д/б только терминалы
            count += 1
    if count == 0:
        rez, flag = 'Введена КС-грамматика', True
    else:
        rez, flag = "Введенная грамматика не является КС-грамматикой", False
    return rez, rules, flag


def check_gramm(rooles, massN,
                S):  # проверка существования языка путём проверки находится ли S в множетсве нетерминалов используемых в правилах
    N0 = []
    temp_rooles_mass_T = set()
    for i in range(len(rooles)):
        for j in chain(rooles[i][1], rooles[i][0]):
            [N0.append(x) for x in list(j) if x in massN and x not in N0]
            for term_str in rooles[i][1].split("|"):
                for term in term_str:
                    temp_rooles_mass_T.add(term)

    temp_rooles_mass_T = list(temp_rooles_mass_T)

    if S not in N0:
        return 'Язык не существует', N0, temp_rooles_mass_T
    else:
        return "Язык существует", N0, temp_rooles_mass_T


def del_useless_sym(massT, massN, lst):
    print('a) бесполезных символов')

    def cycle_el(mass):
        mass_el_mass = massT + mass
        for i in range(len(lst)):
            for x in lst[i][1]:
                if set(list(x)).issubset(mass_el_mass):
                    if lst[i][0] not in mass:
                        mass.append(lst[i][0])
        return mass

    mass = ['.']
    N1 = cycle_el(mass)
    Ni = cycle_el(N1.copy())
    while N1 != Ni:
        N1 = Ni
        Ni = cycle_el(N1.copy())
    N = [element for element in massN if element not in Ni]  # Бесполезные символы
    if len(N) != 0:
        r = []  # Будущие новые правила
        for i in range(len(lst)):
            r0 = []
            for j in lst[i][1]:
                v = []
                [v.append(x) for x in list(j) if x in Ni or x in massT or x == '.']
                if ''.join(v) == j:
                    r0.append(j)
            if len(r0) != 0:
                r.append([lst[i][0], r0])
    else:
        r = lst
    Ni.remove('.')
    return Ni, r


def no_way_sym(lst):
    """
       Находит недостижимые символы в заданном списке правил.

       Параметры:
       - lst (list): Список правил, где каждое правило представляет собой кортеж, содержащий символ и список символов.

       Возвращает:
       - T (list): Список символов, которые достижимы из начального символа.
       - Ni (list): Список символов, которые недостижимы.
       - r (list): Список правил, где каждое правило представляет собой кортеж, содержащий символ и список символов.

       Функция принимает список правил, где каждое правило представляет собой кортеж, содержащий символ и список символов.
       Она находит символы, не достижимые из начального символа, выполняя алгоритм обнаружения циклов. Затем определяет
       достижимые символы и возвращает их вместе с недостижимыми символами и правилами, содержащими недостижимые символы.

       Пример:
        lst = [('S', [('A', 'B'), ('C', 'D')]), ('A', [('A', 'A'), ('B', 'B')]), ('B', [('C', 'C'), ('D', 'D')]), ('C', [('A', 'A'), ('B', 'B')]), ('D', [('C', 'C'), ('D', 'D')])]
        no_way_sym(lst)
       (['A', 'C'], ['B', 'D'], [('A', [('A', 'A'), ('B', 'B')]), ('C', [('A', 'A'), ('B', 'B')])])
    """

    print('б) недостижимых символов')

    # просматриваем каждое правильно по отдельности, заносим каждый этот символ в список, вне зависимости терминал это или нет
    # если левая часть данного правила уже имеется в нашем списке, то добавляем правую частьного правила в этот список
    # если нет, то пропускаем это правило, правило со стартовым символом вносим обязательно

    def cycle_el(mass):
        for i in range(len(lst)):
            if lst[i][0] in mass:
                [mass.append(x) for j in lst[i][1] for x in list(j) if x in massN and x not in mass]
        return mass

    mass = [lst[0][0]]
    N1 = cycle_el(mass)
    Ni = cycle_el(N1.copy())
    while N1 != Ni:
        N1 = Ni
        Ni = cycle_el(N1.copy())
    N = [element for element in massN if element not in Ni]  # Бесполезные символы
    if len(N) != 0:
        r = []  # Будущие новые правила
        for i in range(len(lst)):
            if lst[i][0] in Ni:
                r.append(lst[i])
    else:
        r = lst
    T = []
    for i in range(len(r)):
        [T.append(x) for j in lst[i][1] for x in list(j) if x in massT and x not in T]
    return T, Ni, r


def del_eps_rooles(massN, rooles, S):
    print('в) е-правил')
    # создание новых временных нетерминалов (Заглавные)
    new_massN = massN
    new_S = S

    N = [left_side for left_side, right_side in rooles if
         "." in right_side]  # Находим все нетерминалы порождающие пустые правила

    # Мы смотрим каждое правило и если в нем есть нетерминал, порождающий пустую строку, то
    # добавляем этот нетерминал в список N, потому что таков алгоритм
    for current_rool in rooles:
        if current_rool[0] in N:
            continue

        flage = 0
        right_side = current_rool[1].split("|")  # Рассматриваем каждую часть правила

        for i in right_side:  # Перебираем все части и если там есть терминал
            if flage == 1:
                break
            for n in N:
                if flage == 1:
                    break
                if n in i:
                    N.append(current_rool[0])
                    flage = 1

    # Этот цикл выполняет шаг №2, №3 в алгоритме.
    # Удаление из грамматики пустых строк + дополнение терминалы
    for current_rool in rooles:
        if current_rool[0] in N:
            temp_array = current_rool[1].split("|")  # Костыль, так как там через 1 E строка
            new_right_side = []

            for i in temp_array:
                if i != '.':
                    new_right_side.append(i)
                    temp_i = i.replace(current_rool[0],
                                       '')  # Шаг 3, рассматриваем правила, удаляем E, добавляем конечный терминал,
                    # чтобы не было замкнутости
                    if temp_i not in new_right_side: # Чтобы не было дубликатов правил (# Если нет цикличности, то будем порождать циклично терминалы и одновременно,
                        new_right_side.append(temp_i) # temp_i - цепочка правил без E

            current_rool[1] = "|".join(new_right_side) # обратное преобразование в норм правило

    if S in N: # Шаг №4
        upper_latin = [chr(i) for i in range(65, 91)]

        for non_terminal_symbol in upper_latin:
            if non_terminal_symbol not in massN:
                new_S = non_terminal_symbol
                rooles.insert(0, [new_S, f"{S}|."])
                new_massN.extend([new_S])
                break

    return new_massN, rooles, new_S # Возвращаем новое мн нетерминалов, новые правила и новый стартовый символ
# S может быть изменён, так как если он находится в N, то он долже быть заменён, исходя их логики шага № 4
    pass


def zip_rooles(massN, lst):
    """
        Функция для генерации списка правил без правил-epsilon.

        Параметры:
        massN (list): Список терминалов.
        lst (list): Список правил, где каждое правило представлено кортежем, где первый элемент - нетерминал, а второй элемент - список терминалов/нетерминалов.

        Возвращает:
        list: Список правил без правил-epsilon.
    """

    print('г) цепных правил')

    def cycle_el(mass):
        for i in range(len(lst)):
            if lst[i][0] in mass:
                [mass.append(j) for j in lst[i][1] if j in massN and j not in mass]
        return mass

    # Формируем общий список Ni для каждого нетерминала
    mass_Ni = []
    for i in range(len(lst)):
        mass = [lst[i][0]]
        N1 = cycle_el(mass)
        Ni = cycle_el(N1.copy())
        while N1 != Ni:
            N1 = Ni
            Ni = cycle_el(N1.copy())
        mass_Ni.append([lst[i][0], Ni.copy()])
    # Формируем новый список правил без цепных правил
    r = []
    for i in range(len(mass_Ni)):
        r0 = []
        for j in range(len(lst)):
            if lst[j][0] in mass_Ni[i][1]:
                r01 = [el for el in lst[j][1] if el not in massN]
                r0.extend(r01)
        r.append([mass_Ni[i][0], r0])
    return r


def left_factorize(rooles):
    new_rooles = []

    for current_rooles in rooles:
        array_right_side = current_rooles[1].split("|")
        unique_characters = set()
        temp_str = set(current_rooles[1].replace("|", ""))
        print(array_right_side, temp_str, sep='\n')

    pass


def remove_left_recursion(grammar):
    print('е) левой рекурсии')
    new_grammar = {}
    non_terminals = list(grammar.keys())

    for A in non_terminals:
        A_rules = grammar[A]
        alpha_rules = [rule for rule in A_rules if rule.startswith(A)]
        beta_rules = [rule for rule in A_rules if not rule.startswith(A)]

        if not alpha_rules:
            new_grammar[A] = A_rules
            continue

        A_prime = A + "'"
        new_rules_A = []
        new_rules_A_prime = []

        for beta_rule in beta_rules:
            new_rule = beta_rule + A_prime
            new_rules_A.append(new_rule)

        for alpha_rule in alpha_rules:
            new_rule = alpha_rule[len(A):] + A_prime
            new_rules_A_prime.append(new_rule)

        new_rules_A_prime.append('.')  # точка (.) представляет собой пустую цепочку

        new_grammar[A] = new_rules_A
        new_grammar[A_prime] = new_rules_A_prime

    return new_grammar


rez, rooles, flag = check_KS()
print('1)', rez)
if flag == True:
    rez, N, temp_massT = check_gramm(rooles, massN, S)
    print('2)', rez)

print('Исходная грамматика:')
print('G = (', massN, ',', massT, ', P,', S, ')')
print("\n".join(f"{i[0]} -> {' '.join(i[1])}" for i in rooles))

print('Эквивалентное преобразование грамматики посредством удаления:')

massN1, rooles1 = del_useless_sym(massT, massN, rooles)
print('G = (', massT, ',', massN1, ', P,', S, ')')
print("\n".join(f"{i[0]} -> {' '.join(i[1])}" for i in rooles1))

massT1, massN1, rooles1 = no_way_sym(rooles)
print('G = (', massT1, ',', massN1, ', P,', S, ')')
print("\n".join(f"{i[0]} -> {' '.join(i[1])}" for i in rooles1))

massN1, rooles1, S_new = del_eps_rooles(massN, rooles, S)
print('G = (', massT, ',', massN1, ', P,', S_new, ')')
print("\n".join(f"{i[0]} -> {' '.join(i[1])}" for i in rooles1))

rooles1 = zip_rooles(massN1, rooles1)
print('G = (', massT, ',', massN1, ', P,', S_new, ')')
print("\n".join(f"{i[0]} -> {' '.join(i[1])}" for i in rooles1))

rooles1 = left_factorize(rooles)
print(type(rooles1))
print("\n".join(f"{key} -> {value}" for key, value in rooles1.items()))

grammar = {item[0]: item[1] for item in rooles}
new_grammar = remove_left_recursion(grammar)
new_grammar = {key: value for key, value in new_grammar.items()}
print("\n".join(f"{key} -> {value}".rstrip("|") for key, value in new_grammar.items()))

# a b l = < > ^ v ~
# X Y Z K L
# X
# X = Y|Y=Y|Y<Y|Y>Y|K, Y = Y^Z|YvZ|., Z = ~a|~b|., K = ~K, L = l|a|b
