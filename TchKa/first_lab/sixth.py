# НОД - это наибольший делитель, всегда меньше или равен наименьшему из исходных чисел.
# НОК (наименьшее общее кратное) - наоборот, больше или равен наибольшему числу.

def binary_euclid(c, d):
    two_degrees = 0
    while c != 0 and d != 0 and c != 1 and d != 1 and c != d:
        if c % 2 == 0 and d % 2 == 0:
            print(f"{c}, {d} - чётные -> a = {c}/2, b = {d}/2")
            c = c // 2
            d = d // 2
            two_degrees += 1
            print(f'a = {c}, b = {d}')
            print(f'Притом НОД надо после умножить на 2^{two_degrees}')
            print()
        elif (c % 2 == 0 and d % 2 != 0) or (c % 2 != 0 and d % 2 == 0):
            if c % 2 == 0:
                print(f"{c} - чётное, {d} - нечётное -> a = {c}/2, b = {d}")
                c = c // 2
                print(f'a = {c}, b = {d}')
                print()
            else:
                print(f"{c} - нечётное, {d} - чётное -> a = {c}, b = {d}/2")
                d = d // 2
                print(f'a = {c}, b = {d}')
                print()
        elif c % 2 != 0 and d % 2 != 0:
            if c > d:
                print(f"{c}, {d} - нечётные, притом {c} > {d} -> a = {c}-{d}, b = {d}")
                c = c - d
                print(f'a = {c}, b = {d}')
                print()
            else:
                print(f"{c}, {d} - нечётные, притом {d} > {c} -> a = {c}, b = {d} - {c}")
                d = d - c
                print(f'a = {c}, b = {d}')
                print()
    return c, d, two_degrees


def final(e, f, degree_of_two):
    if e == 0 and f != 0:
        print(f"НОД ({e},{f}) = {f}")
    if e != 0 and f == 0:
        print(f"НОД ({e},{f}) = {e}")
    if e == f:
        print(f"НОД ({e},{f}) = {e * (2 ** degree_of_two)}")
    if e == 1 and f != 0:
        print(f"НОД ({e},{f}) = {e}")
    if e != 0 and f == 1:
        print(f"НОД ({e},{f}) = {f}")


def checking(w, y):
    if w < 0:
        w *= -1
    if y < 0:
        y *= -1
    return w, y


a, b = int(input("Введите первое число: ")), int(input("Введите второе число: "))
print()
a, b = checking(a, b)
a, b, degree_2 = binary_euclid(a, b)
final(a, b, degree_2)
