import wave
import numpy as np
import matplotlib.pyplot as plt
import struct
import random
from typing import Tuple, List


class WavPCMProcessor:
    """Класс для обработки WAV файлов с тремя уровнями искажений"""

    def __init__(self):
        self.sample_width = 2
        self.sample_rate = 44100
        self.channels = 1

    def load_wav(self, filename: str) -> Tuple[np.ndarray, dict]:
        """Загрузка WAV файла"""
        with wave.open(filename, 'rb') as wav_file:
            self.sample_rate = wav_file.getframerate()
            self.channels = wav_file.getnchannels()
            self.sample_width = wav_file.getsampwidth()

            frames = wav_file.readframes(wav_file.getnframes())
            fmt = f'{len(frames) // self.sample_width}h' if self.sample_width == 2 else f'{len(frames)}B'
            pcm_data = np.array(struct.unpack(fmt, frames))

            return pcm_data, {
                'sample_rate': self.sample_rate,
                'channels': self.channels,
                'sample_width': self.sample_width,
                'duration': wav_file.getnframes() / self.sample_rate
            }

    def save_wav(self, pcm_data: np.ndarray, filename: str):
        """Сохранение WAV файла"""
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(self.sample_width)
            wav_file.setframerate(self.sample_rate)
            fmt = f'{len(pcm_data)}h' if self.sample_width == 2 else f'{len(pcm_data)}B'
            wav_file.writeframes(struct.pack(fmt, *pcm_data))

    def _binary_to_pcm(self, binary_data: bytes) -> np.ndarray:
        """Конвертация бинарных данных в PCM массив"""
        fmt = f'{len(binary_data) // self.sample_width}h' if self.sample_width == 2 else f'{len(binary_data)}B'
        return np.array(struct.unpack(fmt, binary_data))

    def _pcm_to_binary(self, pcm_data: np.ndarray) -> bytes:
        """Конвертация PCM массива в бинарные данные"""
        fmt = f'{len(pcm_data)}h' if self.sample_width == 2 else f'{len(pcm_data)}B'
        return struct.pack(fmt, *pcm_data)

    def subtle_distortion(self, binary_data: bytes) -> bytes:
        """Практически незаметные искажения (уровень 1)"""
        corrupted = bytearray(binary_data)

        # 1. Инверсия младшего бита у 1% семплов
        for i in random.sample(range(len(corrupted)), k=len(corrupted) // 100):
            corrupted[i] ^= 0b00000001

        # 2. Незначительное изменение нулевых байтов
        for i in range(len(corrupted)):
            if corrupted[i] == 0x00 and random.random() < 0.01:
                corrupted[i] = 0x01

        return bytes(corrupted)

    def noticeable_distortion(self, binary_data: bytes) -> bytes:
        """Заметные, но терпимые искажения (уровень 2)"""
        corrupted = bytearray(binary_data)

        # 1. Инверсия 2 младших битов у 5% семплов
        for i in random.sample(range(len(corrupted)), k=len(corrupted) // 20):
            corrupted[i] ^= 0b00000011

        # 2. Замена каждого 100-го байта на случайный (0-255)
        for i in range(0, len(corrupted), 100):
            corrupted[i] = random.randint(0, 255)

        # 3. Добавление щелчков в тихие участки
        quiet_zones = [i for i, val in enumerate(corrupted) if val < 10]
        for i in random.sample(quiet_zones, k=min(50, len(quiet_zones))):
            corrupted[i] = 120 if random.random() > 0.5 else 130  # Оба значения в допустимом диапазоне

        return bytes(corrupted)

    def extreme_distortion(self, binary_data: bytes) -> bytes:
        """Крайне заметные искажения (уровень 3)"""
        corrupted = bytearray(binary_data)

        # 1. Полная инверсия каждого 10-го байта
        for i in range(0, len(corrupted), 10):
            corrupted[i] = (~corrupted[i]) & 0xFF  # Обеспечиваем диапазон 0-255

        # 2. Замена 10% байтов на максимальные значения (0xFF или 0x00)
        for i in random.sample(range(len(corrupted)), k=len(corrupted) // 10):
            corrupted[i] = 0xFF if random.random() > 0.5 else 0x00

        # 3. Добавление периодических громких щелчков
        for i in range(0, len(corrupted), len(corrupted) // 20):
            if i + 1 < len(corrupted):
                corrupted[i] = 0x7F
                corrupted[i + 1] = 0xFF

        # 4. Замена тишины на шум (исправлено)
        for i in range(len(corrupted)):
            if corrupted[i] < 5:
                corrupted[i] = random.randint(50, 100)  # Только положительные значения

        return bytes(corrupted)

    def process_with_distortion(self, input_file: str, output_file: str, level: int = 1):
        """Обработка файла с выбранным уровнем искажений"""
        # Загрузка данных
        pcm_data, meta = self.load_wav(input_file)
        binary_data = self._pcm_to_binary(pcm_data)

        # Применение искажений
        if level == 1:
            corrupted_binary = self.subtle_distortion(binary_data)
        elif level == 2:
            corrupted_binary = self.noticeable_distortion(binary_data)
        else:
            corrupted_binary = self.extreme_distortion(binary_data)

        corrupted_pcm = self._binary_to_pcm(corrupted_binary)

        # Сохранение и визуализация
        self.save_wav(corrupted_pcm, output_file)
        self._visualize_distortion(pcm_data, corrupted_pcm, meta['sample_rate'], level)

        return corrupted_pcm

    def _visualize_distortion(self, original: np.ndarray, corrupted: np.ndarray,
                              sample_rate: int, level: int):
        """Визуализация искажений"""
        plt.figure(figsize=(15, 10))
        samples_to_show = min(1000, len(original))

        # Выбираем характерный участок
        start = len(original) // 4

        # 1. Временная область
        plt.subplot(2, 1, 1)
        plt.plot(original[start:start + samples_to_show], 'b', label='Original', alpha=0.7)
        plt.plot(corrupted[start:start + samples_to_show], 'r', label='Corrupted', alpha=0.7)
        plt.title(f'PCM Waveform (Distortion Level {level})')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.grid(True)

        # 2. Спектральная область
        plt.subplot(2, 1, 2)
        freqs = np.fft.rfftfreq(len(original), 1 / sample_rate)
        plt.semilogy(freqs, np.abs(np.fft.rfft(original)), 'b', label='Original')
        plt.semilogy(freqs, np.abs(np.fft.rfft(corrupted)), 'r', label='Corrupted', alpha=0.7)
        plt.title('Frequency Spectrum Comparison')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude (log)')
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    processor = WavPCMProcessor()

    # Примеры использования:
    print("1. Создание практически незаметных искажений...")
    processor.process_with_distortion(
        input_file='input.wav',
        output_file='subtle.wav',
        level=1
    )

    print("\n2. Создание заметных искажений...")
    processor.process_with_distortion(
        input_file='input.wav',
        output_file='noticeable.wav',
        level=2
    )

    print("\n3. Создание крайне заметных искажений...")
    processor.process_with_distortion(
        input_file='input.wav',
        output_file='extreme.wav',
        level=3
    )
