import struct
import random
import os

KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "key.txt")

S_BOX = [
    [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
    [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
    [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
    [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
    [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
    [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 14, 15, 12],
    [13, 11, 4, 10, 7, 2, 1, 5, 0, 8, 15, 14, 9, 3, 12, 6],
    [1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2]
]


def s_block(value):
    result = []
    binary_value = f"{value:032b}" # Число превращается в двоичную строку длиной 32 символа (с ведущими нулями)
    for i in range(8):
        search_id = int(binary_value[i * 4: (i + 1) * 4], 2)
        result.append(f"{S_BOX[i][search_id]:04b}")
    return int("".join(result), 2) # , 2 - бинарный вид


def encrypt(block, key):
    block = block.ljust(8, b'\x00')
    N1, N2 = struct.unpack('<II', block)
    for i in range(32):
        print("=" * 40)
        print(f"Раунд {i + 1}. До ключа: L = {N1:08X} ({N1:032b}), R = {N2:08X} ({N2:032b})")
        if i < 24:
            under_key_number = i % 8
        else:
            under_key_number = (32 - i - 1) % 8
        Ki = key[under_key_number]
        S_sum = (N1 + Ki) % (2 ** 32)
        S_block_out = s_block(S_sum)
        S = ((S_block_out << 11) | (S_block_out >> 21)) % (2 ** 32)
        N1, N2 = N2 ^ S, N1
        print(f"Ключ = {Ki:08X} ({Ki:032b})")
        print(f"Сложение с ключом = {S_sum:08X} ({S_sum:032b})")
        print(f"После S-блока = {S_block_out:08X} ({S_block_out:032b})")
        print(f"После сдвига на 11 = {S:08X} ({S:032b})")
        print(f"После XOR: L = {N1:08X} ({N1:032b}), R = {N2:08X} ({N2:032b})")
    return struct.pack('<II', N2, N1)


def decrypt(block, key):
    block = block.ljust(8, b'\x00')
    N1, N2 = struct.unpack('<II', block)
    for i in reversed(range(32)):
        print("=" * 40)
        print(f"Раунд {32 - i}. До ключа: L = {N1:08X} ({N1:032b}), R = {N2:08X} ({N2:032b})")
        under_key_number = i % 8 if i < 24 else (32 - i - 1) % 8
        Ki = key[under_key_number]
        S_sum = (N1 + Ki) % (2 ** 32)
        S_block_out = s_block(S_sum)
        S = ((S_block_out << 11) | (S_block_out >> 21)) % (2 ** 32)
        N1, N2 = N2 ^ S, N1
        print("=" * 40)
        print(f"Ключ = {Ki:08X} ({Ki:032b})")
        print(f"Сложение с ключом = {S_sum:08X} ({S_sum:032b})")
        print(f"После S-блока = {S_block_out:08X} ({S_block_out:032b})")
        print(f"После сдвига на 11 = {S:08X} ({S:032b})")
        print(f"После XOR: L = {N1:08X} ({N1:032b}), R = {N2:08X} ({N2:032b})")
    return struct.pack('<II', N2, N1)


def pad_message(message):
    encoded = message.encode('utf-8')
    block_size = ((len(encoded) + 7) // 8) * 8
    # Вычисляет ближайшую длину блока, кратную 8, не меньшую, чем len(encoded)
    return encoded.ljust(block_size, b'\x00')


def generate_key():
    key = [random.randint(0, 0xFFFFFFFF) for _ in range(8)]
    # Такое число занимает 32 бита и соответствует одному 32-битному элементу ключа в шифре.
    key_hex = ''.join(f"{k:08X}" for k in key)
    # 08 — вывести число в поле шириной 8 символов, недостающие слева заполнить нулями;
    # X — выводить в верхнем регистре шестнадцатеричной системы (0–9, A–F).
    with open(KEY_FILE, "w") as f:
        f.write(key_hex)
    print(f"Ключ сгенерирован и сохранен в файл: {key_hex}")
    return key


def load_key():
    if not os.path.exists(KEY_FILE):
        print("Файл с ключом не найден! Сначала сгенерируйте ключ.")
        return None
    with open(KEY_FILE, "r") as f:
        key_str = f.read().strip()
    return process_key(key_str)


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


def main():
    while True:
        print("\n" + "=" * 40)
        print("1. -  Сгенерировать ключ и сохранить его в файл")
        print("2. -  Зашифровать текст")
        print("3. -  Расшифровать текст ")
        print("4. -  Выйти")
        print("=" * 40)
        choice = input("Введите команду:   ")
        if choice == "1":
            generate_key()
        elif choice in ["2", "3"]:
            key_str = input("Введите ключ (64 HEX-символа) или Enter для загрузки из файла: ").strip()
            if not key_str:
                key = load_key()
            else:
                key = process_key(key_str)
            if not key:
                continue
            if choice == "2":
                message = input("Введите сообщение: ")
                padded_message = pad_message(message)
                encrypted_blocks = [encrypt(padded_message[i:i + 8], key) for i in range(0, len(padded_message), 8)]
                # Сообщение делится на куски по 8 байт, каждый кусок шифруется отдельно,
                # а результаты складываются в список encrypted_blocks.
                encrypted_message = b''.join(encrypted_blocks)
                print(f"Зашифрованное сообщение (HEX): {encrypted_message.hex()}")
                binary_str = ' '.join(f"{b:08b}" for b in encrypted_message)
                print(f"Зашифрованное сообщение (BIN): {binary_str}")
            elif choice == "3":
                encrypted_hex = input("Введите зашифрованное сообщение (HEX): ")
                try:
                    encrypted_message = bytes.fromhex(encrypted_hex)
                    encrypted_blocks = [encrypted_message[i:i + 8] for i in range(0, len(encrypted_message), 8)]
                    decrypted_blocks = [decrypt(block, key) for block in encrypted_blocks]
                    decrypted_raw = b''.join(decrypted_blocks)
                    decrypted_message = decrypted_raw.decode('utf-8').strip('\x00')
                    print(f"Расшифрованное сообщение: {decrypted_message}")
                    binary_str = ' '.join(f"{b:08b}" for b in decrypted_raw)
                    print(f"Расшифрованное сообщение (BIN): {binary_str}")
                except ValueError:
                    print("Ошибка: некорректный формат зашифрованного текста!")
        elif choice == "4":
            print("Программа завершена.")
            break
        else:
            print("Ошибка: выберите корректный номер действия!")


if __name__ == "__main__":
    main()
