import struct
import random
import os

KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "key.txt")
MOD32 = 2 ** 32
BLOCK_SIZE = 8
ROUNDS = 32

S_BOX = [
    [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
    [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
    [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
    [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
    [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
    [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 14, 15, 12],
    [13, 11, 4, 10, 7, 2, 1, 5, 0, 8, 15, 14, 9, 3, 12, 6],
    [1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2],
]


def _get_subkey_index(i):
    return i % 8 if i < 24 else (31 - i) % 8


def _rotate_left11(value):
    return ((value << 11) | (value >> 21)) % MOD32


def s_block(value):
    result = []
    binary_value = f"{value:032b}" # Число превращается в двоичную строку длиной 32 символа (с ведущими нулями)
    for i in range(8):
        search_id = int(binary_value[i * 4: (i + 1) * 4], 2)
        result.append(f"{S_BOX[i][search_id]:04b}")
    return int("".join(result), 2) # , 2 - бинарный вид


def _feistel_round(N1, N2, Ki, show_steps, round_num):
    S_sum = (N1 + Ki) % MOD32
    S_block_out = s_block(S_sum)
    S = _rotate_left11(S_block_out)
    N1_new, N2_new = N2 ^ S, N1

    if show_steps:
        print(f"Раунд {round_num}. До ключа: L = {N1:08X} ({N1:032b}), R = {N2:08X} ({N2:032b})")
        print(f"Ключ = {Ki:08X} ({Ki:032b})")
        print(f"Сложение с ключом = {S_sum:08X} ({S_sum:032b})")
        print(f"После S-блока = {S_block_out:08X} ({S_block_out:032b})")
        print(f"После сдвига на 11 = {S:08X} ({S:032b})")
        print(f"После XOR: L = {N1_new:08X} ({N1_new:032b}), R = {N2_new:08X} ({N2_new:032b})")

    return N1_new, N2_new


def encrypt(block, key, show_steps=True):
    block = block.ljust(BLOCK_SIZE, b'\x00')
    N1, N2 = struct.unpack('<II', block)
    for i in range(ROUNDS):
        print("=" * 40)
        Ki = key[_get_subkey_index(i)]
        N1, N2 = _feistel_round(N1, N2, Ki, show_steps, i + 1)
    return struct.pack('<II', N2, N1)


def decrypt(block, key, show_steps=True):
    block = block.ljust(BLOCK_SIZE, b'\x00')
    N1, N2 = struct.unpack('<II', block)
    for i in reversed(range(ROUNDS)):
        print("=" * 40)
        Ki = key[_get_subkey_index(i)]
        N1, N2 = _feistel_round(N1, N2, Ki, show_steps, ROUNDS - i)
    return struct.pack('<II', N2, N1)


def pad_message(message):
    encoded = message.encode('utf-8')
    size = ((len(encoded) + BLOCK_SIZE - 1) // BLOCK_SIZE) * BLOCK_SIZE
    return encoded.ljust(size, b'\x00')


def generate_key():
    key = [random.randint(0, 0xFFFFFFFF) for _ in range(8)]
    key_hex = ''.join(f"{k:08X}" for k in key)
    with open(KEY_FILE, "w") as f:
        f.write(key_hex)
    print(f"Ключ сгенерирован и сохранен в файл: {key_hex}")
    return key


def load_key():
    if not os.path.exists(KEY_FILE):
        print("Файл с ключом не найден! Сначала сгенерируйте ключ.")
        return None
    with open(KEY_FILE, "r") as f:
        return process_key(f.read().strip())


def process_key(key_str):
    try:
        key_bytes = bytes.fromhex(key_str)
        if len(key_bytes) != 32:
            raise ValueError
        key = [struct.unpack("<I", key_bytes[i:i + 4])[0] for i in range(0, 32, 4)]
        # Строка берёт 32 байта (key_bytes) и преобразует их в список из 8 целых чисел (каждое по 4 байта = 32 бита)
        # [0] потому что кортеж вернёт (число, )
        return key
    except ValueError:
        print("Ошибка: ключ должен быть 32-байтовым (64 HEX-символа)!")
        return None


def _format_binary(data):
    return ' '.join(f"{b:08b}" for b in data)


def _process_blocks(data, key, cipher_func):
    return b''.join(
        cipher_func(data[i:i + BLOCK_SIZE], key)
        for i in range(0, len(data), BLOCK_SIZE)
    )


def main():
    while True:
        print("\n" + "=" * 40)
        print("1. Сгенерировать ключ и сохранить в файл")
        print("2. Зашифровать текст")
        print("3. Расшифровать текст")
        print("4. Выйти")
        print("=" * 40)
        choice = input("Введите команду: ").strip()

        if choice == "1":
            generate_key()
        elif choice in ("2", "3"):
            key_str = input("Ключ (64 HEX) или Enter для загрузки из файла: ").strip()
            key = load_key() if not key_str else process_key(key_str)
            if not key:
                continue

            if choice == "2":
                msg = pad_message(input("Введите сообщение: "))
                enc = _process_blocks(msg, key, encrypt)
                print(f"Зашифрованное (HEX): {enc.hex()}")
                print(f"Зашифрованное (BIN): {_format_binary(enc)}")
            else:
                try:
                    enc = bytes.fromhex(input("Зашифрованное сообщение (HEX): "))
                    dec = _process_blocks(enc, key, decrypt)
                    text = dec.decode('utf-8').strip('\x00')
                    print(f"Расшифрованное: {text}")
                    print(f"Расшифрованное (BIN): {_format_binary(dec)}")
                except ValueError:
                    print("Ошибка: некорректный HEX-формат!")
        elif choice == "4":
            print("Программа завершена.")
            break
        else:
            print("Выберите действие 1–4.")


if __name__ == "__main__":
    main()
