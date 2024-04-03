# Импортируем необходимые модули
import glob
import itertools
import os
import zipfile
from concurrent.futures import ThreadPoolExecutor

import orjson
import pandas as pd


def main():
    # Устанавливаем опции pandas для отображения большого количества строк и столбцов
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # Функция для распаковки и чтения JSON файлов из ZIP-архивов
    def unzip_and_read_file(zip_file_path):
        # Открываем ZIP-архив на чтение
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # Проходим по всем файлам в архиве
            for file in zip_ref.namelist():
                # Если файл имеет расширение .json, то читаем его
                if file.endswith('.json'):
                    with zip_ref.open(file) as f:
                        # Используем orjson для быстрого чтения JSON и извлечения данных
                        yield from orjson.loads(f.read())['CVE_Items']

    # Определяем количество ядер процессора для оптимизации параллелизма
    num_cores = os.cpu_count() or 4

    # Создаем пул потоков для параллельной обработки файлов
    with ThreadPoolExecutor(max_workers=min(num_cores, 8)) as ex:
        # Используем map для применения функции unzip_and_read_file к каждому ZIP-файлу
        # и получаем итератор по результатам
        merged_data_iterator = itertools.chain.from_iterable(ex.map(unzip_and_read_file, glob.glob('*.zip')))

    # Создаем DataFrame из объединенных данных без указания типов данных
    data = pd.DataFrame(merged_data_iterator)

    # Преобразуем столбец 'publishedDate' в формат datetime для дальнейшего анализа
    data['publishedDate'] = pd.to_datetime(data['publishedDate'])
    # Группируем данные по дате публикации и подсчитываем количество CVE для каждой даты
    cve_per_day = data.groupby(data['publishedDate'].dt.date).size()

    # # Выводим количество CVE для каждой даты
    # print("Number of CVEs per Day:")
    # for date, count in cve_per_day.items():
    #     # print(f"{date}: {count}")
    #     print(f"{count}", end=' ')  # для удобного копирования элементов

    # Вычисляем статистику для количества CVE: минимальное, максимальное и среднее значение
    summary_stats = cve_per_day.agg(['min', 'max', 'mean'])

    # Данные в файл
    # 1ую строку в файле можно удалить
    summary_stats.to_csv('summary_stats.csv')
    list = []
    for date, count in cve_per_day.items():
        list.append(count)
    print(list)

    # Сортируем данные по возрастанию
    cve_per_day_sorted = list.sort()

    # Создаем вариационный ряд
    variation_series = cve_per_day_sorted

    # Выводим вариационный ряд
    print("Вариационный ряд:")
    print(variation_series)

    # Сохраняем вариационный ряд в CSV-файл
    variation_series.to_csv("variation_series.csv", header=False, index=False)

    # Выводим сообщение об успешном сохранении
    print("Вариационный ряд сохранен в файл variation_series.csv")


if __name__ == "__main__":
    # Запускаем основную функцию
    main()