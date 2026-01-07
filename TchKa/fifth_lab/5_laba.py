from functools import reduce
import second_laba

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

def symbol_Lezh(a, p):
    while True:
        # print(f'{a}/{p}')
        r = razlozhenie(a)
        if a == 1:
            # 4 свйоство
            # print('4 свойство')
            # print('   1')
            print(' =4= 1')
            return 1
        elif a == -1:
            # 4 свойство
            # print('4 свойство')
            if p % 4 == 1:
                # print('   1')
                print(' =4= 1')
                return 1
            elif p % 4 == 3:
                # print('   -1')
                print(' =4= -1')
                return -1
        elif a == 2:
            # 6 свойство
            # print('6 свойство')
            if p % 8 == 1 or p % 8 == 7:
                # print('   1')
                print(' =6= 1')
                return 1
            elif p % 8 == 3 or p % 8 == 5:
                # print('   -1')
                print(' =6= -1')
                return -1
        elif sum(r.values()) > len(r):
            # 2 свойство
            # print('2 свойство')
            ch = 1
            for key, values in r.items():
                if values >= 2:
                    ch *= key
                    a //= key ** 2
            print(f' =2= (({a} * {ch}^2)/{p}) = ({a}/{p})', end='')
        elif a >= p:
            # 1 свойство
            # print('1 свойство')
            print(f' =1= (({p} * {a // p} + {a % p})/{p}) = ({a % p}/{p})', end='')
            a %= p
        elif len(r) == 0:
            # 7 свойство
            # print('7 свойство')
            num = ((-1) ** (((a - 1) // 2) * ((p - 1) // 2)))
            print(f' =7= (-1)^(({a} - 1)/2 * ({p} - 1)/2) * ({p}/{a}) = '
                  f'(-1)^({(a - 1) // 2} * {(p - 1) // 2}) * ({p}/{a}) = {num} * ({p}/{a}) = [')
            # print('- / - / - / - / -')
            print(f'    ({p}/{a})', end='')
            ans = symbol_Lezh(p, a)
            print(f'  ] = {num} * {ans} = {num * ans}')
            # print('- / - / - / - / -')
            return num * ans
        else:
            # 3 свойство
            # print('3 свойство')
            answer = 1
            sp = []
            for i in r.keys():
                sp.append(f'({i}/{p})')
            print(' =3= ' + ' * '.join(sp) + ' = [')
            for i in r.keys():
                print(f'    ({a}/{i})', end='')
                s_le = symbol_Lezh(i, p)
                answer *= s_le
            print(f'  ] = {answer}')
            return answer



def main():
    print('Вычисление символа Лежандра/Якоби')
    a = int(input('Введите число a >> '))
    p = int(input('Введите число p >> '))
    print()

    if algorithmEuclid(abs(a), p) != 1:
        print(f'({a}/{p}) = 0')
        return

    r = razlozhenie(p)
    znam = []
    if len(r) != 0:
        print('Для нахождения ответа определяем симол Якоби')
        for key, item in r.items():
            for _ in range(item):
                znam.append(key)
    else:
        print('Для нахождения ответа определим символ Лежандра')
        znam = [p]
    print()

    ch = int(input('Выберите способ подсчёта:\n1. Через критерий Эйлера\n2. При помощи свойств\nВведите число >> '))
    print()

    print(f'({a}/{p})', end='')
    answer = []
    if a < 0:
        a = abs(a)
        print(f'= (-1/{p}) * ({a}/{p}) = ', end='')
        if p % 4 == 1:
            print(f'[(-1/{p}) =(4)= 1] = ({a}/{p}) (=)')
            answer.append(1)
        elif p % 4 == 3:
            answer.append(-1)
            print(f'[(-1/{p}) =(4)= -1] = (-1) * ({a}/{p}) (=)')
        # ДОБАВИТЬ КРАСИВЫЙ ВЫВОД
    else:
        print(' (=)')
    print()
    if ch == 1:
        for i in znam:
            znach = second_laba.main(a, i, ((i - 1) // 2))
            if znach > 1:
                znach -= i
            answer.append(znach)
    elif ch == 2:
        for i in znam:
            print(f'  ({a}/{i})', end='')
            answer.append(symbol_Lezh(a, i))
            print()
    ans = reduce(lambda x, y: x * y, answer, 1)
    # print()
    print('(=)', int(ans))


if __name__ == '__main__':
    main()