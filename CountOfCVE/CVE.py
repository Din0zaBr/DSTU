def count_seconds_from_file(file_path):
    total_seconds = 0
    with open(file_path, 'r') as file:
        for line in file:
            minutes, seconds = map(int, line.strip().split(':'))
            total_seconds += minutes * 60 + seconds
    return total_seconds


# Замените 'times.txt' на путь к вашему файлу, если он отличается
file_path = 'times.txt'
total_seconds = count_seconds_from_file(file_path)
print(f"Общее количество секунд: {total_seconds}")
