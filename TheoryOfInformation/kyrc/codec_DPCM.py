import sys
import wave
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QLabel, QWidget, QGroupBox, QTextEdit, QMessageBox, QSlider, QDoubleSpinBox
)


class DPCMCodec:
    """DPCM encoder/decoder for audio signals."""

    @staticmethod
    def encode(signal: np.ndarray, step: float) -> np.ndarray:
        """Encode signal using DPCM with given quantization step."""
        encoded = []
        prev = 0
        for sample in signal:
            diff = sample - prev
            code = int(round(diff / step))
            # Ограничиваем значение диапазоном int8
            code = max(-128, min(127, code))
            encoded.append(code)
            # Обновляем prev с учетом ограничения int8
            prev += code * step
        return np.array(encoded, dtype=np.int8)

    @staticmethod
    def decode(encoded: np.ndarray, step: float) -> np.ndarray:
        """Decode DPCM-encoded data with given quantization step."""
        decoded = []
        prev = 0
        for code in encoded:
            # Восстанавливаем сэмпл
            sample = prev + code * step
            decoded.append(sample)
            # Обновляем prev так же, как при кодировании
            prev = sample
        return np.array(decoded, dtype=np.int16)

    @staticmethod
    def save_compressed(encoded: np.ndarray, filename: str):
        """
        Save DPCM-encoded data as a text file (one value per line).
        """
        with open(filename, 'w') as f:
            for value in encoded:
                f.write(f"{value}\n")

    @staticmethod
    def load_compressed(filename: str) -> np.ndarray:
        """
        Load DPCM-encoded data from a text file (one value per line).
        """
        with open(filename, 'r') as f:
            return np.array([int(line.strip()) for line in f if line.strip()], dtype=np.int8)

    @staticmethod
    def compression_info(original: np.ndarray, encoded: np.ndarray, step: float) -> str:
        """Return compression statistics as a string."""
        # Размер оригинальных данных в байтах (16 бит на сэмпл)
        orig_size = len(original) * 2

        # Размер закодированных данных в байтах
        # Каждая разность занимает 8 бит (1 байт)
        # Плюс 8 байт для хранения шага квантования (float64)
        enc_size = len(encoded) + 8

        ratio = orig_size / enc_size if enc_size else 0
        decoded = DPCMCodec.decode(encoded, step)
        error = np.mean(np.abs(original - decoded))
        return (
            f"Размер оригинальных данных: {orig_size:,} байт\n"
            f"Размер сжатых данных: {enc_size:,} байт\n"
            f"Коэффициент сжатия: {ratio:.2f}x\n"
            f"Средняя ошибка квантования: {error:.2f}\n"
            f"Шаг квантования: {step}\n"
            f"ВНИМАНИЕ: Используется 8-битное кодирование разностей.\n"
            f"          Большие разности между сэмплами будут обрезаться,\n"
            f"          что может привести к искажению сигнала."
        )


class WavProcessor:
    """WAV file loader/saver for mono 16-bit PCM audio."""

    def __init__(self):
        self.sample_rate = 44100
        self.bit_depth = 16

    def load(self, filename: str) -> np.ndarray:
        with wave.open(filename, 'rb') as wav:
            if wav.getnchannels() != 1:
                raise ValueError("Только монофайлы поддерживаются.")
            if wav.getsampwidth() != 2:
                raise ValueError("Только 16-битные файлы поддерживаются.")
            self.sample_rate = wav.getframerate()
            self.bit_depth = 16
            data = wav.readframes(wav.getnframes())
            return self._binary_to_pcm(data)

    def save(self, pcm: np.ndarray, filename: str):
        with wave.open(filename, 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            wav.writeframes(self._pcm_to_binary(pcm))

    def _pcm_to_binary(self, pcm: np.ndarray) -> bytes:
        return pcm.astype(np.int16).tobytes()

    def _binary_to_pcm(self, data: bytes) -> np.ndarray:
        return np.frombuffer(data, dtype=np.int16)


class DPCMGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.processor = WavProcessor()
        self.codec = DPCMCodec()
        self.setWindowTitle("DPCM Codec")
        self.setGeometry(100, 100, 1200, 800)
        self.original = None
        self.encoded = None
        self.decoded = None
        self._init_ui()

    def _init_ui(self):
        main_widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self._control_panel(), 1)
        layout.addWidget(self._graph_panel(), 3)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def _control_panel(self) -> QGroupBox:
        panel = QGroupBox("Управление")
        layout = QVBoxLayout()

        btn_load = QPushButton("Загрузить WAV (16-битный)")
        btn_load.clicked.connect(self.load_wav)
        layout.addWidget(btn_load)

        self.info = QTextEdit(readOnly=True)
        layout.addWidget(QLabel("Метаданные:"))
        layout.addWidget(self.info)

        layout.addWidget(QLabel("Шаг квантования:"))
        self.step = QDoubleSpinBox()
        self.step.setRange(0.1, 100.0)
        self.step.setSingleStep(0.1)
        self.step.setValue(1.0)
        layout.addWidget(self.step)

        btn_encode = QPushButton("Закодировать DPCM")
        btn_encode.clicked.connect(self.encode_dpcm)
        layout.addWidget(btn_encode)

        self.btn_save_compr = QPushButton("Сохранить сжатые данные")
        self.btn_save_compr.clicked.connect(self.save_compressed)
        self.btn_save_compr.setEnabled(False)
        layout.addWidget(self.btn_save_compr)

        self.btn_load_compr = QPushButton("Загрузить сжатые данные")
        self.btn_load_compr.clicked.connect(self.load_compressed)
        layout.addWidget(self.btn_load_compr)

        self.stats = QTextEdit(readOnly=True)
        layout.addWidget(QLabel("Информация о кодировании:"))
        layout.addWidget(self.stats)

        btn_decode = QPushButton("Декодировать DPCM")
        btn_decode.clicked.connect(self.decode_dpcm)
        layout.addWidget(btn_decode)

        btn_save = QPushButton("Сохранить результат")
        btn_save.clicked.connect(self.save_wav)
        layout.addWidget(btn_save)

        panel.setLayout(layout)
        return panel

    def _graph_panel(self) -> QGroupBox:
        panel = QGroupBox("Графики")
        layout = QVBoxLayout()
        self.figure = plt.figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        panel.setLayout(layout)
        return panel

    def load_wav(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Открыть WAV файл", "", "WAV files (*.wav)")
        if not filename:
            return
        try:
            self.original = self.processor.load(filename)
            self.info.setText(
                f"Частота дискретизации: {self.processor.sample_rate} Hz\n"
                f"Разрядность: {self.processor.bit_depth} бит\n"
                f"Длительность: {len(self.original) / self.processor.sample_rate:.2f} сек\n"
                f"Количество сэмплов: {len(self.original)}"
            )
            self.plot_signals()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def encode_dpcm(self):
        if self.original is None:
            return
        step = self.step.value()
        self.encoded = self.codec.encode(self.original, step)
        self.stats.setText(self.codec.compression_info(self.original, self.encoded, step))
        self.btn_save_compr.setEnabled(True)
        self.plot_signals()
        # Показываем предупреждение о возможных искажениях
        QMessageBox.warning(self, "Предупреждение",
                            "Используется 8-битное кодирование разностей.\n"
                            "Большие разности между сэмплами будут обрезаться,\n"
                            "что может привести к искажению сигнала.")

    def save_compressed(self):
        if self.encoded is None:
            return
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить сжатые данные", "", "Text files (*.txt)")
        if not filename:
            return
        try:
            self.codec.save_compressed(self.encoded, filename)
            QMessageBox.information(self, "Успех", "Сжатые данные успешно сохранены (text, одно значение на строку)")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def load_compressed(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Загрузить сжатые данные", "", "Text files (*.txt)")
        if not filename:
            return
        try:
            self.encoded = self.codec.load_compressed(filename)
            self.plot_signals()
            QMessageBox.information(self, "Успех", "Сжатые данные успешно загружены (text, одно значение на строку)")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def decode_dpcm(self):
        if self.encoded is None:
            return
        step = self.step.value()
        self.decoded = self.codec.decode(self.encoded, step)
        self.plot_signals()

    def save_wav(self):
        if self.decoded is None:
            return
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить WAV файл", "", "WAV files (*.wav)")
        if not filename:
            return
        try:
            self.processor.save(self.decoded, filename)
            QMessageBox.information(self, "Успех", "Файл успешно сохранен")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def plot_signals(self):
        self.figure.clear()
        if self.original is not None:
            ax1 = self.figure.add_subplot(311)
            ax1.plot(self.original)
            ax1.set_title("Оригинальный сигнал")
            ax1.grid(True)
        if self.encoded is not None:
            ax2 = self.figure.add_subplot(312)
            ax2.plot(self.encoded)
            ax2.set_title("DPCM-код (разности)")
            ax2.grid(True)
        if self.decoded is not None:
            ax3 = self.figure.add_subplot(313)
            ax3.plot(self.decoded)
            ax3.set_title("Декодированный сигнал")
            ax3.grid(True)
        self.figure.tight_layout()
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DPCMGUI()
    window.show()
    sys.exit(app.exec_())
