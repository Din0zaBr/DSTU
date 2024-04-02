import cProfile
import glob
import os
import zipfile
from concurrent.futures import ThreadPoolExecutor

import orjson
import pandas as pd


def main():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    def unzip_and_read_file(zip_file_path):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith('.json'):
                    with zip_ref.open(file) as f:
                        yield from orjson.loads(f.read())['CVE_Items']

    num_cores = os.cpu_count() or 4

    with ThreadPoolExecutor(max_workers=min(num_cores, 8)) as ex:
        merged_data = [item for lst in ex.map(unzip_and_read_file, glob.glob('*.zip')) for item in lst]

    # Создаем DataFrame без указания типов данных
    data = pd.DataFrame(merged_data)

    # Теперь мы можем изменить типы данных столбцов
    # Например, если у нас есть столбец 'column_name', мы можем изменить его тип данных на 'category'
    # data['column_name'] = data['column_name'].astype('category')

    # Обработка и анализ данных
    data['publishedDate'] = pd.to_datetime(data['publishedDate'])
    cve_per_day = data.groupby(data['publishedDate'].dt.date).size()

    print("Number of CVEs per Day:")
    for date, count in cve_per_day.items():
        # print(f"{date}: {count}")
        print(f"{count}", end=' ')  # для удобного копирования элементов
        print()

    summary_stats = cve_per_day.agg(['min', 'max', 'mean'])

    # Данные в файл
    summary_stats.to_csv('summary_stats.csv')


if __name__ == "__main__":
    main()
