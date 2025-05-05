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


class WavPCMProcessor:
    """Полная реализация PCM с бинарными ошибками"""

    def __init__(self):
        self.sample_rate = 44100
        self.bit_depth = 16
        self.max_level = 2 ** (self.bit_depth - 1) - 1

    def analog_to_pcm(self, analog_signal: Callable[[np.ndarray], np.ndarray],
                      duration: float) -> np.ndarray:
        """Полный цикл: аналоговый сигнал -> PCM"""
        # 1. Дискретизация
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        samples = analog_signal(t)

        # 2. Квантование
        pcm_data = np.round(samples * self.max_level).astype(np.int32)
        return np.clip(pcm_data, -self.max_level, self.max_level)

    def pcm_to_binary(self, pcm_data: np.ndarray) -> bytes:
        """PCM -> бинарные данные (с учетом битности)"""
        fmt = {16: 'h', 24: 'i', 32: 'i'}[self.bit_depth]
        return struct.pack(f'<{len(pcm_data)}{fmt}', *pcm_data)

    def binary_to_pcm(self, binary_data: bytes) -> np.ndarray:
        """Бинарные данные -> PCM"""
        fmt = {16: 'h', 24: 'i', 32: 'i'}[self.bit_depth]
        return np.array(struct.unpack(f'<{len(binary_data) // (self.bit_depth // 8)}{fmt}', binary_data))

    def corrupt_binary(self, binary_data: bytes, error_level: int) -> bytes:
        """Внесение ошибок в бинарные данные с выводом бинарного представления"""

        corrupted = bytearray(binary_data)

        if error_level == 1:  # Слабые ошибки (1% битов)
            for i in random.sample(range(len(corrupted)), k=len(corrupted) // 100):
                corrupted[i] ^= 0b00000001

        elif error_level == 2:  # Умеренные ошибки (5% битов + шум)
            for i in random.sample(range(len(corrupted)), k=len(corrupted) // 20):
                corrupted[i] ^= 0b00000011
            for i in range(0, len(corrupted), len(corrupted) // 50):
                corrupted[i] = random.randint(0, 255)

        elif error_level == 3:  # Ошибки 20%
            for i in random.sample(range(len(corrupted)), k=len(corrupted) // 5):
                corrupted[i] ^= 0b00000011

        elif error_level == 4:  # Ошибки 50%
            for i in random.sample(range(len(corrupted)), k=len(corrupted) // 2):
                corrupted[i] ^= 0b00000011

        return bytes(corrupted)

    def load_wav(self, filename: str) -> Tuple[np.ndarray, dict]:
        """Загрузка WAV с проверкой формата"""
        with wave.open(filename, 'rb') as wav_file:
            if wav_file.getnchannels() != 1:
                raise ValueError("Только моно-файлы")
            if wav_file.getsampwidth() not in (2, 3):
                raise ValueError("Только 16/24 бита")

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
        """Сохранение PCM в WAV"""
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
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        layout = QHBoxLayout()

        # Левая панель
        control_panel = QGroupBox("Управление")
        control_layout = QVBoxLayout()

        # Генерация тестового сигнала
        self.btn_generate = QPushButton("Сгенерировать сигнал 440 Гц")
        self.btn_generate.clicked.connect(self.generate_signal)
        control_layout.addWidget(self.btn_generate)

        # Загрузка WAV
        self.btn_load = QPushButton("Загрузить WAV (16/24 бит)")
        self.btn_load.clicked.connect(self.load_wav)
        control_layout.addWidget(self.btn_load)

        # Информация
        self.file_info = QTextEdit()
        self.file_info.setReadOnly(True)
        control_layout.addWidget(QLabel("Метаданные:"))
        control_layout.addWidget(self.file_info)

        # Уровень ошибок
        control_layout.addWidget(QLabel("Уровень ошибок:"))
        self.error_slider = QSlider(Qt.Horizontal)
        self.error_slider.setRange(0, 4)
        self.error_slider.setTickPosition(QSlider.TicksBelow)
        self.error_slider.valueChanged.connect(self.update_error_label)
        control_layout.addWidget(self.error_slider)

        self.error_label = QLabel("0 - Без ошибок")
        control_layout.addWidget(self.error_label)

        # Кнопки обработки
        self.btn_apply = QPushButton("Применить ошибки к бинарным данным")
        self.btn_apply.clicked.connect(self.apply_errors)
        self.btn_apply.setEnabled(False)
        control_layout.addWidget(self.btn_apply)

        self.btn_save = QPushButton("Сохранить WAV")
        self.btn_save.clicked.connect(self.save_wav)
        self.btn_save.setEnabled(False)
        control_layout.addWidget(self.btn_save)

        control_panel.setLayout(control_layout)

        # Правая панель
        graph_panel = QGroupBox("Визуализация")
        graph_layout = QVBoxLayout()

        self.figure, (self.ax_orig, self.ax_corr) = plt.subplots(2, 1, figsize=(10, 8))
        self.canvas = FigureCanvas(self.figure)
        graph_layout.addWidget(self.canvas)

        graph_panel.setLayout(graph_layout)

        layout.addWidget(control_panel, stretch=1)
        layout.addWidget(graph_panel, stretch=3)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def update_error_label(self, value):
        levels = {
            0: "0 - Без ошибок",
            1: "1 - 1% битов",
            2: "2 - 5% битов + шум",
            3: "3 - 20% битов",
            4: "4 - 50% битов"
        }
        self.error_label.setText(levels[value])

    def generate_signal(self):
        """Генерация тестового сигнала"""
        duration = 2.0  # 2 секунды
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
        """Применение ошибок к бинарным данным"""
        error_level = self.error_slider.value()
        if error_level == 0:
            self.corrupted_pcm = self.original_pcm.copy()
        else:
            # Конвертируем в бинарный вид
            binary_data = self.processor.pcm_to_binary(self.original_pcm)

            # Вносим ошибки
            corrupted_binary = self.processor.corrupt_binary(binary_data, error_level)

            # Обратно в PCM
            self.corrupted_pcm = self.processor.binary_to_pcm(corrupted_binary)

        self.plot_signals()
        self.file_info.append(f"\nПрименены ошибки уровня {error_level}")

    def save_wav(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Сохранить WAV", "", "WAV files (*.wav)")

        if not filepath:
            return

        try:
            self.processor.save_wav(self.corrupted_pcm, filepath)
            QMessageBox.information(self, "Успех", "Файл сохранён с ошибками")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def plot_signals(self):
        self.ax_orig.clear()
        self.ax_corr.clear()

        # Оригинал
        self.ax_orig.plot(self.original_pcm[:2000], 'b')
        self.ax_orig.set_title("Оригинальный PCM")

        # Искажённый
        self.ax_corr.plot(self.corrupted_pcm[:2000], 'r')
        self.ax_corr.set_title("С ошибками")

        self.figure.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PCMGUI()
    window.show()
    sys.exit(app.exec_())
