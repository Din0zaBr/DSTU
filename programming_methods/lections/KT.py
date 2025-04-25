"""
27.   Плейлист
       Песни играют в порядке добавления. Реализуйте систему воспроизведения.
"""

from collections import deque


class Playlist:
    def __init__(self):
        self.queue = deque()

    def add_song(self, song):
        """Добавляет песню в плейлист."""
        self.queue.append(song)
        print(f"Добавлена песня: {song}")
        print()

    def play_next(self):
        """Воспроизводит следующую песню в плейлисте."""
        if self.queue:
            song = self.queue.popleft()
            print(f"Воспроизводится: {song}")
            print()
        else:
            print("Плейлист пуст.")

    def show_playlist(self):
        """Показывает текущий плейлист."""
        print("Текущий плейлист:")
        for song in self.queue:
            print(song)
        print()


def main():
    playlist = Playlist()
    playlist.add_song("'Bohemian Rhapsody' - Queen")
    playlist.add_song("'Stairway to Heaven' - Led Zeppelin")
    playlist.add_song("'Imagine' - John Lennon")
    playlist.add_song("'Billie Jean' - Michael Jackson")
    playlist.add_song("'Hotel California' - Eagles")
    playlist.add_song("'Smells Like Teen Spirit' - Nirvana")

    playlist.show_playlist()
    playlist.play_next()
    playlist.play_next()
    playlist.show_playlist()
    playlist.play_next()
    playlist.play_next()


if __name__ == "__main__":
    main()
