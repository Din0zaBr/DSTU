import sys
import wave
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFileDialog, QLabel, QWidget, QGroupBox,
                             QTextEdit, QMessageBox, QSlider)
from PyQt5.QtCore import Qt
from typing import Tuple, Callable
import struct
import random


class RLEEncoder:
    """Кодировщик RLE для PCM-аудио."""

    @staticmethod
    def encode(pcm_data: np.ndarray) -> bytes:
        """Сжимает PCM-данные с помощью RLE."""
        if len(pcm_data) == 0:
            return b''

        encoded = bytearray()
        current_value = pcm_data[0]
        count = 1

        # Используем struct для упаковки значений (16-битные числа -> 'h')
        pack_fmt = {16: 'h', 24: 'i', 32: 'i'}[pcm_data.dtype.itemsize * 8]

        for sample in pcm_data[1:]:
            if sample == current_value and count < 32767:  # Ограничение длины повтора
                count += 1
            else:
                encoded.extend(struct.pack(f'<{pack_fmt}H', current_value, count))
                current_value = sample
                count = 1

        # Добавляем последнюю последовательность
        encoded.extend(struct.pack(f'<{pack_fmt}H', current_value, count))
        return bytes(encoded)


class RLEDecoder:
    """Декодировщик RLE для PCM-аудио."""

    @staticmethod
    def decode(encoded_data: bytes, bit_depth: int) -> np.ndarray:
        """Восстанавливает PCM-данные из RLE."""
        if len(encoded_data) == 0:
            return np.array([], dtype=np.int32)

        unpack_fmt = {16: 'h', 24: 'i', 32: 'i'}[bit_depth // 8]
        sample_size = struct.calcsize(unpack_fmt)
        step_size = sample_size + 2  # +2 байта для длины повтора (H)

        decoded = []
        for i in range(0, len(encoded_data), step_size):
            chunk = encoded_data[i:i + step_size]
            value, count = struct.unpack(f'<{unpack_fmt}H', chunk)
            decoded.extend([value] * count)

        return np.array(decoded, dtype=np.int32)

class WavPCMProcessor:
    """Обработчик PCM-аудио с поддержкой бинарных ошибок."""

    def __init__(self):
        self.sample_rate = 44100
        self.bit_depth = 16
        self.max_level = 2 ** (self.bit_depth - 1) - 1

    def analog_to_pcm(self, analog_signal: Callable[[np.ndarray], np.ndarray],
                      duration: float) -> np.ndarray:
        """Преобразует аналоговый сигнал в PCM."""
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        samples = analog_signal(t)
        pcm_data = np.round(samples * self.max_level).astype(np.int32)
        return np.clip(pcm_data, -self.max_level, self.max_level)

    def pcm_to_binary(self, pcm_data: np.ndarray) -> bytes:
        """Конвертирует PCM в бинарные данные."""
        fmt = {16: 'h', 24: 'i', 32: 'i'}[self.bit_depth]
        return struct.pack(f'<{len(pcm_data)}{fmt}', *pcm_data)

    def binary_to_pcm(self, binary_data: bytes) -> np.ndarray:
        """Конвертирует бинарные данные обратно в PCM."""
        fmt = {16: 'h', 24: 'i', 32: 'i'}[self.bit_depth]
        return np.array(struct.unpack(f'<{len(binary_data) // (self.bit_depth // 8)}{fmt}', binary_data))

    def corrupt_binary(self, binary_data: bytes, error_level: int) -> bytes:
        """Вносит ошибки в бинарные данные."""
        corrupted = bytearray(binary_data)

        if error_level == 1:  # 1% битов
            for i in random.sample(range(len(corrupted)), k=len(corrupted) // 100):
                corrupted[i] ^= 0b00000001

        elif error_level == 2:  # 5% битов + шум
            for i in random.sample(range(len(corrupted)), k=len(corrupted) // 20):
                corrupted[i] ^= 0b00000011
            for i in range(0, len(corrupted), len(corrupted) // 50):
                corrupted[i] = random.randint(0, 255)

        elif error_level >= 3:  # 20%–100% битов
            error_mask = 0b00000011
            k = len(corrupted) // (6 - error_level)  # 3→20%, 4→50%, 5→100%
            for i in random.sample(range(len(corrupted)), k=k):
                corrupted[i] ^= error_mask

        return bytes(corrupted)

    def load_wav(self, filename: str) -> Tuple[np.ndarray, dict]:
        """Загружает WAV-файл с проверкой формата."""
        with wave.open(filename, 'rb') as wav_file:
            if wav_file.getnchannels() != 1:
                raise ValueError("Только монофайлы поддерживаются.")
            if wav_file.getsampwidth() not in (2, 3):
                raise ValueError("Только 16/24-битные файлы.")
            if wav_file.getframerate() not in (44100, 48000, 96000):
                raise ValueError("Частота дискретизации должна быть 44.1kHz, 48kHz или 96kHz.")

            self.sample_rate = wav_file.getframerate()
            self.bit_depth = wav_file.getsampwidth() * 8
            self.max_level = 2 ** (self.bit_depth - 1) - 1

            binary_data = wav_file.readframes(wav_file.getnframes())
            pcm_data = self.binary_to_pcm(binary_data)

            return pcm_data, {
                'sample_rate': self.sample_rate,
                'bit_depth': self.bit_depth,
                'duration': len(pcm_data) / self.sample_rate
            }

    def save_wav(self, pcm_data: np.ndarray, filename: str):
        """Сохраняет PCM-данные в WAV-файл."""
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(self.bit_depth // 8)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(self.pcm_to_binary(pcm_data))


class PCMGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.processor = WavPCMProcessor()
        self.setWindowTitle("PCM Processor with Binary Errors")
        self.setGeometry(100, 100, 1200, 800)
        self.rle_compressed_data = None
        self.init_ui()
        self.init_rle_ui()

    def init_ui(self):
        main_widget = QWidget()
        layout = QHBoxLayout()

        # Левая панель: управление
        control_panel = self._create_control_panel()
        layout.addWidget(control_panel, stretch=1)

        # Правая панель: графика
        graph_panel = self._create_graph_panel()
        layout.addWidget(graph_panel, stretch=3)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def init_rle_ui(self):
        """Добавляем элементы управления RLE."""
        rle_group = QGroupBox("RLE Сжатие")
        layout = QVBoxLayout()

        self.btn_compress = QPushButton("Сжать RLE")
        self.btn_compress.clicked.connect(self.compress_rle)
        layout.addWidget(self.btn_compress)

        self.btn_decompress = QPushButton("Разжать RLE")
        self.btn_decompress.clicked.connect(self.decompress_rle)
        layout.addWidget(self.btn_decompress)

        self.rle_stats = QLabel("Коэффициент сжатия: N/A")
        layout.addWidget(self.rle_stats)

        rle_group.setLayout(layout)
        self.control_panel.layout().insertWidget(2, rle_group)  # Добавляем после кнопок загрузки


    def _create_control_panel(self) -> QGroupBox:
        """Создаёт панель управления."""
        panel = QGroupBox("Управление")
        layout = QVBoxLayout()

        self.btn_generate = QPushButton("Сгенерировать сигнал 440 Гц")
        self.btn_generate.clicked.connect(self.generate_signal)
        layout.addWidget(self.btn_generate)

        self.btn_load = QPushButton("Загрузить WAV (16/24 бит)")
        self.btn_load.clicked.connect(self.load_wav)
        layout.addWidget(self.btn_load)

        self.file_info = QTextEdit()
        self.file_info.setReadOnly(True)
        layout.addWidget(QLabel("Метаданные:"))
        layout.addWidget(self.file_info)

        layout.addWidget(QLabel("Уровень ошибок:"))
        self.error_slider = QSlider(Qt.Horizontal)
        self.error_slider.setRange(0, 5)
        self.error_slider.setTickPosition(QSlider.TicksBelow)
        self.error_slider.valueChanged.connect(self.update_error_label)
        layout.addWidget(self.error_slider)

        self.error_label = QLabel("0 - Без ошибок")
        layout.addWidget(self.error_label)

        self.btn_apply = QPushButton("Применить ошибки")
        self.btn_apply.clicked.connect(self.apply_errors)
        self.btn_apply.setEnabled(False)
        layout.addWidget(self.btn_apply)

        self.btn_save = QPushButton("Сохранить WAV")
        self.btn_save.clicked.connect(self.save_wav)
        self.btn_save.setEnabled(False)
        layout.addWidget(self.btn_save)

        panel.setLayout(layout)
        return panel

    def _create_graph_panel(self) -> QGroupBox:
        """Создаёт панель с графиками."""
        panel = QGroupBox("Визуализация")
        layout = QVBoxLayout()

        self.figure, ((self.ax_full_orig, self.ax_full_corr),
                      (self.ax_zoom_orig, self.ax_zoom_corr)) = plt.subplots(
            2, 2, figsize=(12, 10))

        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        panel.setLayout(layout)
        return panel

    def update_error_label(self, value):
        """Обновляет описание уровня ошибок."""
        levels = {
            0: "0 - Без ошибок",
            1: "1 - 1% битов",
            2: "2 - 5% битов + шум",
            3: "3 - 20% битов",
            4: "4 - 50% битов",
            5: "5 - 100% битов"
        }
        self.error_label.setText(levels[value])

    def generate_signal(self):
        """Генерирует тестовый сигнал 440 Гц."""
        duration = 2.0
        signal = lambda t: 0.5 * np.sin(2 * np.pi * 440 * t) + 0.1 * np.random.normal(size=len(t))

        self.original_pcm = self.processor.analog_to_pcm(signal, duration)
        self.corrupted_pcm = self.original_pcm.copy()

        self.file_info.setPlainText(
            f"Сгенерирован сигнал 440 Гц\n"
            f"Частота: {self.processor.sample_rate} Гц\n"
            f"Битность: {self.processor.bit_depth} бит\n"
            f"Длительность: {duration} сек"
        )
        self.btn_apply.setEnabled(True)
        self.btn_save.setEnabled(True)
        self.plot_signals()

    def load_wav(self):
        """Загружает WAV-файл."""
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Выберите WAV", "", "WAV files (*.wav)")

        if not filepath:
            return

        try:
            self.original_pcm, meta = self.processor.load_wav(filepath)
            self.corrupted_pcm = self.original_pcm.copy()

            self.file_info.setPlainText(
                f"Файл: {filepath}\n"
                f"Частота: {meta['sample_rate']} Гц\n"
                f"Битность: {meta['bit_depth']} бит\n"
                f"Длительность: {meta['duration']:.2f} сек"
            )
            self.btn_apply.setEnabled(True)
            self.btn_save.setEnabled(True)
            self.plot_signals()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Неверный формат:\n{str(e)}")

    def apply_errors(self):
        """Применяет бинарные ошибки к сигналу."""
        error_level = self.error_slider.value()
        if error_level == 0:
            self.corrupted_pcm = self.original_pcm.copy()
        else:
            binary_data = self.processor.pcm_to_binary(self.original_pcm)
            corrupted_binary = self.processor.corrupt_binary(binary_data, error_level)
            self.corrupted_pcm = self.processor.binary_to_pcm(corrupted_binary)

        self.plot_signals()
        self.file_info.append(f"\nПрименены ошибки уровня {error_level}")

    def save_wav(self):
        """Сохраняет искажённый WAV-файл."""
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Сохранить WAV", "", "WAV files (*.wav)")

        if not filepath:
            return

        try:
            self.processor.save_wav(self.corrupted_pcm, filepath)
            QMessageBox.information(self, "Успех", "Файл сохранён с ошибками")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def compress_rle(self):
        """Сжимает текущий PCM-сигнал через RLE."""
        if self.original_pcm is None:
            QMessageBox.warning(self, "Ошибка", "Нет данных для сжатия!")
            return

        self.rle_compressed_data = RLEEncoder.encode(self.original_pcm)
        original_size = len(self.original_pcm) * (self.processor.bit_depth // 8)
        compressed_size = len(self.rle_compressed_data)
        ratio = original_size / compressed_size

        self.rle_stats.setText(
            f"Коэффициент сжатия: {ratio:.2f}:1\n"
            f"Исходный размер: {original_size} байт\n"
            f"Сжатый размер: {compressed_size} байт"
        )
        QMessageBox.information(self, "RLE", f"Данные сжаты с коэффициентом {ratio:.2f}:1")

    def decompress_rle(self):
        """Восстанавливает данные из RLE."""
        if self.rle_compressed_data is None:
            QMessageBox.warning(self, "Ошибка", "Нет сжатых данных!")
            return

        self.corrupted_pcm = RLEDecoder.decode(
            self.rle_compressed_data,
            self.processor.bit_depth
        )
        self.plot_signals()


    def plot_signals(self):
        """Отрисовывает 4 графика:
        1. Полный оригинальный сигнал
        2. Полный искажённый сигнал
        3. Первые 2000 отсчётов оригинального сигнала
        4. Первые 2000 отсчётов искажённого сигнала
        """
        # Очистка предыдущих графиков
        for ax in [self.ax_full_orig, self.ax_full_corr,
                   self.ax_zoom_orig, self.ax_zoom_corr]:
            ax.clear()

        # Полный сигнал (оригинал)
        self.ax_full_orig.plot(self.original_pcm, 'b', linewidth=0.5)
        self.ax_full_orig.set_title("Оригинальный сигнал (полный)")
        self.ax_full_orig.set_xlabel("Отсчёты")
        self.ax_full_orig.set_ylabel("Амплитуда")
        self.ax_full_orig.grid(True)

        # Полный сигнал (с ошибками)
        self.ax_full_corr.plot(self.corrupted_pcm, 'r', linewidth=0.5)
        self.ax_full_corr.set_title("Искажённый сигнал (полный)")
        self.ax_full_corr.set_xlabel("Отсчёты")
        self.ax_full_corr.set_ylabel("Амплитуда")
        self.ax_full_corr.grid(True)

        # Увеличенный участок (оригинал)
        self.ax_zoom_orig.plot(self.original_pcm[:2000], 'b', linewidth=1)
        self.ax_zoom_orig.set_title("Оригинальный сигнал (первые 2000 отсчётов)")
        self.ax_zoom_orig.set_xlabel("Отсчёты")
        self.ax_zoom_orig.set_ylabel("Амплитуда")
        self.ax_zoom_orig.grid(True)

        # Увеличенный участок (с ошибками)
        self.ax_zoom_corr.plot(self.corrupted_pcm[:2000], 'r', linewidth=1)
        self.ax_zoom_corr.set_title("Искажённый сигнал (первые 2000 отсчётов)")
        self.ax_zoom_corr.set_xlabel("Отсчёты")
        self.ax_zoom_corr.set_ylabel("Амплитуда")
        self.ax_zoom_corr.grid(True)

        self.figure.tight_layout()
        self.canvas.draw()

    def plot_rle_stats(self):
        """Рисует гистограмму длин повторов RLE."""
        if self.rle_compressed_data is None:
            return

        # Парсим RLE-данные
        unpack_fmt = {16: 'h', 24: 'i', 32: 'i'}[self.processor.bit_depth // 8]
        step_size = struct.calcsize(unpack_fmt) + 2
        lengths = []

        for i in range(0, len(self.rle_compressed_data), step_size):
            _, count = struct.unpack(f'<{unpack_fmt}H',
                                     self.rle_compressed_data[i:i + step_size])
            lengths.append(count)

        # Рисуем гистограмму
        plt.figure()
        plt.hist(lengths, bins=20, alpha=0.7)
        plt.title("Распределение длин повторов RLE")
        plt.xlabel("Длина повтора")
        plt.ylabel("Частота")
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PCMGUI()
    window.show()
    sys.exit(app.exec_())
