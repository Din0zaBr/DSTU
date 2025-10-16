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
        return a * a, m, degree - 1
    else:
        return a, m, degree


def small_theorem(m, a, degree, k):
    small_degree = m - 1
    diff = degree // small_degree
    print(f"Получим {small_degree} и умножим на {diff} = {small_degree * diff}")
    new_degree = degree - small_degree * diff
    print(f"Новая степень = {new_degree} вместо {degree}. Получаем {a} в степени {new_degree} по модулю {m}")
    return (pow(a, new_degree) * k) % m


def ailer(digit, base, degree, k):
    print()
    small_degree = 0
    if is_prime(digit):
        small_degree = digit - 1
        diff = degree // small_degree
        print(f"Получим {small_degree} и умножим на {diff} = {small_degree * diff}")
        new_degree = degree - small_degree * diff
        print(f"Новая степень = {new_degree} вместо {degree}. Получаем {base} в степени {new_degree} по модулю {digit}")
        return pow(base, new_degree) % digit
    else:
        for number in range(1, digit):
            print()
            print(f"Находим НОД для {digit, number}")
            print()
            a, b, degree_2 = binary_euclid(digit, number)
            if final(a, b, degree_2) == 1:
                small_degree += 1
            else:
                continue
        diff = degree // small_degree
        print(f"Получим {small_degree} и умножим на {diff} = {small_degree * diff}")
        new_degree = degree - small_degree * diff
        print(f"Новая степень = {new_degree} вместо {degree}. Получаем {base} в степени {new_degree} по модулю {digit}")
        return (pow(base, new_degree) * k) % digit


def main():
    Flag = 1
    sum = 0
    while Flag:
        try:
            a, degree, m = int(input("a = ")), int(input("Степень = ")), int(input("m = "))
            a, m, degree = checking(a, m, degree)
            a_check, m_check, degree_2 = binary_euclid(a, m)
            NOD = final(a_check, m_check, degree_2)
            print()
            coefficient = 1
            if NOD != 1:
                print(f"НОД {a, m} = {NOD}, потому имеем право {a, m} поделить на {NOD}")
                while NOD != 1:
                    coefficient *= NOD
                    a_check, a = a_check // 3, a // 3
                    m_check, m = m_check // 3, m // 3
                    a_check, m_check, degree_2 = binary_euclid(a_check, m_check)
                    NOD = final(a_check, m_check, degree_2)
            else:
                if is_prime(m):
                    print()
                    print("Используем малую теорему Ферма")
                    remainder = small_theorem(m, a, degree, coefficient)
                    print(f"Остаток = {remainder}")
                    sum += remainder
                    print(f"Итого: {sum}")


                else:
                    print()
                    print("Используем теорему Эйлера")
                    remainder = ailer(m, a, degree, coefficient)
                    print(f"Остаток = {remainder}")
                    sum += remainder
                    print(f"Итого: {sum}")

            Flag = int(input("Если хотите прервать программу, введите 0: "))
            print()
        except:
            print()
            print("Введите три целых числа")
            print()


if __name__ == "__main__":
    main()
