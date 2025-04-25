import numpy as np
import wave

def pcm_encode(input_file, output_file, sample_rate=44100, bit_depth=16):
    # Открываем входной файл
    with wave.open(input_file, 'rb') as wf:
        # Читаем параметры входного файла
        params = wf.getparams()
        n_channels, sampwidth, framerate, n_frames = params[:4]

        # Читаем все фреймы
        frames = wf.readframes(n_frames)

    # Преобразуем фреймы в массив numpy
    audio_array = np.frombuffer(frames, dtype=np.int16)

    # Нормализуем аудио данные
    audio_array = audio_array / (2 ** (bit_depth - 1))

    # Сохраняем в выходной файл
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_array.astype(np.int16).tobytes())

# Пример использования
pcm_encode('input.wav', 'output.wav')
