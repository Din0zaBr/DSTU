def isPrime(num):
    if num % 2 == 0:
        return num == 2
    d = 3
    while d * d <= num and num % d != 0:
        d += 2
    return d * d > num


def xgcd(a: int, b: int) -> tuple[int, int, int]:
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


# A => B
# User B
p = int(input("Введите простое число: p = "))  # 5
if isPrime(p) == False:
    print(f"Число {p} не простое")
    while isPrime(p) == False:
        p = int(input("Введите простое число: p = "))
        if isPrime(p) == True:
            break
        else:
            print(f"Число {p} опять не является простым")

q = int(input("Введите простое число: q = "))  # 11
if isPrime(q) == False:
    print(f"Число {q} не простое")
    while isPrime(q) == False:
        q = int(input("Введите простое число: q = "))
        if isPrime(q) == True:
            break
        else:
            print(f"Число {q} опять не является простым")

n = p * q

phi = (p - 1) * (q - 1)

e = int(input("Введите простое число: e = "))  # 65537
if isPrime(e) == False:
    print(f"Число {e} не простое")
    while isPrime(e) == False:
        e = int(input("Введите простое число: e = "))
        if isPrime(e) == True:
            break
        else:
            print(f"Число {e} опять не является простым")

d, private_key, b = xgcd(e, phi)

private_key = private_key % phi

public_key = e

# User A
message = int(input("Введите число, которое будет зашифровано: "))  # 54
if message >= n:
    print(f"Введённое число {message} не может быть больше или равняться {n}")
    while message >= n:
        message = int(input("Введите число, которое будет зашифровано: "))
        if message < n:
            break
        else:
            print(f"Введённое число {message} не может быть больше или равняться {n}")
encrypt_msg = pow(message, public_key, n)

# User B
decrypted_msg = pow(encrypt_msg, private_key, n)

print(message, decrypted_msg)
