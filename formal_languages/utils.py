def is_rrg(rules: list[tuple[str, str]], terms: list[str], non_terms: list[str]) -> bool:
    """
    Проверяет, является ли грамматика праволинейной.

    :param rules: Список правил грамматики, где каждое правило представлено в виде кортежа (левая часть, правая часть).
    :param terms: Список терминальных символов.
    :param non_terms: Список нетерминальных символов.
    :return: True, если грамматика является праволинейной, иначе False.
    """
    for rule in rules:
        left, right = rule

        # Проверяем, что левая часть правила состоит из одного нетерминального символа.
        if not (len(left) == 1 and left in non_terms):
            return False

        # Если правая часть правила равна "eps", пропускаем это правило.
        if right == "eps":
            continue

        # Проверяем, что все символы в правой части, кроме последнего, являются терминальными.
        for el in right[:-1]:
            if el not in terms:
                return False

    return True


def is_lrg(rules: list[tuple[str, str]], terms: list[str], non_terms: list[str]) -> bool:
    """
    Проверяет, является ли грамматика леволинейной.

    :param rules: Список правил грамматики, где каждое правило представлено в виде кортежа (левая часть, правая часть).
    :param terms: Список терминальных символов.
    :param non_terms: Список нетерминальных символов.
    :return: True, если грамматика является леволинейной, иначе False.
    """
    for rule in rules:
        left, right = rule

        # Проверяем, что левая часть правила состоит из одного нетерминального символа.
        if not (len(left) == 1 and left in non_terms):
            return False

        # Если правая часть правила равна "eps", пропускаем это правило.
        if right == "eps":
            continue

        # Проверяем, что все символы в правой части, кроме первого, являются терминальными.
        for el in right[1:]:
            if el not in terms:
                return False

    return True


def is_cfg(rules: list[tuple[str, str]], non_terms: list[str]) -> bool:
    """
    Проверяет, является ли грамматика контекстно-свободной.

    :param rules: Список правил грамматики, где каждое правило представлено в виде кортежа (левая часть, правая часть).
    :param non_terms: Список нетерминальных символов.
    :return: True, если грамматика является контекстно-свободной, иначе False.
    """
    for rule in rules:
        left, right = rule

        # Проверяем, что левая часть правила состоит из одного нетерминального символа.
        if not (len(left) == 1 and left in non_terms):
            return False

        # Если правая часть правила равна "eps", пропускаем это правило.
        if right == "eps":
            continue

    return True


def is_csg(rules: list[tuple[str, str]], non_terms: list[str], start_symbol: str) -> bool:
    """
    Проверяет, является ли грамматика контекстно-зависимой.

    :param rules: Список правил грамматики, где каждое правило представлено в виде кортежа (левая часть, правая часть).
    :param non_terms: Список нетерминальных символов.
    :param start_symbol: Стартовый символ грамматики.
    :return: True, если грамматика является контекстно-зависимой, иначе False.
    """
    flag = False

    for rule in rules:
        left, right = rule

        # Проверяем, что левая часть правила состоит из одного нетерминального символа.
        if len(left) == 1:
            if right == "eps":
                if left != start_symbol and flag:
                    return False
                else:
                    flag = True

        if start_symbol in right:
            if flag:
                return False
            else:
                flag = True

        # Проверяем, что левая часть правила содержит хотя бы один нетерминальный символ.
        is_left_ok = False
        for el in non_terms:
            if el in left:
                is_left_ok = True
                break

        if not is_left_ok:
            return False

        # Проверяем, что правая часть правила не равна "eps".
        is_right_ok = False
        if right != "eps":
            is_right_ok = True

        if not is_right_ok:
            return False

        """
        Далее идёт фрагмент кода, который используется для проверки, что правая часть правила грамматики содержит 
        дополнительные символы, которые не соответствуют нетерминальным символам в левой части правила, что является 
        характерной особенностью контекстно-зависимых грамматик
        """

        # Инициализация переменной gamma значением None. Это делается для того, чтобы позже можно было проверить,
        # была ли найдена подходящая часть правой части правила.
        gamma = None

        # Перебор каждого символа в левой части правила с индексом.
        for index, el in enumerate(left):
            # Если текущий символ не является нетерминальным (т.е. не присутствует в списке нетерминальных символов),
            # то переходим к следующему символу без выполнения остального кода внутри цикла.
            if el not in non_terms:
                continue

            # Разделение левой части правила на две части: xi_1 (все символы до текущего) и xi_2 (все символы после
            # текущего).
            xi_1 = left[:index]
            xi_2 = left[index + 1:]

            # Проверка, начинается ли правая часть правила с xi_1 и заканчивается ли она на xi_2.
            if right.startswith(xi_1) and right.endswith(xi_2):
                # Если условие выполняется, то вычисляем gamma как часть правой части правила, которая находится
                # между xi_1 и xi_2.
                gamma = right.replace(xi_1, "").replace(xi_2, "")
                # Если gamma пустая строка (что означает, что правая часть правила полностью соответствует xi_1 и xi_2),
                # то переходим к следующему символу в левой части правила.
                if not gamma:
                    continue

        # Если после перебора всех символов в левой части правила переменная gamma остается None (то есть подходящая
        # часть правой части правила не была найдена), функция возвращает False, указывая на то, что грамматика не
        # соответствует классу контекстно-зависимых грамматик.
        if not gamma:
            return False

    return True


def is_ng(rules: list[tuple[str, str]], start_symbol: str) -> bool:
    """
    Проверяет, является ли грамматика неукорачивающей.

    :param rules: Список правил грамматики, где каждое правило представлено в виде кортежа (левая часть, правая часть).
    :param start_symbol: Стартовый символ грамматики.
    :return: True, если грамматика является неукорачивающей, иначе False.
    """
    flag = False

    for rule in rules:
        left, right = rule

        # Проверяем, что левая часть правила состоит из одного нетерминального символа.
        if len(left) == 1:
            if right == "eps":
                if left != start_symbol and flag:
                    return False
                else:
                    flag = True

        if start_symbol in right:
            if flag:
                return False
            else:
                flag = True

        # Проверяем, что длина левой части правила не больше длины правой части.
        if len(left) > len(right):
            return False

    return True
