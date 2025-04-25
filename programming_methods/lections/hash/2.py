def simple_hash(key, table_size):
    return sum(ord(c) for c in str(key)) % table_size


def djb2_hash(key, table_size):
    hash_value = 5381
    for c in str(key):
        hash_value = (hash_value * 33) + ord(c)
    return hash_value % table_size


def multiplicative_hash(key, table_size):
    # Константа A ≈ (√5 - 1)/2 * 2^w, где w - разрядность машины
    A = 2654435769  # Для 32-битных систем
    return (key * A) % (2 ** 32) % table_size


