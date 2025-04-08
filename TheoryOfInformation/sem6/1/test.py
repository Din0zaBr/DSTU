def text_to_binary(text):
    """Переводит текст в двоичную строку (ASCII)"""
    return ''.join(f"{ord(c):08b}" for c in text)

def binary_to_text(binary_str):
    """Переводит двоичную строку обратно в текст (ASCII)"""
    chars = []
    print(binary_str)
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i + 8]
        chars.append(chr(int(byte, 2)))
    print(chars)
    return ''.join(chars)

binary = text_to_binary(input())
print(binary)
print(binary_to_text(binary))
