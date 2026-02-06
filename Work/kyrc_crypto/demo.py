"""
Демонстрационный модуль для работы с алгоритмами шифрования

Демонстрирует использование классов AES и ГОСТ 28147-89,
а также сравнительный анализ алгоритмов.
"""

from typing import Dict

from .aes_encryption import AESEncryption
from .gost28147 import GOST28147
from .base_encryption import BlockCipher
from .encryption_comparison import EncryptionComparison


def demo_encryption() -> None:
    """
    Демонстрация работы алгоритмов шифрования
    """
    print("\n" + "="*80)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ АЛГОРИТМОВ ШИФРОВАНИЯ")
    print("="*80)
    
    # Инициализация
    aes = AESEncryption(key_size=256)
    gost = GOST28147()
    
    # Тестовое сообщение
    test_message = "Привет, это тестовое сообщение для шифрования!".encode('utf-8')
    print(f"\nИсходное сообщение: {test_message.decode('utf-8')}")
    print(f"Размер сообщения: {len(test_message)} байт")
    
    # AES шифрование
    print("\n" + "-"*80)
    print("AES ШИФРОВАНИЕ:")
    print("-"*80)
    aes_key = aes.generate_key()
    print(f"Ключ AES (hex, первые 32 символа): {aes_key.hex()[:32]}...")
    
    aes_encrypted = aes.encrypt(test_message, aes_key)
    print(f"Зашифрованное сообщение (hex, первые 64 символа): {aes_encrypted.hex()[:64]}...")
    print(f"Размер зашифрованного сообщения: {len(aes_encrypted)} байт")
    
    aes_decrypted = aes.decrypt(aes_encrypted, aes_key)
    print(f"Расшифрованное сообщение: {aes_decrypted.decode('utf-8')}")
    print(f"Корректность расшифрования: {aes_decrypted == test_message}")
    
    # ГОСТ шифрование
    print("\n" + "-"*80)
    print("ГОСТ 28147-89 (МАГМА) ШИФРОВАНИЕ:")
    print("-"*80)
    gost_key = gost.generate_key()
    print(f"Ключ ГОСТ (hex, первые 32 символа): {gost_key.hex()[:32]}...")
    
    gost_encrypted = gost.encrypt(test_message, gost_key)
    print(f"Зашифрованное сообщение (hex, первые 64 символа): {gost_encrypted.hex()[:64]}...")
    print(f"Размер зашифрованного сообщения: {len(gost_encrypted)} байт")
    
    gost_decrypted = gost.decrypt(gost_encrypted, gost_key)
    print(f"Расшифрованное сообщение: {gost_decrypted.decode('utf-8')}")
    print(f"Корректность расшифрования: {gost_decrypted == test_message}")
    
    print("\n" + "="*80)


def demo_comparison() -> None:
    """
    Демонстрация сравнительного анализа алгоритмов
    """
    # Инициализация алгоритмов
    aes = AESEncryption(key_size=256)
    gost = GOST28147()
    
    # Создание словаря алгоритмов
    algorithms: Dict[str, BlockCipher] = {
        'AES': aes,
        'ГОСТ (Магма)': gost,
    }
    
    # Создание объекта сравнения
    comparison = EncryptionComparison(algorithms=algorithms)
    
    # Вывод сравнительного анализа
    comparison.print_comparison()


def demo_extensibility() -> None:
    """
    Демонстрация расширяемости системы сравнения
    
    Показывает, как можно добавить новые методы сравнения
    """
    print("\n" + "="*80)
    print("ДЕМОНСТРАЦИЯ РАСШИРЯЕМОСТИ СИСТЕМЫ СРАВНЕНИЯ")
    print("="*80)
    
    # Инициализация алгоритмов
    aes = AESEncryption(key_size=256)
    gost = GOST28147()
    
    algorithms: Dict[str, BlockCipher] = {
        'AES': aes,
        'ГОСТ (Магма)': gost,
    }
    
    # Создание объекта сравнения
    comparison = EncryptionComparison(algorithms=algorithms)
    
    # Показываем доступные методы
    print("\nДоступные методы сравнения:")
    for method_name in comparison.get_available_methods():
        print(f"  - {method_name}")
    
    # Добавляем заготовки для новых методов
    from .comparison_methods import MemoryUsageComparison, KeySizeComparison
    
    print("\nДобавление новых методов сравнения...")
    comparison.register_method(MemoryUsageComparison())
    comparison.register_method(KeySizeComparison())
    
    print("\nОбновленный список методов сравнения:")
    for method_name in comparison.get_available_methods():
        print(f"  - {method_name}")
    
    print("\n" + "="*80)


def main() -> None:
    """
    Главная функция для запуска всех демонстраций
    """
    # Демонстрация шифрования
    demo_encryption()
    
    # Демонстрация сравнения
    demo_comparison()
    
    # Демонстрация расширяемости
    demo_extensibility()


if __name__ == "__main__":
    main()

