import utils


# a, b
# A, B
# S

# S -> aA|bA
# A -> + aB - bC|+ bC - aB| + aB - aB| + bC - bC
# A -> + aBC - bBC|+ bBC - aBC| + aBC - aBC| + bBC - bBC
# B -> aB|a
# C -> bC|b
def main():
    print(
        "Введите терминальные символы"
        " ('end' для окончания): "
    )
    terms = []
    while True:
        term = input("> ").strip()
        if term == "end":
            break

        if len(term) == 1:
            terms.append(term)

    print(
        "Введите нетерминальные символы"
        " ('end' для окончания): "
    )
    non_terms = []
    while True:
        non_term = input("> ").strip()
        if non_term == "end":
            break

        if len(non_term) == 1:
            non_terms.append(non_term)

    start_symbol = input("Введите стартовый символ: ").strip()

    print(
        "Введите правила грамматики в формате: "
        "'A->a|b|c' или 'S -> a'"
        " ('end' для окончания): "
    )
    rules = []
    while True:
        rule = input("> ").strip()
        if rule != 'end':
            left, right = rule.split('->')
            for el in right.split('|'):
                rules.append((left.strip(), el.strip()))
        else:
            break

    if utils.is_rrg(rules, terms, non_terms):
        print("Класс 3: Праволинейная грамматика")
        return
    elif utils.is_lrg(rules, terms, non_terms):
        print("Класс 3: Леволинейная грамматика")
        return
    elif utils.is_cfg(rules, non_terms):
        print("Класс 2: Контекстно-свободная грамматика")
        return
    elif utils.is_ng(rules, start_symbol):
        if utils.is_csg(rules, non_terms, start_symbol):
            print("Класс 1: Контекстно-зависимая грамматика")
            return
        else:
            print("Класс 1: Неукорачивающая грамматика")
            return
    else:
        print("Класс 0:  Неограниченная грамматика")


if __name__ == '__main__':
    main()
