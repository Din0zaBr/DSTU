from TchKa.second_lab.sixth import is_prime
from TchKa.first_lab.sixth import binary_euclid, final


def nod(a, b):
    while abs(a) != 0 and abs(b) != 0:
        if abs(a) > abs(b):
            a = a % b
        else:
            b = b % a
    return a + b


def fi(m):
    if is_prime(m):
        return m - 1
    else:
        small_degree = 0
        for number in range(1, m):
            a_check, b_check, degree_2 = binary_euclid(m, number)
            if final(a_check, b_check, degree_2) == 1:
                small_degree += 1
        return small_degree


def main(a, b, m):
    output = ''

    flage_a_m = nod(a, m)
    flage_b = b % flage_a_m

    if flage_b == 0:
        output += f'НОД({a}, {m}) = {flage_a_m} и {b} делится на {flage_a_m}\n'
        output += f'Решения существуют и их {flage_a_m}\n'
    else:
        output += f'НОД({a}, {m}) = {flage_a_m} и {b} не делится на {flage_a_m}\n'
        output += 'Решений нет'
        return output

    new_a = a // flage_a_m
    new_b = b // flage_a_m
    new_m = m // flage_a_m
    output += f'{new_a}x = {new_b}(mod {new_m})\n'

    fi_m = fi(new_m) - 1

    x_0 = (new_a ** fi_m) * new_b % new_m
    output += f'x0 = {x_0}\n'

    if flage_a_m == 1:
        return output

    for i in range(1, flage_a_m):
        output += f'x{i} = {x_0 + new_m * i}\n'

    return output


if __name__ == "__main__":
    try:
        a = int(input("Введите a: "))
        b = int(input("Введите b: "))
        m = int(input("Введите m: "))
        print()
        print(main(a, b, m))
    except Exception as e:
        print(f'Ошибка: {e}')
