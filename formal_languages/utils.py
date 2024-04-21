def is_rrg(rules: list[tuple[str, str]], terms: list[str], non_terms: list[str]) -> bool:
    """
    Класс 3: Праволинейная грамматика

    :param non_terms:
    :param terms:
    :param rules:
    :return:
    """
    for rule in rules:
        left, right = rule

        if not (len(left) == 1 and left in non_terms):
            return False

        if right == "eps":
            continue

        for el in right[:-1]:
            if el not in terms:
                return False

    return True


def is_lrg(rules: list[tuple[str, str]], terms: list[str], non_terms: list[str]) -> bool:
    """
    Класс 3: Леволинейная грамматика

    :param non_terms:
    :param terms:
    :param rules:
    :return:
    """
    for rule in rules:
        left, right = rule

        if not (len(left) == 1 and left in non_terms):
            return False

        if right == "eps":
            continue

        for el in right[1:]:
            if el not in terms:
                return False

    return True


def is_cfg(rules: list[tuple[str, str]], non_terms: list[str]) -> bool:
    """
    Класс 2: Контекстно-свободная грамматика

    :param non_terms:
    :param rules:
    :return:
    """

    for rule in rules:
        left, right = rule

        if not (len(left) == 1 and left in non_terms):
            return False

        if right == "eps":
            continue

    return True


def is_csg(rules: list[tuple[str, str]], non_terms: list[str], start_symbol: str) -> bool:
    """
    Класс 1: Контекстно-зависимая грамматика

    :param start_symbol:
    :param non_terms:
    :param rules:
    :return:
    """

    flag = False

    for rule in rules:
        left, right = rule

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

        # левая часть
        is_left_ok = False
        for el in non_terms:
            if el in left:
                is_left_ok = True
                break

        if not is_left_ok:
            return False

        # Правая часть
        is_right_ok = False
        if right != "eps":
            is_right_ok = True

        if not is_right_ok:
            return False

        gamma = None
        for index, el in enumerate(left):
            if el not in non_terms:
                continue
            xi_1 = left[:index]
            xi_2 = left[index + 1:]

            if right.startswith(xi_1) and right.endswith(xi_2):
                gamma = right.replace(xi_1, "").replace(xi_2, "")
                if not gamma:
                    continue

        if not gamma:
            return False

    return True


def is_ng(rules: list[tuple[str, str]], start_symbol: str) -> bool:
    """
    Класс 1: Неукорачивающая грамматика

    :param start_symbol:
    :param rules:
    :return:
    """
    flag = False

    for rule in rules:
        left, right = rule

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

        if len(left) > len(right):
            return False

    return True
