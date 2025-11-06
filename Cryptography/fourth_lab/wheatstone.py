"""
ШИФР «ДВОЙНОЙ КВАДРАТ» УИТСТОНА

Модуль для шифрования и расшифрования текста с использованием шифра "Двойной квадрат" Уитстона.
Шифр Уитстона использует две таблицы для преобразования биграмм текста.
"""

import re
from itertools import product
from typing import List, Tuple, Optional

# Левая таблица 7x5
left_table = [
    ['Ж', 'Щ', 'Н', 'Ю', 'Р'],
    ['И', 'Т', 'Ь', 'Ц', 'Б'],
    ['Я', 'М', 'Е', '.', 'С'],
    ['В', 'Ы', 'П', 'Ч', ' '],
    [':', 'Д', 'У', 'О', 'К'],
    ['З', 'Э', 'Ф', 'Г', 'Ш'],
    ['Ч', 'А', ',', 'Л', 'Ъ']
]

# Правая таблица 7x5
right_table = [
    ['И', 'Ч', 'Г', 'Я', 'Т'],
    [',', 'Ж', 'Ь', 'М', 'О'],
    ['З', 'Ю', 'Р', 'В', 'Щ'],
    ['Ц', ':', 'П', 'Е', 'Л'],
    ['Ъ', 'А', 'Н', '.', 'Х'],
    ['Э', 'К', 'С', 'Ш', 'Д'],
    ['Б', 'Ф', 'У', 'Ы', ' ']
]


def prepare_text_double_square(text: str) -> str:
    """
    Подготовка текста для двойного квадрата: сохраняем знаки препинания из таблиц и пробелы
    
    Args:
        text: Исходный текст (str)
    
    Returns:
        Подготовленный текст: только буквы, знаки препинания (.,:) и пробелы (str)
    """
    text = text.upper().replace('Ё', 'Е').replace('Й', 'И')
    return re.sub(r'[^А-Я.,: ]', '', text)


def get_cell(table: List[List[str]], row: int, col: int) -> str:
    """
    Получение символа из таблицы с проверкой границ
    
    Args:
        table: Таблица (список списков строк)
        row: Номер строки (int)
        col: Номер столбца (int)
    
    Returns:
        Символ из таблицы или пустая строка, если координаты вне границ (str)
    """
    if 0 <= row < len(table) and 0 <= col < len(table[row]):
        return table[row][col]
    return ''


def find_all_positions(table: List[List[str]], char: str) -> List[Tuple[int, int]]:
    """
    Находит все позиции символа в таблице
    
    Args:
        table: Таблица (список списков строк)
        char: Искомый символ (str)
    
    Returns:
        Список кортежей (строка, столбец) всех позиций символа (List[Tuple[int, int]])
    """
    positions = []
    for i, row in enumerate(table):
        for j, cell in enumerate(row):
            if cell == char:
                positions.append((i, j))
    return positions


def get_bigram_result(left_table: List[List[str]], right_table: List[List[str]], 
                     pos1: Tuple[int, int], pos2: Tuple[int, int], encrypt: bool = True) -> str:
    """
    Вычисляет результат биграммы для заданных позиций по алгоритму двойного квадрата
    
    Алгоритм:
    - Если буквы в одной строке: первая буква результата из правой таблицы (та же строка, столбец первой буквы),
      вторая из левой таблицы (та же строка, столбец второй буквы)
    - Если буквы в разных строках: строим прямоугольник, берем противоположные вершины
    
    Args:
        left_table: Левая таблица (List[List[str]])
        right_table: Правая таблица (List[List[str]])
        pos1: Позиция первой буквы (строка, столбец) (Tuple[int, int])
        pos2: Позиция второй буквы (строка, столбец) (Tuple[int, int])
        encrypt: True для шифрования, False для расшифрования (bool, по умолчанию True)
    
    Returns:
        Результат биграммы (две буквы) (str)
    """
    row1, col1 = pos1
    row2, col2 = pos2
    
    if row1 == row2:
        # Буквы в одной строке
        if encrypt:
            return get_cell(right_table, row2, col1) + get_cell(left_table, row1, col2)
        else:
            return get_cell(left_table, row1, col1) + get_cell(right_table, row2, col2)
    else:
        # Буквы в разных строках - прямоугольник
        if encrypt:
            return get_cell(right_table, row1, col2) + get_cell(left_table, row2, col1)
        else:
            return get_cell(left_table, row1, col2) + get_cell(right_table, row2, col1)


def get_all_bigram_variants(left_table: List[List[str]], right_table: List[List[str]], 
                           bigram: Tuple[str, str], encrypt: bool = True) -> List[str]:
    """
    Возвращает все возможные варианты расшифрования/шифрования биграммы
    
    Args:
        left_table: Левая таблица (List[List[str]])
        right_table: Правая таблица (List[List[str]])
        bigram: Биграмма (две буквы) (Tuple[str, str])
        encrypt: True для шифрования, False для расшифрования (bool, по умолчанию True)
    
    Returns:
        Список всех возможных вариантов результата (List[str])
    """
    letter1, letter2 = bigram
    
    if encrypt:
        pos1_all = find_all_positions(left_table, letter1)
        pos2_all = find_all_positions(right_table, letter2)
    else:
        pos1_all = find_all_positions(right_table, letter1)
        pos2_all = find_all_positions(left_table, letter2)
    
    if not pos1_all or not pos2_all:
        return [letter1 + letter2]
    
    variants = []
    for p1 in pos1_all:
        for p2 in pos2_all:
            result = get_bigram_result(left_table, right_table, p1, p2, encrypt)
            if result[0] and result[1]:  # Обе буквы не пустые
                variants.append(result)
    
    return variants if variants else [letter1 + letter2]


def process_bigram_double_square(left_table: List[List[str]], right_table: List[List[str]], 
                                bigram: Tuple[str, str], encrypt: bool = True, verbose: bool = False) -> str:
    """
    Универсальная функция для шифрования/расшифрования биграммы методом двойного квадрата
    
    Args:
        left_table: Левая таблица (List[List[str]])
        right_table: Правая таблица (List[List[str]])
        bigram: Биграмма (две буквы) (Tuple[str, str])
        encrypt: True для шифрования, False для расшифрования (bool, по умолчанию True)
        verbose: Выводить ли дополнительную информацию (bool, по умолчанию False)
    
    Returns:
        Результат обработки биграммы (две буквы) (str)
    """
    letter1, letter2 = bigram
    
    if encrypt:
        pos1_all = find_all_positions(left_table, letter1)
        pos2_all = find_all_positions(right_table, letter2)
    else:
        pos1_all = find_all_positions(right_table, letter1)
        pos2_all = find_all_positions(left_table, letter2)
    
    if not pos1_all or not pos2_all:
        return letter1 + letter2
    
    # Собираем все возможные комбинации
    all_results = []
    for p1 in pos1_all:
        for p2 in pos2_all:
            result = get_bigram_result(left_table, right_table, p1, p2, encrypt)
            if result[0] and result[1]:
                all_results.append(result)
    
    # Вывод информации только при расшифровании
    if verbose and not encrypt:
        variants_count = len(pos1_all) * len(pos2_all)
        if variants_count > 1:
            print(f"Биграмма '{letter1}{letter2}': {variants_count} вариантов")
    
    return all_results[0] if all_results else get_bigram_result(left_table, right_table, pos1_all[0], pos2_all[0], encrypt)


def encrypt_bigram_double_square(left_table: List[List[str]], right_table: List[List[str]], 
                                 bigram: Tuple[str, str]) -> str:
    """
    Шифрование биграммы методом двойного квадрата
    
    Args:
        left_table: Левая таблица (List[List[str]])
        right_table: Правая таблица (List[List[str]])
        bigram: Биграмма для шифрования (Tuple[str, str])
    
    Returns:
        Зашифрованная биграмма (str)
    """
    return process_bigram_double_square(left_table, right_table, bigram, encrypt=True)


def decrypt_bigram_double_square(left_table: List[List[str]], right_table: List[List[str]], 
                                 bigram: Tuple[str, str], verbose: bool = False) -> str:
    """
    Расшифрование биграммы методом двойного квадрата
    
    Args:
        left_table: Левая таблица (List[List[str]])
        right_table: Правая таблица (List[List[str]])
        bigram: Биграмма для расшифрования (Tuple[str, str])
        verbose: Выводить ли информацию о вариантах (bool, по умолчанию False)
    
    Returns:
        Расшифрованная биграмма (str)
    """
    return process_bigram_double_square(left_table, right_table, bigram, encrypt=False, verbose=verbose)


def split_into_bigrams_double_square(text: str) -> List[Tuple[str, str]]:
    """
    Разбиение текста на биграммы для двойного квадрата
    
    Args:
        text: Исходный текст (str)
    
    Returns:
        Список биграмм (кортежей из двух символов) (List[Tuple[str, str]])
    """
    bigrams = []
    for i in range(0, len(text) - 1, 2):
        bigrams.append((text[i], text[i + 1]))
    if len(text) % 2 == 1:
        bigrams.append((text[-1], 'Ъ'))
    return bigrams


def encrypt_double_square(text: str, left_table: List[List[str]], right_table: List[List[str]]) -> str:
    """
    Шифрование текста методом двойного квадрата
    
    Args:
        text: Исходный текст для шифрования (str)
        left_table: Левая таблица (List[List[str]])
        right_table: Правая таблица (List[List[str]])
    
    Returns:
        Зашифрованный текст (str)
    """
    prepared_text = prepare_text_double_square(text)
    bigrams = split_into_bigrams_double_square(prepared_text)
    return ''.join(encrypt_bigram_double_square(left_table, right_table, bg) for bg in bigrams)


def decrypt_double_square(ciphertext: str, left_table: List[List[str]], right_table: List[List[str]], 
                          verbose: bool = False) -> Tuple[str, List[str]]:
    """
    Расшифрование текста методом двойного квадрата
    
    Генерирует все возможные варианты расшифрования, если символы встречаются
    в таблицах несколько раз (неоднозначность расшифрования).
    
    Args:
        ciphertext: Зашифрованный текст (str)
        left_table: Левая таблица (List[List[str]])
        right_table: Правая таблица (List[List[str]])
        verbose: Выводить ли информацию о вариантах (bool, по умолчанию False)
    
    Returns:
        Кортеж: (основной результат расшифрования, список всех возможных вариантов) (Tuple[str, List[str]])
    """
    prepared_text = prepare_text_double_square(ciphertext)
    bigrams = split_into_bigrams_double_square(prepared_text)
    
    # Получаем все варианты для каждой биграммы (если символы встречаются несколько раз)
    bigram_variants = [get_all_bigram_variants(left_table, right_table, bg, encrypt=False) for bg in bigrams]
    
    # Генерируем все возможные комбинации вариантов из всех биграмм
    all_variants = [''.join(combo) for combo in product(*bigram_variants)]
    
    # Основной результат (первый вариант каждой биграммы)
    result = ''.join(decrypt_bigram_double_square(left_table, right_table, bg, verbose=verbose) for bg in bigrams)
    
    # Убираем дубликаты и сортируем
    unique_variants = sorted(set(all_variants))
    
    return result, unique_variants


def print_tables() -> None:
    """
    Печать обеих таблиц
    
    Returns:
        None
    """
    for name, table in [("Левая таблица", left_table), ("Правая таблица", right_table)]:
        print(f"\n{name}:")
        for i, row in enumerate(table):
            print(f"{i + 1}: | {' | '.join(cell if cell else ' ' for cell in row)} |")
    print()


def print_result(title: str, original: str, result: str, variants: Optional[List[str]] = None) -> None:
    """
    Вывод результата шифрования/расшифрования
    
    Args:
        title: Заголовок результата (str)
        original: Исходный текст (str)
        result: Результат обработки (str)
        variants: Список всех возможных вариантов (Optional[List[str]], по умолчанию None)
    
    Returns:
        None
    """
    print(f"\n{title}")
    print(f"Исходный текст: {original}")
    if variants:
        print(f"Всего вариантов: {len(variants)}")
        for i, variant in enumerate(variants, 1):
            print(f"  {i}. {variant}")
    else:
        print(f"Результат: {result}")


def encrypt_double_square_menu():
    """
    Независимая функция шифрования двойного квадрата
    
    Запрашивает у пользователя текст и шифрует его методом двойного квадрата Уитстона.
    """
    plaintext = input("\nВведите текст для шифрования: ")
    print_tables()
    ciphertext = encrypt_double_square(plaintext, left_table, right_table)
    print_result("РЕЗУЛЬТАТ ШИФРОВАНИЯ", plaintext, ciphertext)


def decrypt_double_square_menu():
    """
    Независимая функция расшифрования двойного квадрата
    
    Запрашивает у пользователя шифртекст и расшифровывает его методом двойного квадрата Уитстона.
    """
    ciphertext = input("\nВведите текст для расшифрования: ")
    print_tables()
    _, variants = decrypt_double_square(ciphertext, left_table, right_table, verbose=True)
    print_result("РЕЗУЛЬТАТ РАСШИФРОВАНИЯ", ciphertext, "", variants)


def double_square_menu():
    """
    Меню для шифра "Двойной квадрат" Уитстона
    
    Предоставляет пользователю выбор между шифрованием и расшифрованием.
    """
    print("\n=== ШИФР 'ДВОЙНОЙ КВАДРАТ' УИТСТОНА ===")
    print("1. Зашифровать")
    print("2. Расшифровать")
    print("0. Назад")
    choice = input("Выбор: ").strip()
    
    if choice == "1":
        encrypt_double_square_menu()
    elif choice == "2":
        decrypt_double_square_menu()
    elif choice == "0":
        return
    else:
        print("Неверный выбор!")

