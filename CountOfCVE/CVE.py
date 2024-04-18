import requests
import json
import pandas as pd

# Ваш ключ API Genius
api_key = 'vHkykJyc-MRW_7tRxW2xa86E1KZjinHeE48YUwv3PgoW3H5g4ohy-bTNkuVC8SSW'

# URL API Genius для поиска песен Ханса Циммера
search_url = 'https://api.genius.com/search'

# Параметры запроса
params = {
    'q': 'Hans Zimmer songs',
    'access_token': api_key
}

# Отправляем запрос к API Genius
response = requests.get(search_url, params=params)


# Функция для преобразования строки с длительностью в секунды
def convert_duration_to_seconds(duration_str):
    """
    Преобразует строку с длительностью в секунды.

    :param duration_str: Строка с длительностью, например, "3:30".
    :return: Количество секунд.
    """
    minutes, seconds = map(int, duration_str.split(':'))
    return minutes * 60 + seconds


# Проверяем, что запрос был успешным
if response.status_code == 200:
    # Парсим JSON-ответ
    data = json.loads(response.text)

    # Извлекаем информацию о песнях
    songs = data['response']['hits']

    # Создаем список для хранения данных о песнях
    songs_data = []

    # Проходим по каждой песне и извлекаем название и длительность
    for song in songs:
        title = song['result']['title']
        # Получаем URL песни для дальнейшего запроса к API
        song_url = song['result']['url']

        # Отправляем запрос к API для получения деталей песни
        song_details_response = requests.get(song_url, params={'access_token': api_key})
        if song_details_response.status_code == 200:
            song_details = json.loads(song_details_response.text)
            # Извлекаем длительность песни
            duration_str = song_details['response']['song']['lyrics_state']
            # Преобразуем длительность в секунды
            duration_seconds = convert_duration_to_seconds(duration_str)
            # Добавляем данные в список
            songs_data.append([title, duration_seconds])

    # Преобразуем список в DataFrame для удобства работы
    df = pd.DataFrame(songs_data, columns=['Title', 'Duration'])

    # Выводим DataFrame
    print(df)
else:
    print("Ошибка при получении данных от API Genius")
