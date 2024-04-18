import requests
import json
import re

# Ваш API ключ от Google Cloud
api_key = 'YOUR_API_KEY'

# ID канала YouTube
channel_id = 'UC-9-kyTW8ZkZNDHQJ6FgpwQ'

# Название плейлиста
playlist_name = 'Hans Zimmer'

# Функция для получения ID плейлиста по имени
def get_playlist_id(api_key, channel_id, playlist_name):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&q={playlist_name}&type=playlist&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        if 'items' in data and len(data['items']) > 0:
            return data['items'][0]['id']['playlistId']
    return None

# Функция для получения списка видео в плейлисте
def get_playlist_videos(api_key, playlist_id):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults=50&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        if 'items' in data:
            return data['items']
    return None

# Функция для получения длительности видео
def get_video_duration(video_id, api_key):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_id}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        if 'items' in data and len(data['items']) > 0:
            duration = data['items'][0]['contentDetails']['duration']
            # Преобразование ISO 8601 длительности в секунды
            return convert_iso8601_to_seconds(duration)
    return None

# Функция для преобразования длительности в формате ISO 8601 в секунды
def convert_iso8601_to_seconds(iso8601_duration):
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso8601_duration)
    if match:
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        seconds = int(match.group(3)) if match.group(3) else 0
        return hours * 3600 + minutes * 60 + seconds
    return 0

# Получаем ID плейлиста
playlist_id = get_playlist_id(api_key, channel_id, playlist_name)
if playlist_id:
    print(f"ID плейлиста: {playlist_id}")
    # Получаем список видео в плейлисте
    videos = get_playlist_videos(api_key, playlist_id)
    if videos:
        # Открываем файл для записи
        with open('times.txt', 'w') as file:
            for video in videos:
                video_id = video['snippet']['resourceId']['videoId']
                duration = get_video_duration(video_id, api_key)
                if duration:
                    # Записываем название видео и его длительность в файл
                    file.write(f"{video['snippet']['title']}: {duration} секунд\n")
                else:
                    print(f"Не удалось получить длительность для видео: {video['snippet']['title']}")
    else:
        print("Не удалось получить список видео")
else:
    print("Не удалось получить ID плейлиста")
