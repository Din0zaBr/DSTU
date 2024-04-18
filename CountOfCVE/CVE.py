import os


def count_seconds_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
        return []

    seconds_list = []
    with open(file_path, 'r') as file:
        for line in file:
            minutes, seconds = map(int, line.strip().split(':'))
            total_seconds = minutes * 60 + seconds
            seconds_list.append(total_seconds)
    return seconds_list


# Замените 'times.txt' на путь к вашему файлу, если он отличается
file_path = 'times.txt'
seconds_list = count_seconds_from_file(file_path)
print(f"Список секунд: {seconds_list}")
