import os


def count_seconds_from_file(file_path):
    """
    Считает общее количество секунд, указанных в файле.

    Параметры:
    file_path (str): Путь к файлу, содержащему временные отметки в формате 'минуты:секунды'.

    Возвращает:
    int: Общее количество секунд, указанных в файле.

    Исключения:
    FileNotFoundError: Если файл не найден.
    """
    # Проверяем, существует ли файл, и если нет, создаем его
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            pass  # Файл создается, но не выводится никакой информации
        print(f"Наполните файл times.txt данными")
        return []

    with open(file_path, 'r') as file:
        times_list = [minutes * 60 + seconds for line in file for minutes, seconds in
                      [map(int, line.strip().split(':'))]]
    return times_list


if __name__ == "__main__":
    # Автоматически узнаем адрес файла times.txt
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, 'times.txt')
    Data = count_seconds_from_file(file_path)
