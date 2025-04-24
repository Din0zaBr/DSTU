import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter


class PCMProcessor:
    def __init__(self, sample_rate=44100, bits=8):
        """
        Инициализация процессора PCM

        Args:
            sample_rate: частота дискретизации в Гц
            bits: количество бит для квантования
        """
        self.sample_rate = sample_rate
        self.bits = bits

    def load_audio(self, filename):
        """Загрузка аудиофайла"""
        data, sr = sf.read(filename)
        if len(data.shape) > 1:  # Если стерео, конвертируем в моно
            data = np.mean(data, axis=1)
        return data

    def save_audio(self, signal, filename):
        """Сохранение аудиосигнала в файл"""
        sf.write(filename, signal, self.sample_rate)

    def quantize_signal(self, signal):
        """Квантование сигнала"""
        max_val = np.max(np.abs(signal))
        levels = 2 ** self.bits
        return np.round((signal / max_val * (levels - 1))) * (max_val / (levels - 1))

    def decode_signal(self, quantized_signal):
        """Декодирование сигнала"""
        return quantized_signal.copy()

    def apply_filter(self, signal):
        """Применение ЦИХ фильтра"""
        nyq_freq = 0.5 * self.sample_rate
        cutoff_freq = 20000
        order = 8

        b, a = butter(order, cutoff_freq / nyq_freq, btype='low')
        return lfilter(b, a, signal)

    def process_pcm(self, input_filename, output_filename=None):
        """
        Полная обработка PCM для файла

        Args:
            input_filename: имя входного файла
            output_filename: имя выходного файла (если None, вернёт сигнал)

        Returns:
            Обработанный сигнал если output_filename=None
        """
        # Загружаем файл
        signal = self.load_audio(input_filename)

        # Квантуем сигнал
        quantized = self.quantize_signal(signal)

        # Декодируем и применяем фильтр
        decoded = self.decode_signal(quantized)
        filtered = self.apply_filter(decoded)

        # Сохраняем результат или возвращаем его
        if output_filename:
            self.save_audio(filtered, output_filename)
            return None
        return filtered


# Пример использования:
processor = PCMProcessor(bits=8)
processed_signal = processor.process_pcm('input.wav')

processor.process_pcm('input.wav', 'output.wav')
