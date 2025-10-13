from TchKa.first_lab.sixth import binary_euclid, final
from math import sqrt


def is_prime(digit):
    if digit < 2:
        return False
    if digit == 2:
        return True
    if digit % 2 == 0:
        return False
    for i in range(3, int(sqrt(digit)) + 1, 2):
        if digit % i == 0:
            return False
    return True


def checking(a, m, degree):
    if a < 0 and degree % 2 == 0:
        return abs(a), m, degree
    elif a < 0 and degree % 2 == 1:
        return abs(a), m, degree - 1
    else:
        return a, m, degree


def small_theorem(m, a, degree):
    small_degree = m - 1
    diff = degree // small_degree
    new_degree = degree - small_degree * diff
    print(f"Новая степень = {new_degree} вместо {degree}. Получаем {a} в степени {new_degree} по модулю {m}")
    return pow(a, new_degree) % m


def ailer(digit):
    print()
    count = 0
    if is_prime(digit):
        digit -= 1
        
    for number in range(1, digit):
        a, b, degree_2 = binary_euclid(digit, number)
        if final(a, b, degree_2) == 1:
            count += 1
        else:
            continue
    return count


Flag = 1
while Flag:
    try:
        a, degree, m = int(input("a = ")), int(input("Степень = ")), int(input("m = "))
        a, m, degree = checking(a, m, degree)
        # print(a, m, degree)
        a_check, m_check, degree_2 = binary_euclid(a, m)
        # print(a_check, m_check, degree_2)
        # print(a_check, m_check, degree_2)
        NOD = final(a_check, m_check, degree_2)
        print(NOD)
        print(is_prime(m))
        if NOD == 1 and is_prime(m):
            print(small_theorem(m, a, degree))
        if NOD == 1 and not (is_prime(m)):
            phi = ailer(m)
            print(phi)
        Flag = int(input("Если хотите прервать программу, введите 0: "))
        print()
    except:
        print("Введите три целых числа")
        print()
