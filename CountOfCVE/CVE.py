import pandas as pd
import glob
from concurrent.futures import ThreadPoolExecutor
import orjson
import zipfile
import os

# Установка настроек отображения для полного вывода данных
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def unzip_files(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(zip_file_path))

def read_file(filename):
    with open(filename, 'rb') as f:
        return orjson.loads(f.read())['CVE_Items']

# Разархивация всех .zip файлов в текущем каталоге
for zip_file in glob.glob('*.zip'):
    unzip_files(zip_file)

# Чтение и объединение данных из всех файлов с использованием многопоточности
with ThreadPoolExecutor() as ex:
    merged_data = [item for lst in ex.map(read_file, glob.glob('*.json')) for item in lst]

# Преобразование списка в DataFrame
data = pd.json_normalize(merged_data)

# Обработка и анализ данных
data['publishedDate'] = pd.to_datetime(data['publishedDate'])
cve_per_day = data.groupby(data['publishedDate'].dt.date).size()

# Вывод результата
print(cve_per_day)

summary_stats = cve_per_day.agg(['min', 'max', 'mean'])
date_with_max_cve = cve_per_day.idxmax()
date_with_min_cve = cve_per_day.idxmin()
print(summary_stats, date_with_max_cve, date_with_min_cve)
