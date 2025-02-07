import collections
import matplotlib.pyplot as plt


def build_histogram(text):
    # Разделение текста на кириллицу, латиницу и символы
    cyrillic_text = ''.join(c for c in text if 'А' <= c <= 'я' or c == 'Ё' or c == 'ё')
    latin_text = ''.join(c for c in text if 'A' <= c <= 'Z' or 'a' <= c <= 'z')
    symbols_text = ''.join(c for c in text if not (
            'А' <= c <= 'я' or c == 'Ё' or c == 'ё' or 'A' <= c <= 'Z' or 'a' <= c <= 'z') and c.isprintable())

    # Подсчет частоты каждого символа в каждом тексте
    cyrillic_frequency = collections.Counter(cyrillic_text)
    latin_frequency = collections.Counter(latin_text)
    symbols_frequency = collections.Counter(symbols_text)

    # Построение гистограмм
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    # Сортировка символов в алфавитном порядке
    cyrillic_frequency = dict(sorted(cyrillic_frequency.items()))
    latin_frequency = dict(sorted(latin_frequency.items()))
    symbols_frequency = dict(sorted(symbols_frequency.items()))

    axs[0].bar(cyrillic_frequency.keys(), cyrillic_frequency.values())
    axs[0].set_title('Гистограмма появления кириллицы')
    axs[0].set_xlabel('Символы')
    axs[0].set_ylabel('Частота')

    axs[1].bar(latin_frequency.keys(), latin_frequency.values())
    axs[1].set_title('Гистограмма появления латиницы')
    axs[1].set_xlabel('Символы')
    axs[1].set_ylabel('Частота')

    axs[2].bar(symbols_frequency.keys(), symbols_frequency.values())
    axs[2].set_title('Гистограмма появления всего остального')
    axs[2].set_xlabel('Символы')
    axs[2].set_ylabel('Частота')

    plt.tight_layout()
    plt.show()


def build_byte_histogram(data):
    # Подсчет частоты каждого байта в файле
    byte_frequency = collections.Counter(data)

    # Построение гистограммы
    plt.bar(byte_frequency.keys(), byte_frequency.values())
    plt.title('Гистограмма появления всех байт')
    plt.xlabel('Байты')
    plt.ylabel('Частота')
    plt.show()
