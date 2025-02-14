def mod_inverse(a, p):
    """Вычисление мультипликативной инверсии по модулю p."""
    if a > 0:
        return a % p
    elif a < 0 and abs(a) <= p:
        return p + a
    else:
        test = abs(a) // p
        return a + p * test


print(mod_inverse(0, 509))
