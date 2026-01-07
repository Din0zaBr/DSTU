from functools import reduce


def pryamoyHod(p, a):
    mnozhitel = p // a
    ostatok = p % a
    return [mnozhitel, ostatok]


def algorithmEuclid(a, b):
    sp = []
    sp1 = []
    n = max(a, b)
    k = min(a, b)
    nod = 0
    while True:
        mnozh, ost = pryamoyHod(n, k)
        sp.append(str(n) + '=' + str(k) + '*' + str(mnozh) + '+' + str(ost))
        sp1.append([n, k, mnozh, ost])
        if ost == 0:
            nod = k
            break
        n = k
        k = ost
    return nod


def razlozhenie(n):
    sl = {}
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            sl[i] = 0
            while n % i == 0:
                n //= i
                sl[i] += 1
    return sl


def func_Eilera(m):
    if m == 1:
        print(f'ф({m}) = 1')
        return 1
    sl = razlozhenie(m)
    if len(sl) == 0:
        print(f'ф({m}) = {m - 1}')
        return m - 1
    else:
        zn = m
        st = f'ф({m}) = {zn}'
        for i in sl.keys():
            zn *= (1 - 1 / i)
            st += f' * (1 - 1/{i})'
        st += f' = {int(zn)}'
        print(st)
        return int(zn)


def t_Pherma(m):
    print('Используем теорему Ферма')
    return m - 1


def t_Eilera(m):
    print('Используем теорему Эйлера')
    return func_Eilera(m)


def main(a, m, st):
    # a = int(input('Введите число a >> '))
    if a < 0:
        while a < 0:
            a += m
    # st = int(input('Введите степень числа a >> '))
    # m = int(input('Введите модуль >> '))
    print()
    nod = algorithmEuclid(a, m)
    print(f'НОД({a}, {m}) = {nod}')
    if nod != 1:
        print('Введены некорректные данные, попробуйте ещё раз')
        return
    if len(razlozhenie(m)) == 0:
        n_st = t_Pherma(m)
    else:
        n_st = t_Eilera(m)
    print(f'{a}^{n_st} = 1 (mod {m})')
    c_st = st % n_st
    answer = (f'{a}^{st} (mod {m}) = ({a}^{n_st})^{st // n_st} * {a}^{c_st} (mod {m}) = '
              f'1^{st // n_st} * {a}^{c_st} (mod {m}) = {a}^{c_st} (mod {m})')
    mn = []
    if a > m:
        answer += f' = [{a} = {a % m} (mod {m})] = {a % m}^{c_st} (mod {m})'
        a %= m
    while c_st != 1:
        if c_st % 2 != 0:
            mn.append(a)
            c_st -= 1
        answer += ' = '
        for i in mn:
            answer += f'{i} * '
        c_st //= 2
        answer += f'({a}^2)^{c_st} (mod {m})'
        if (a ** 2) > m:
            answer += f' = [{a ** 2} = {(a ** 2) % m} (mod {m})]'
        a = (a ** 2) % m
        answer += ' = '
        for i in mn:
            answer += f'{i} * '
        answer += f'{a}^{c_st} (mod {m})'
    a = reduce(lambda x, y: x * y, mn, a)
    answer += f' = {a} (mod {m}) = {a % m}'
    print(answer)
    return a % m


if __name__ == '__main__':
    main()
