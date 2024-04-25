"""
Проверка на регулярную грамматику
"""


def pr_na_3(sp):
    # Проходит по всем правилам
    for i in range(len(sp)):
        sp1 = sp[i].split('>')
        # Слева - нетерминалы (Большие)
        lev = sp1[0]
        # Справа - правила
        sp_pr = sp1[1].split('|')
        # Если слева терминалы, то это не регулярная грамматика
        if not lev.isupper():
            return False
        # Проходимся по каждому правилу т.е. T1T, T1U, W, E
        for k in range(len(sp_pr)):
            ind = 0
            pr = sp_pr[k]
            # Если есть эпсилон, то нам всё равно, всё ок
            if len(pr) == 1 and pr == 'E':
                break
            # Проверка на лево и право стороннюю грамматику
            for j in range(len(pr) - 1):
                if ((pr[j].islower() and pr[j + 1].isupper()) or
                        (pr[j + 1].islower() and pr[j].isupper()) or pr.islower()):
                    ind = j
                    break
            ## Это ...
            if ind == 0:
                ind += 1
            if not ((pr[:ind].islower() and pr[ind:].isupper()) or
                    (pr[ind:].islower() and pr[:ind].isupper()) or pr.islower()):
                return False
    return True


"""
Проверка на КС
"""


def pr_na_2(sp):
    for i in range(len(sp)):
        # Проверка на то, чтобы слева были только нетерминалы
        lev = sp[i].split('>')[0]
        if not lev.isupper():
            return False
    return True


"""
Существование языка
"""


def susch_yaz(sp):  # правая цепочка должна принадлежать множетсву нетерминалов?
    # term = input('Введите множество терминалов').split()
    # множество нетерминалов
    N = []
    st = input('Введите стартовый символ >> ')
    # .reverse, так как существование языка смотрится в обратном порядке правил
    sp.reverse()
    for i in range(len(sp)):
        par = sp[i].split('>')
        lev = par[0]
        pr = par[1].split('|')
        marker = True
        for j in range(len(pr)):
            # Проверка на конечность цепочки
            if (not (not pr[j].isupper()) or lev in pr[j]):
                marker = False  # это говорит о том, что мы работаем не с конечной (последней) строкой
        if marker == True:
            # Если с этим правилом ок, то добавляем его нетерминалы в множество нетерминалов
            N.append(lev)
        else:
            # Если с правилом не всё ок, то
            marker1 = False
            for x in N:
                for y in pr:
                    # Если хоть какой-нибудь из множества нетерминалов содержится в правиле, то не ок
                    if x in y:
                        marker1 = True
            # Если правило выводимо и оно не выводится само в себя
            if marker1 and lev not in N:
                N.append(lev)
    if st in N:
        print('Язык КС-грамматики существует')
    else:
        print('Язык КС-грамматики не существует')


"""
Бесполезные символы
"""


def besp_s(sp):
    N = []
    # Список итоговых правил
    sp1 = []
    for i in range(len(sp)):
        par = sp[i].split('>')
        lev = par[0]
        pr = par[1].split('|')
        marker = True
        for j in range(len(pr)):
            # Проверка на конечность цепочки (из большой буквы выводятся большие буквы и это считается как
            # бесполезные символы)
            # not (not pr[j].isupper()) - проверка на то, что терминал порождает нетерминал
            if (not (not pr[j].isupper()) or lev in pr[j]):
                marker = False
        # Если терминал порождает нетерминал, то добавляем его в список итоговых правил
        if marker == True:
            sp1.append(sp[i])
            # if lev not in N:
            #     N.append(lev)

    if sp1 == [] and N == []:
        print('Таких строк нет')
    else:
        for i in sp1:
            print(i)


"""
Недостижимые символы
"""


def ned_s(sp):
    N = []
    N.append(input('Введите стартовый символ >> '))
    sp1 = []
    for i in range(len(sp)):
        par = sp[i].split('>')
        lev = par[0]
        pr = par[1].split('|')
        # Проверка на то, что нетерминалы выводимы из правил
        # Если нетерминал есть в N, то мы добавляем всё, что есть справа
        if lev in N:
            sp1.append(sp[i])
            for x in pr:
                for y in x:
                    N.append(y)

    for i in sp1:
        print(i)


def e_pr(sp):
    n = input('Введите множество нетерминалов >> ').split()
    start_s = input('Введите стартовый символ >> ')
    N = []
    it = []
    it_n = []
    for i in range(len(sp)):
        it_pr = ''
        par = sp[i].split('>')
        lev = par[0]
        pr = par[1].split('|')
        for j in pr:
            if j == 'E':
                N.append(lev)
            mark = True
            for x in j:
                if x not in n:
                    mark = False
            if mark == True:
                it_pr += (j + '|')
                if len(j) > 1:
                    for x in j:
                        it_pr += (x + '|')
            else:
                it_pr += (j + '|')
            # print(it_pr)
        it_n.append(lev)
        it.append(it_pr[:(len(it_pr) - 1)])
        # if j.isupper() and j != 'E':
        #     print(j)
        #     it_pr += j + '|'
        #     for x in j:
        #         it_pr += x + '|'
        #     it_n.append(lev)
        #     it.append(it_pr[:(len(it_pr) - 1)])
    for i in N:
        for j in range(len(it)):
            it_st = ''
            if n[j] == i:
                st = ''
                pr = it[j].split('|')
                for x in pr:
                    if x != 'E':
                        if st == '':
                            for y in range(len(x)):
                                if x[y] not in n:
                                    st += x[y]
                        it_st += x + '|'
                    elif x == 'E' and st != '':
                        it_st += st + '|'
                it[j] = it_st[:(len(it_st) - 1)]
    str_b = 'WRTYUIOPASDFGHJKLZXCVBNM'
    if start_s in it_n:
        for i in str_b:
            if i not in n:
                it_n.insert(0, i)
                it.insert(0, (start_s + '|E'))
                break
    for i in range(len(it_n)):
        print(it_n[i] + '>' + it[i])


"""
Цепные правила
"""


def cep_pr(sp):
    N = input('Введите множество нетерминалов в строку >> ').split()
    # Итоговый список правил
    it_sp = []
    for i in N:
        # Список нетерминалов
        sp_r = []
        sp_r.append(i)
        for j in range(len(sp)):
            par = sp[j].split('>')
            lev = par[0]
            pr = par[1].split('|')
            # Если левая часть находится в списке нетерминалов,
            # то ищем все нетерминалы в правой части и добавляем в список нетерминалов
            # Делаем до последнего правила
            if lev in sp_r:
                for x in pr:
                    for y in x:
                        if y.isupper() and y not in sp_r and y != 'E':
                            sp_r.append(y)
        # Добавляем в итоговую строку 1ый нетерминал
        it_str = sp_r[0] + ">"
        for j in sp:
            # Мы ищем правило, которое выводится из последнего нетерминала
            par = j.split('>')
            lev = par[0]
            # Если левая часть, совпадает с нашим нетерминалом, то добавляем это правило
            if lev == sp_r[-1]:
                it_str += par[1]
        it_sp.append(it_str)
    # print(it_sp)
    for i in it_sp:
        print(i)

"""
Левая факторизация
"""
def lev_fact(sp):
    N = input('Введите множество нетерминалов >> ').split()
    str_b = 'WRTYUIOPASDFGHJKLZXCVBNM'
    it_n = []
    it_pr = []
    for i in range(len(sp)):
        par = sp[i].split('>')
        lev = par[0]
        pr = par[1].split('|')
        nach = ''
        ind = 0
        for j in range(len(pr) - 1):
            # print(pr[j])
            marker = False
            if nach == '':
                dl = len(pr[j]) - 1
                while dl != 0:
                    if pr[j][:dl] == pr[j + 1][:dl]:
                        marker = True
                        nach = pr[j][:dl]
                        for x in str_b:
                            if x not in N:
                                N.append(x)
                                it_n.append(lev)
                                it_pr.append(
                                    nach + x)  # заменить x на любую другую букву, x - это локальная переменная цикла
                                it_n.append(x)
                                it_pr.append(pr[j][dl:])
                                it_n.append(x)
                                it_pr.append(pr[j + 1][dl:])
                                break
                        break
                    dl -= 1
            else:
                if pr[j + 1][:len(nach)] == nach:
                    marker = True
                    it_n.append(N[-1])
                    it_pr.append(pr[j + 1][len(nach):])
            if not marker and nach == '':
                it_n.append(lev)
                it_pr.append(pr[j])
                if j == (len(pr) - 2):
                    it_n.append(lev)
                    it_pr.append(pr[j + 1])
            elif not marker:
                it_n.append(lev)
                it_pr.append(pr[j + 1])
    for i in range(len(it_n)):
        print(it_n[i] + '>' + it_pr[i])

"""
Устранение прямой левой рекурсии
"""
def pr_lev_rec(sp):
    N = input('Введите множество нетерминалов >> ').split()
    str_b = 'WRTYUIOPASDFGHJKLZXCVBNM'
    it_sp = []
    it_N = []
    for i in range(len(sp)):
        it_pr = ''
        par = sp[i].split('>')
        lev = par[0]
        pr = par[1].split('|')
        b = ''
        for j in pr:
            if lev == j[0]:
                for x in str_b:
                    if x not in N and b == '':
                        b = x
                        N.append(x)
                        break
                it_pr += (j[1:] + b) + '|'
                vt_pr = (j[1:] + b) + '|' + j[1:]
                it_sp.append(vt_pr)
                it_N.append(b)
            else:
                it_pr += (j + '|')

        it_pr = it_pr[:(len(it_pr) - 1)]
        it_sp.append(it_pr)
        it_N.append(lev)
    for i in range(len(it_N)):
        print(it_N[i] + '>' + it_sp[i])


print('Эта программа определяет тип грамматики по классификации Хомского')
print('Для корректной работы программы терминалы вводите с прописной, а нетерминалы с заглавной буквы')
n = int(input('Введите количество правил вывода >> '))
print('Введите правила вывода, разделяя их знаком > без пробелов')
sp_pr = []
for i in range(n):
    sp_pr.append(input())
if pr_na_3(sp_pr) or pr_na_2(sp_pr):
    print('Эта грамматика является контекстно-свободной')
    susch_yaz(sp_pr)
    besp_s(sp_pr)
    ned_s(sp_pr)
    cep_pr(sp_pr)
    e_pr(sp_pr)
    lev_fact(sp_pr)
    pr_lev_rec(sp_pr)
else:
    print("Эта грамматика не является контекстно-свободной")

# elif pr_na_2(sp_pr):
#     print('Эта грамматика принадлежит к типу 2 (контекстно-свободная)')

# R>T1T|T1U|W|E
# T>U|T01|T10|E
# U>+U|+0|+1
# W>W-W|W+W
# V>*0|/1

# Q>01A|01B|A
# A>0B1|B|1|E
# B>BA0|B1|C|E
# C>0C11
# D>-D1|-0|-1

#