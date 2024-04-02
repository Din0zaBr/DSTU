import glob
import os
import zipfile
from concurrent.futures import ThreadPoolExecutor

import orjson
import pandas as pd

# Установка настроек отображения для полного вывода данных
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def unzip_and_read_file(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith('.json'):
                with zip_ref.open(file) as f:
                    return orjson.loads(f.read())['CVE_Items']


# Определение количества ядер процессора для оптимизации параллельной обработки
num_cores = os.cpu_count() or 4

# Разархивация всех .zip файлов в текущем каталоге и чтение данных
with ThreadPoolExecutor(max_workers=num_cores) as ex:
    merged_data = [item for lst in ex.map(unzip_and_read_file, glob.glob('*.zip')) for item in lst]

# Преобразование списка в DataFrame
data = pd.DataFrame(merged_data)

# Обработка и анализ данных
data['publishedDate'] = pd.to_datetime(data['publishedDate'])
cve_per_day = data.groupby(data['publishedDate'].dt.date).size()

# Вывод результата
print("Number of CVEs per Day:")
for date, count in cve_per_day.items():
    # print(f"{date}: {count}")
    print(f"{count}", end=' ')  # для будущей печати
    print()

summary_stats = cve_per_day.agg(['min', 'max', 'mean'])
date_with_max_cve = cve_per_day.idxmax()
date_with_min_cve = cve_per_day.idxmin()
print(summary_stats, date_with_max_cve, date_with_min_cve)
