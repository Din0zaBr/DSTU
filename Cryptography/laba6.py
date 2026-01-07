from laba5 import quadratic_residue
from laba3 import Mod_Reduction, Euler_Function
from laba1_bin import binary_gcd_chain
from sympy import isprime

def cluchay(p, a):
    """Функция выбора случая для приведения к полю"""
    if Mod_Reduction(p, 4) == 3:
        rech1(p, a)
    elif Mod_Reduction(p, 8) == 5:
        rech2(p, a)
    else:
        rech3(p, a)

def rech1(p, a):
    """Случай 1: p ≡ 3 (mod 4)"""
    print("Случай 1: p ≡ 3 (mod 4)")
    m = (p - 3) // 4
    print(f"Разложение: {p} = 4 * {m} + 3, следовательно m = {m}")
    print(f"Используем формулу x ≡ ± a^(m+1) (mod p) - ± пока отпустим")
    print(f"x ≡ {a}^({m}+1) (mod {p})")
    Mod_Reduction(m, p)
    exponent = m + 1
    a = pow(a, exponent)
    result = Mod_Reduction(a,p)
    print(f"x ≡ {a} (mod {p}) ≡ {result} (mod {p})")
    print(f"Следовательно x ≡ ± {result} (mod {p}) или")
    print(f"x_1 ≡ {result} (mod {p})")
    x = - result
    x_2 = Mod_Reduction(x, p)
    print(f"x_2 ≡ {x_2} (mod {p})")
    stepen = pow(result, 2)
    a_new = Mod_Reduction(stepen, p)
    print(f"Проверка: (± {result}) = {stepen} = {a_new}")



def rech2(p, a):
    """Случай 2: p ≡ 5 (mod 8)"""
    print("Случай 2: p ≡ 5 (mod 8)")
    m = (p - 5) // 8
    print(f"Разложение: {p} = 8 * {m} + 5, следовательно m = {m}")
    print(f"Используем формулу x ≡ ± a^(2m+1) (mod p) - ± пока отпустим")
    print(f"x ≡ {a}^(2*{m}+1) (mod {p})")
    print(f"x ≡ {a}^{2*m + 1} (mod {p})")
    Mod_Reduction(m, p)
    exponent = 2*m + 1
    a1= pow(a, exponent)
    result = Mod_Reduction(a1, p)
    print(f"x ≡ {a}^{2*m + 1} (mod {p}) ≡ {result} (mod {p})")
    if result == 1:
        print(f"Так как result = {result}, следовательно используем формулу x ≡ ± a^(m+1) (mod p)")
        print(f"x ≡ {a}^({m}+1) (mod p)")
        print(f"x ≡ {a}^({m+1}) (mod p)")
        exponent = m + 1
        a1 = pow(a, exponent)
        res = Mod_Reduction(a1, p)
        print(f"x ≡ ± {res} (mod p) или")
        print(f"x_1 ≡ {res} (mod {p})")
        x = - res
        x_2 = Mod_Reduction(x, p)
        print(f"x_2 ≡ {x_2} (mod {p})")
        stepen = pow(res, 2)
        a_new = Mod_Reduction(stepen, p)
        print(f"Проверка: (± {res}) = {stepen} = {a_new}")
    elif result == p-1:
        print(f"Так как {result} mod {p} ≡ -1, следовательно используем формулу x ≡ ± a^(m+1) * 2^(2m+1) (mod p)")
        result_new = 2*m+1
        print(f"x ≡ {a}^{m+1} * 2^{result_new} (mod {p})")
        res1 = pow(a,m+1)
        res2 = pow(2,result_new)
        result_new2 = res1*res2
        res = Mod_Reduction(result_new2, p)
        print(f"x ≡ ± {res} (mod {p}) или")
        print(f"x_1 ≡ {res} (mod {p})")
        x = - res
        x_2 = Mod_Reduction(x, p)
        print(f"x_2 ≡ {x_2} (mod {p})")
        stepen = pow(res, 2)
        a_new = Mod_Reduction(stepen, p)
        print(f"Проверка: (± {res}) = {stepen} = {a_new}")


def rech3(p, a):
    """Случай 3: другие простые числа"""
    print(f"Так как {p} ≠ 3 (mod 4) и {p} ≠ 5 (mod 8), следовательно используем 3 случай: ")
    print("3 шаг. "
          "Выберем N такое, что (N/p) = -1")
    found = False
    for n in range(2, p):
        if isprime(n):
            legendre_symbol = pow(n, (p - 1) // 2, p)
            if legendre_symbol == p - 1:  # Это означает -1 mod p
                print(f"N = {n}, следовательно ({n}/{p}) = -1")
                found = True
                N = n
                break
            else:
                print(f"N = {n}, следовательно ({n}/{p}) = 1 - не подходит")
    print("4 шаг. Представим p = 2^k * h + 1, где h - нечетное")
    k = 0
    h = p - 1
    while h % 2 == 0:
        k += 1
        h //= 2
    print(f"{p} = 2^{k} * {h} + 1")
    print(f"Следовательно: k = {k}, h = {h}")
    stepen_chag5 = (h + 1) / 2
    a_new = pow(a, stepen_chag5)
    a_1 = int(Mod_Reduction(a_new, p))
    print(f"5 шаг. a_1 = a^(h+1)/2 (mod p) = {a}^{int(stepen_chag5)} (mod {p}) = {a_1} (mod {p})")
    gcd_result, gcd_chain = binary_gcd_chain(a, p)
    if gcd_result == 1:
        print(f"a_2 = a^-1 (mod p) = {a}^-1 (mod {p}) = [НОД({a}, {p}) = {gcd_result}, следовательно {a}^-1 - существует, используем теорему Эйлера: a^-1 = a^φ(m)-1 (mod p)]")
        print(f"{a}^φ({p})-1 (mod {p})")
        Euler = Euler_Function(p)
        print(f"{a}^({Euler} - 1) (mod {p})")
        Euler = Euler - 1
        a_2 = pow(a, Euler)
        a_2 = Mod_Reduction(a_2, p)
        print(f"{a}^({Euler}) (mod {p}) ≡ {a_2} (mod {p})")
        N_1 = pow(n,h)
        N_1 = Mod_Reduction(N_1, p)
        print(f"N_1 = N^h (mod p) = {n}^{h} (mod {p}) ≡ {N_1} (mod {p})")
        N_2 = 1
        j = 0
        print(f"N2 = {N_2}; j = {j}")
        print(f"6 шаг. Построение таблицы")
        print(f"\n{'i':<3} {'b':<10} {'c':<10} {'d':<15} {'j_i':<5} {'N2_new':<10}")
        print("-" * 60)
        for i in range(0, k - 1):
            # b = a_1 * N2 (mod p)
            b = int(Mod_Reduction(a_1 * N_2, p))
            #print(f"b = {a_1} * {N_2} ≡ {b} (mod {p})")

            # c = a_2 * b^2 (mod p)
            b_squared = int(pow(b,2))
            c = Mod_Reduction(a_2 * b_squared, p)
            #print(f"c = {a_2} * {b}^2 = {a_2} * {b_squared} ≡ {c} (mod {p})")

            # d = c^(2^(k-2-i)) (mod p)
            exponent_d = pow(2, k - 2 - i)
            d = pow(c, exponent_d)
            d = Mod_Reduction(d, p)
            #print(f"d = {c}^(2^{k - 2 - i}) = {c}^{exponent_d} ≡ {d} (mod {p})")

            # Определяем j_i
            if d == p - 1:  # d ≡ -1 mod p
                j_i = 1
                #print(f"d ≡ -1 (mod {p}) ⇒ j_i = 1")
            elif d == 1:
                j_i = 0
                #print(f"d ≡ 1 (mod {p}) ⇒ j_i = 0")
            else:
                j_i = 0
                #print(f"d = {d} ⇒ j_i = 0")

            exponent_N2 = pow(2, i) * j_i
            N1_power = pow(N_1, exponent_N2, p)
            N_2_new = (N_2 * N1_power) % p
            #print(f"N2_new = N2 * N1^(2^i * j_i) = {N_2} * {N_1}^{exponent_N2} = {N_2} * {N1_power} ≡ {N_2_new} (mod {p})")

            print(f"{i:<3} {b:<10} {c:<10} {f'{d} (≡ {d if d != p - 1 else -1})':<15} {j_i:<5} {N_2_new:<10}")
            N_2 = N_2_new
            print()

        print(f"7 шаг. Результат: x ≡ ± a_1 * N_2 (mod p)")
        result = a_1 * N_2
        result = Mod_Reduction(result, p)
        print(f"x ≡ ± {a_1} * {N_2} (mod {p}) ≡ ± {result} (mod {p}) или ")
        print(f"x_1 = {result} (mod {p})")
        res = - result
        res = Mod_Reduction(res, p)
        print(f"x_2 = {res} (mod {p})")
    else:
        print(f"Числа не взаимнопростые, {a}^-1 - не существует")
def main():
    """Главная функция"""
    a = int(input("Введите число a: "))
    p = int(input("Введите число p: "))
    print(" ")
    print("1 шаг: ")
    quadratic_residue(a, p)
    print(" ")
    print("2 шаг: ")
    cluchay(p, a)

if __name__ == "__main__":
    main()
