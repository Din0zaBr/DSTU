import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL страницы с песнями Ханса Циммера
url = "https://genius.com/artists/Hans-zimmer/songs"

# Отправляем запрос на страницу
response = requests.get(url)

# Проверяем, что запрос был успешным
if response.status_code == 200:
    # Парсим HTML-страницу
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все элементы с названиями песен и их длительностью
    songs = soup.find_all('div', class_='song_title')
    durations = soup.find_all('span', class_='song_info_duration')

    # Создаем список для хранения данных о песнях
    songs_data = []

    # Проходим по каждой песне и извлекаем название и длительность
    for song, duration in zip(songs, durations):
        title = song.text.strip()
        duration_text = duration.text.strip()
        # Добавляем данные в список
        songs_data.append([title, duration_text])

    # Преобразуем список в DataFrame для удобства работы
    df = pd.DataFrame(songs_data, columns=['Title', 'Duration'])

    # Выводим DataFrame
    print(df)
else:
    print("Ошибка при получении страницы")
