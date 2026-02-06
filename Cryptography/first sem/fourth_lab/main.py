# В симметричной криптосистеме секретный ключ передается по защищенному каналу
# Справочник
from vigenere import vigenere_menu
from wheatstone import double_square_menu


def main():
    """
    Главное меню программы
    """
    while True:
        print("\n" + "="*50)
        print("ЛАБОРАТОРНАЯ РАБОТА ПО КРИПТОГРАФИИ")
        print("="*50)
        print("1. Система Вижинера")
        print("2. Шифр 'Двойной квадрат' Уитстона")
        print("0. Выход")
        choice = input("\nВыберите задание: ").strip()
        
        if choice == "1":
            vigenere_menu()
        elif choice == "2":
            double_square_menu()
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор! Попробуйте снова.")


if __name__ == "__main__":
    main()
