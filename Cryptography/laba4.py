import math
from laba3 import  Euler_Function,Mod_Reduction, Solve_Comparison

def poparno_prostye(spisok_m):
    for i in range(len(spisok_m)):
        for j in range(i + 1, len(spisok_m)):
            if math.gcd(spisok_m[i], spisok_m[j]) != 1:
                return False

    return True

def poisk_Mi(spisok_m):
    spisok_M = []
    proizvedenie = 1

    for j in spisok_m:
        proizvedenie *= j

    for i in spisok_m:
        spisok_M.append(proizvedenie // i)

    return spisok_M, proizvedenie

def poisk_Ni(spisok_m, spisok_M):
    spisok_N = []

    for i in range(len(spisok_M)):
        Mi = spisok_M[i]
        mi = spisok_m[i]
        print(f'{Mi}^(-1) mod {mi}')

        if math.gcd(Mi, mi) == 1:
            print(f'НОД({Mi},{mi}) = 1, используем теорему Эйлера: ')

            fi = Euler_Function(mi) - 1

            print(f'{Mi}^{fi} mod {mi}')

            if Mi > mi:
                Mi = Mod_Reduction(Mi, mi)

            print(f'{Mi}^{fi} mod {mi}')

            Mi **= fi

            print(f'{Mi} mod {mi}')

            Mi = Mod_Reduction(Mi, mi)

            print(f'{Mi} mod {mi}')

            spisok_N.append(Mi)

    return spisok_N

def poisk_x0(spisok_b, spisok_M, spisok_N, new_m):
    x0 = 0

    for i in range(len(spisok_M)):
        x0 += int(spisok_M[i]) * int(spisok_N[i]) * int(spisok_b[i])

    print(f'x0 = {x0} (mod {new_m})')

    x0 %= new_m

    return x0

def main():
    n = int(input('Введите количество сравнений: '))
    spisok_a = []
    spisok_b = []
    spisok_m = []

    for i in range(n):
        print(f'Введите числа a, b, m через пробел для {i+1} сравнения')
        a = int(input('Введите a: '))
        b = int(input('Введите b: '))
        m = int(input('Введите m: '))
        if b < 0:
            b = m + b
        spisok_a.append(a)
        spisok_b.append(b)
        spisok_m.append(m)

    print('Вы ввели: ')
    for j in range(n):
        print(str(spisok_a[j]) + 'x' + '≡' + str(spisok_b[j]) + '(mod ' + str(spisok_m[j]) + ')')

    if any(x != 1 for x in spisok_a):
        for p in spisok_a:
            if p != 1:
                ind_zameni = spisok_a.index(p)
                print(f'Разрешение {ind_zameni + 1} сравнения:')
                zamena_v_a = spisok_a[ind_zameni]
                zamena_v_b = spisok_b[ind_zameni]
                zamena_v_m = spisok_m[ind_zameni]
                zamena_v_c = Solve_Comparison(zamena_v_a, zamena_v_b, zamena_v_m)
                if zamena_v_c == 'Сравнение не разрешимо':
                    print(f'Cравнение {ind_zameni+1} не разрешимо')
                    print('Система не имеет решений')
                    return

                spisok_m[ind_zameni] = spisok_m[ind_zameni] // math.gcd(spisok_a[ind_zameni], spisok_m[ind_zameni])
                spisok_a[ind_zameni] = 1
                spisok_b[ind_zameni] = zamena_v_c[0]

        print('Система была приведена к виду пригодной для КТО')
        for f in range(n):
            print(str(spisok_a[f]) + 'x' + '≡' + str(spisok_b[f]) + '(mod ' + str(spisok_m[f]) + ')')

    if poparno_prostye(spisok_m) == True:
        print('Решение существует')
    else:
        print('Решение не существует')
        return

    spisok_M, new_m = poisk_Mi(spisok_m)
    print(f'Список найденных Mi: ', spisok_M)

    spisok_N = poisk_Ni(spisok_m, spisok_M)
    print(f'Список найденных Ni: ', spisok_N)

    print("Коеффициены b = ", spisok_b)
    print("Коеффициены Mi = ", spisok_M)
    print("Коеффициены Ni = ", spisok_N)
    print("Поле ",new_m)

    x0 = poisk_x0(spisok_b, spisok_M, spisok_N, new_m)

    print(f'Решение системы: {x0}')

    print('Проверка: ')

    for k in range(len(spisok_M)):
        if x0 % spisok_m[k] == spisok_b[k]:
            print(f'{x0} ≡ {spisok_b[k]} (mod {spisok_m[k]})')
        else:
            print('Ошибка в проверке!')

if __name__ == "__main__":
    main()