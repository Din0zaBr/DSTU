def binary_gcd_chain(a, b):
    chain = [f"НОД({a},{b})"]

    while a != b:
        if a == 0:
            chain.append(str(b))
            return b, chain
        if b == 0:
            chain.append(str(a))
            return a, chain

        if a % 2 == 0 and b % 2 == 0:
            a, b = a // 2, b // 2
            chain.append(f" = 2*НОД({a},{b})")
            continue

        if a % 2 == 0 and b % 2 == 1:
            a //= 2
            chain.append(f" = НОД({a},{b})")
            continue
        if a % 2 == 1 and b % 2 == 0:
            b //= 2
            chain.append(f" = НОД({a},{b})")
            continue

        if a > b:
            a -= b
            chain.append(f" = НОД({a},{b})")
        else:
            b -= a
            chain.append(f" = НОД({a},{b})")

    chain.append(f"={a}")
    return a, chain

    print(f"НОД({a},{b}) = {g}")
