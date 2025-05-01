import wave
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Callable, Optional


class WavPCMProcessor:
    """Класс для обработки WAV файлов с визуализацией изменений"""

    def __init__(self):
        self.sample_width = 2  # 16-bit PCM по умолчанию
        self.sample_rate = 44100
        self.channels = 1

    def load_wav(self, filename: str) -> Tuple[np.ndarray, dict]:
        """Загрузка WAV файла"""
        with wave.open(filename, 'rb') as wav_file:
            self.sample_rate = wav_file.getframerate()
            self.channels = wav_file.getnchannels()
            self.sample_width = wav_file.getsampwidth()

            frames = wav_file.readframes(wav_file.getnframes())
            dtype = np.int16 if self.sample_width == 2 else np.int8
            pcm_data = np.frombuffer(frames, dtype=dtype)

            metadata = {
                'sample_rate': self.sample_rate,
                'channels': self.channels,
                'sample_width': self.sample_width,
                'duration': wav_file.getnframes() / self.sample_rate
            }

            return pcm_data, metadata

    def save_wav(self, pcm_data: np.ndarray, filename: str):
        """
        Сохранение в WAV файл
        """
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(self.sample_width)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(pcm_data.tobytes())

    def pcm_to_float(self, pcm_data: np.ndarray) -> np.ndarray:
        """
        Конвертация PCM в float [-1, 1]
        WAV → Float
        """
        if self.sample_width == 1:
            return pcm_data.astype(np.float32) / 127.0
        return pcm_data.astype(np.float32) / 32767.0

    def float_to_pcm(self, float_audio: np.ndarray) -> np.ndarray:
        """
        Конвертация float в PCM
        Float → PCM
        """

        if self.sample_width == 1:
            return (float_audio * 127).astype(np.int8)
        return (float_audio * 32767).astype(np.int16)

    def process_with_visualization(self, input_file: str, output_file: str,
                                   process_func: Callable[[np.ndarray], np.ndarray],
                                   title: str = "Audio Processing"):
        """
        Полная обработка с визуализацией изменений
        """
        # Загрузка исходного файла
        original_pcm, meta = self.load_wav(input_file)
        original_float = self.pcm_to_float(original_pcm)

        # Обработка аудио
        processed_float = process_func(original_float)
        processed_pcm = self.float_to_pcm(processed_float)

        # Сохранение результата
        self.save_wav(processed_pcm, output_file)

        # Визуализация
        self._plot_comparison(original_float, processed_float,
                              original_pcm, processed_pcm,
                              title, meta['sample_rate'])

        return processed_pcm

    def _plot_comparison(self, original_float: np.ndarray, processed_float: np.ndarray,
                         original_pcm: np.ndarray, processed_pcm: np.ndarray,
                         title: str, sample_rate: int):
        """Сравнение оригинального и обработанного аудио"""
        plt.figure(figsize=(15, 10))

        # Временная область (первые 0.1 секунды)
        samples_to_show = int(0.1 * sample_rate)

        # 1. Сравнение float сигналов
        plt.subplot(3, 1, 1)
        plt.plot(original_float[:samples_to_show], 'b', label='Original', alpha=0.7)
        plt.plot(processed_float[:samples_to_show], 'r', label='Processed', alpha=0.7)
        plt.title(f'{title} - Float Signal Comparison')
        plt.xlabel('Samples')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.grid(True)

        # 2. Сравнение PCM сигналов
        plt.subplot(3, 1, 2)
        plt.plot(original_pcm[:samples_to_show], 'b', label='Original', alpha=0.7)
        plt.plot(processed_pcm[:samples_to_show], 'r', label='Processed', alpha=0.7)
        plt.title('PCM Signal Comparison')
        plt.xlabel('Samples')
        plt.ylabel('PCM Value')
        plt.legend()
        plt.grid(True)

        # 3. Сравнение спектров
        plt.subplot(3, 1, 3)
        freqs = np.fft.rfftfreq(len(original_float), 1 / sample_rate)
        plt.semilogy(freqs, np.abs(np.fft.rfft(original_float)), 'b',
                     label='Original', alpha=0.7)
        plt.semilogy(freqs, np.abs(np.fft.rfft(processed_float)), 'r',
                     label='Processed', alpha=0.7)
        plt.title('Frequency Spectrum Comparison')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()


# Примеры эффектов для обработки
# def gain_effect(audio: np.ndarray, gain: float = 2.0) -> np.ndarray:
#     """Эффект усиления сигнала"""
#     return np.clip(audio * gain, -0.99, 0.99)
#
#
# def distortion_effect(audio: np.ndarray, intensity: float = 3.0) -> np.ndarray:
#     """Эффект дисторшна"""
#     return np.tanh(audio * intensity)
#
#
# def lowpass_effect(audio: np.ndarray, cutoff: float = 2000.0, sr: int = 44100) -> np.ndarray:
#     """Простой низкочастотный фильтр"""
#     fft_audio = np.fft.rfft(audio)
#     freqs = np.fft.rfftfreq(len(audio), 1 / sr)
#     fft_audio[freqs > cutoff] *= 0.1  # Ослабляем высокие частоты
#     return np.fft.irfft(fft_audio)


# Сравнение правильного и ошибочного декодирования
print("Сравнение правильного и ошибочного декодирования")
WavPCMProcessor.compare_decoding(input_file='input.wav')

    # # Обработка с усилением
    # print("Пример обработки - усиление сигнала")
    # processor.process_with_visualization(
    #     input_file='input.wav',
    #     output_file='output_gain.wav',
    #     process_func=lambda x: gain_effect(x, gain=2.0),
    #     title="Gain Effect (2x)"
    # )
    #
    # # Обработка с дисторшном
    # print("\nПример обработки - дисторшн")
    # processor.process_with_visualization(
    #     input_file='input.wav',
    #     output_file='output_distortion.wav',
    #     process_func=lambda x: distortion_effect(x, intensity=5.0),
    #     title="Distortion Effect"
    # )
    #
    # # Обработка с низкочастотным фильтром
    # print("\nПример обработки - низкочастотный фильтр")
    # processor.process_with_visualization(
    #     input_file='input.wav',
    #     output_file='output_lowpass.wav',
    #     process_func=lambda x: lowpass_effect(x, cutoff=2000.0),
    #     title="Lowpass Filter (2kHz)"
