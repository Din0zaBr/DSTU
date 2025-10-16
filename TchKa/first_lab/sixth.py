# НОД - это наибольший делитель, всегда меньше или равен наименьшему из исходных чисел.
# НОК (наименьшее общее кратное) - наоборот, больше или равен наибольшему числу.

def binary_euclid(c, d):
    two_degrees = 0
    while 1 < c != d > 1:
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
    if e == f:
        print(f"НОД ({e},{f}) = {e * (2 ** degree_of_two)}")
        return e * (2 ** degree_of_two)
    if e != 0:
        if f == 1:
            print(
                f"НОД ({e},{f}) = {f} и домножаем на {degree_of_two} степень двойки. Значит {f * (2 ** degree_of_two)}")
            return f * (2 ** degree_of_two)
        if f == 0:
            print(
                f"НОД ({e},{f}) = {e} и домножаем на {degree_of_two} степень двойки. Значит {e * (2 ** degree_of_two)}")
            return e * (2 ** degree_of_two)
    if f != 0:
        if e == 0:
            print(
                f"НОД ({e},{f}) = {f} и домножаем на {degree_of_two} степень двойки. Значит {f * (2 ** degree_of_two)}")
            return f * (2 ** degree_of_two)
        if e == 1:
            print(
                f"НОД ({e},{f}) = {e} и домножаем на {degree_of_two} степень двойки. Значит {e * (2 ** degree_of_two)}")
            return e * (2 ** degree_of_two)


def checking(w, y):
    w, y = abs(w), abs(y)
    if y != 0:
        if w == 1:
            print(f"НОД ({y},{w}) = {w}")
            return False
        if w == 0:
            print(f"НОД ({y},{w}) = {y}")
            return False
    if w != 0:
        if y == 0:
            print(f"НОД ({y},{w}) = {w}")
            return False
        if y == 1:
            print(f"НОД ({y},{w}) = {y}")
            return False

    return w, y

# Эта часть куда выключена, так как используется в second_lab\sixth.py.
# Её можно включить в кол, если необходим лишь этот файл

# Flag = 1
# while Flag:
#     try:
#         a, b = int(input("a = ")), int(input("b = "))
#         print()
#         if checking(a, b):
#             a, b = checking(a, b)
#             a, b, degree_2 = binary_euclid(a, b)
#             final(a, b, degree_2)
#             Flag = int(input("Если хотите прервать программу, введите 0: "))
#             print()
#     except:
#         print("Введите два целых числа")
#         print()
