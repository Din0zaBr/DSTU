# -*- coding: utf-8 -*-
import PySimpleGUI as sg
import random
import numpy as np


class CyclicCodeApp:
    def __init__(self):
        self.polynomial = "1011"
        self.n = 7
        self.k = 4
        self.error_positions = ""
        self.manual_errors = False
        self.code_type = "polynomial"
        self.input_type = "keyboard"
        self.num_errors = 1
        self.G = None

        self.setup_layout()
        self.window = sg.Window("Циклический код - Кодер/Декодер", self.layout, finalize=True)

    def setup_layout(self):
        tab1 = self.create_encode_tab()
        tab2 = self.create_decode_tab()

        self.layout = [
            [sg.TabGroup([
                [sg.Tab('Кодирование', tab1),
                 sg.Tab('Декодирование', tab2),
                 ]
            ], expand_x=True, expand_y=True)
            ]]

    def create_encode_tab(self):
        return [
            [sg.Frame('Входные данные', [
                [sg.Radio('Ввод с клавиатуры', 'input_type', default=True, key='-INPUT_KEYBOARD-'),
                 sg.Radio('Загрузка из файла', 'input_type', key='-INPUT_FILE-')],
                [sg.Text('Текст для кодирования:')],
                [sg.Multiline(size=(60, 5), key='-INPUT_TEXT-')],
                [sg.Button('Загрузить из файла', key='-LOAD_FILE-')]
            ])],

            [sg.Frame('Параметры кода', [
                [sg.Radio('Полиномиальный код', 'code_type', default=True, key='-POLY_CODE-'),
                 sg.Radio('Матричный код', 'code_type', key='-MATRIX_CODE-')],

                [sg.pin(sg.Column([
                    [sg.Text('Порождающий полином (двоичный):'), sg.Input("1011", size=(20, 1), key='-POLYNOMIAL-')],
                    [sg.Text('Длина кода (n):'), sg.Input("7", size=(5, 1), key='-N-')],
                    [sg.Text('Размерность кода (k):'), sg.Input("4", size=(5, 1), key='-K-')]
                ], key='-POLY_FRAME-'))],

                [sg.pin(sg.Column([
                    [sg.Text('Порождающая матрица (построчно, двоичные значения):')],
                    [sg.Multiline(size=(40, 5), key='-MATRIX_TEXT-')]
                ], visible=False, key='-MATRIX_FRAME-'))]
            ])],

            [sg.Button('Закодировать', key='-ENCODE-')],

            [sg.Frame('Результаты кодирования', [
                [sg.Text('Закодированная последовательность:')],
                [sg.Input(size=(60, 1), key='-OUTPUT_TEXT-', readonly=True)],
                [sg.Multiline(size=(60, 10), key='-ENCODE_INFO-', disabled=True)]
            ])]
        ]

    def create_decode_tab(self):
        return [
            [sg.Frame('Входные данные', [
                [sg.Text('Закодированная последовательность:')],
                [sg.Input(size=(60, 1), key='-ENCODED_INPUT-')]
            ])],

            [sg.Frame('Параметры кода', [
                [sg.Radio('Полиномиальный код', 'decode_code_type', default=True, key='-DECODE_POLY_CODE-'),
                 sg.Radio('Матричный код', 'decode_code_type', key='-DECODE_MATRIX_CODE-')],

                [sg.pin(sg.Column([
                    [sg.Text('Порождающий полином (двоичный):'),
                     sg.Input("1011", size=(20, 1), key='-DECODE_POLYNOMIAL-')],
                    [sg.Text('Длина кода (n):'), sg.Input("7", size=(5, 1), key='-DECODE_N-')],
                    [sg.Text('Размерность кода (k):'), sg.Input("4", size=(5, 1), key='-DECODE_K-')]
                ], key='-DECODE_POLY_FRAME-'))],

                [sg.pin(sg.Column([
                    [sg.Text('Порождающая матрица (построчно, двоичные значения):')],
                    [sg.Multiline(size=(40, 5), key='-DECODE_MATRIX_TEXT-')]
                ], visible=False, key='-DECODE_MATRIX_FRAME-'))]
            ])],

            [sg.Frame('Внесение ошибок', [
                [sg.Radio('Случайные ошибки', 'error_type', default=True, key='-RANDOM_ERRORS-'),
                 sg.Radio('Ручное указание ошибок', 'error_type', key='-MANUAL_ERRORS-')],

                [sg.pin(sg.Column([
                    [sg.Text('Количество ошибок:'), sg.Input("1", size=(5, 1), key='-NUM_ERRORS-')]
                ], key='-RANDOM_ERROR_FRAME-'))],

                [sg.pin(sg.Column([
                    [sg.Text('Позиции ошибок (через запятую):'), sg.Input(size=(30, 1), key='-ERROR_POSITIONS-')]
                ], visible=False, key='-MANUAL_ERROR_FRAME-'))]
            ])],

            [sg.Button('Декодировать', key='-DECODE-')],

            [sg.Frame('Результаты декодирования', [
                [sg.Text('Декодированная последовательность:')],
                [sg.Input(size=(60, 1), key='-DECODED_TEXT-', readonly=True)],
                [sg.Multiline(size=(60, 15), key='-DECODE_INFO-', disabled=True)]
            ])]
        ]

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WINDOW_CLOSED:
                break

            elif event == '-POLY_CODE-':
                self.window['-POLY_FRAME-'].update(visible=True)
                self.window['-MATRIX_FRAME-'].update(visible=False)

            elif event == '-MATRIX_CODE-':
                self.window['-POLY_FRAME-'].update(visible=False)
                self.window['-MATRIX_FRAME-'].update(visible=True)

            elif event == '-DECODE_POLY_CODE-':
                self.window['-DECODE_POLY_FRAME-'].update(visible=True)
                self.window['-DECODE_MATRIX_FRAME-'].update(visible=False)

            elif event == '-DECODE_MATRIX_CODE-':
                self.window['-DECODE_POLY_FRAME-'].update(visible=False)
                self.window['-DECODE_MATRIX_FRAME-'].update(visible=True)

            elif event == '-RANDOM_ERRORS-':
                self.window['-RANDOM_ERROR_FRAME-'].update(visible=True)
                self.window['-MANUAL_ERROR_FRAME-'].update(visible=False)

            elif event == '-MANUAL_ERRORS-':
                self.window['-RANDOM_ERROR_FRAME-'].update(visible=False)
                self.window['-MANUAL_ERROR_FRAME-'].update(visible=True)

            elif event == '-LOAD_FILE-':
                file_path = sg.popup_get_file('Выберите файл')
                if file_path:
                    try:
                        with open(file_path, 'r') as file:
                            self.window['-INPUT_TEXT-'].update(file.read())
                    except Exception as e:
                        sg.popup_error(f"Не удалось загрузить файл: {str(e)}")

            elif event == '-ENCODE-':
                self.encode(values)

            elif event == '-DECODE-':
                self.decode(values)

        self.window.close()

    def binary_to_poly(self, binary_str):
        terms = []
        degree = len(binary_str) - 1
        for i, bit in enumerate(binary_str):
            if bit == '1':
                if degree - i == 1:
                    terms.append("x")
                elif degree - i == 0:
                    terms.append("1")
                else:
                    terms.append(f"x^{degree - i}")
        return " + ".join(terms) if terms else "0"

    def polynomial_encode(self, data, g, n, k):
        m = len(g) - 1
        if n - k != m:
            raise ValueError("Несоответствие параметров n, k и степени полинома")

        blocks = [data[i:i + k] for i in range(0, len(data), k)]
        encoded_blocks = []

        for block in blocks:
            block = block.zfill(k)
            extended = block + '0' * m
            remainder = self.polynomial_division(extended, g)
            codeword = block + remainder
            encoded_blocks.append(codeword)

        return ''.join(encoded_blocks)

    def polynomial_division(self, dividend, divisor):
        dividend = [int(bit) for bit in dividend]
        divisor = [int(bit) for bit in divisor]

        while len(dividend) > 0 and dividend[0] == 0:
            dividend = dividend[1:]

        while len(divisor) > 0 and divisor[0] == 0:
            divisor = divisor[1:]

        if not dividend:
            return '0' * (len(divisor) - 1)

        if len(divisor) > len(dividend):
            return ''.join(map(str, dividend)).zfill(len(divisor) - 1)

        current = list(dividend)
        divisor_len = len(divisor)

        for i in range(len(current) - divisor_len + 1):
            if current[i] == 1:
                for j in range(divisor_len):
                    current[i + j] ^= divisor[j]

        remainder = current[-(divisor_len - 1):] if divisor_len > 1 else [0]
        return ''.join(map(str, remainder)).zfill(len(divisor) - 1)

    def matrix_encode(self, data, G):
        k = len(G)
        n = len(G[0])
        blocks = [data[i:i + k] for i in range(0, len(data), k)]
        encoded_blocks = []

        for block in blocks:
            block = block.zfill(k)
            block_vector = [int(bit) for bit in block]
            codeword = [0] * n
            for i in range(n):
                for j in range(k):
                    codeword[i] += block_vector[j] * G[j][i]
                codeword[i] %= 2
            encoded_blocks.append(''.join(map(str, codeword)))

        return ''.join(encoded_blocks)

    def encode(self, values):
        try:
            input_data = values['-INPUT_TEXT-']
            if not input_data:
                sg.popup_error("Введите текст для кодирования")
                return

            binary_data = ''.join(format(ord(c), '08b') for c in input_data)

            if values['-POLY_CODE-']:
                g_str = values['-POLYNOMIAL-']
                if not g_str:
                    sg.popup_error("Введите порождающий полином")
                    return

                try:
                    n = int(values['-N-'])
                    k = int(values['-K-'])
                except ValueError:
                    sg.popup_error("Параметры n и k должны быть целыми числами")
                    return

                g = [int(bit) for bit in g_str]
                encoded = self.polynomial_encode(binary_data, g, n, k)
                G = self.poly_to_matrix(g_str, n, k)
                matrix_str = '\n'.join(''.join(str(bit) for bit in row) for row in G)

                info = f"Порождающий полином: {g_str}\n"
                info += f"Полиномиальное представление: {self.binary_to_poly(g_str)}\n\n"
                info += f"Порождающая матрица:\n{matrix_str}\n\n"
                info += f"Исходные данные (бинарно): {binary_data}\n"
                info += f"Закодированные данные: {encoded}"

            else:
                matrix_text = values['-MATRIX_TEXT-']
                if not matrix_text:
                    sg.popup_error("Введите порождающую матрицу")
                    return

                G = []
                for line in matrix_text.split('\n'):
                    row = [int(bit) for bit in line.strip()]
                    G.append(row)

                try:
                    n = len(G[0])
                    k = len(G)
                except IndexError:
                    sg.popup_error("Некорректная порождающая матрица")
                    return

                encoded = self.matrix_encode(binary_data, G)
                poly_str = self.matrix_to_poly(G)
                poly_repr = self.binary_to_poly(poly_str)

                info = f"Порождающая матрица:\n{matrix_text}\n\n"
                info += f"Порождающий полином (двоичный): {poly_str}\n"
                info += f"Полиномиальное представление: {poly_repr}\n\n"
                info += f"Исходные данные (бинарно): {binary_data}\n"
                info += f"Закодированные данные: {encoded}"

            self.window['-OUTPUT_TEXT-'].update(encoded)
            self.window['-ENCODE_INFO-'].update(info)

        except Exception as e:
            sg.popup_error(f"Ошибка кодирования: {str(e)}")

    def decode(self, values):
        try:
            encoded_data = values['-ENCODED_INPUT-']
            if not encoded_data:
                sg.popup_error("Введите закодированную последовательность")
                return

            if not all(c in '01' for c in encoded_data):
                sg.popup_error("Данные должны содержать только 0 и 1")
                return

            if values['-DECODE_POLY_CODE-']:
                g_str = values['-DECODE_POLYNOMIAL-']
                if not g_str:
                    sg.popup_error("Введите порождающий полином")
                    return

                try:
                    n = int(values['-DECODE_N-'])
                    k = int(values['-DECODE_K-'])
                except ValueError:
                    sg.popup_error("Параметры n и k должны быть целыми числами")
                    return

                if len(encoded_data) % n != 0:
                    sg.popup_error(f"Длина данных ({len(encoded_data)}) должна быть кратна n ({n})")
                    return

                g = [int(bit) for bit in g_str]

                if values['-MANUAL_ERRORS-']:
                    error_pos = values['-ERROR_POSITIONS-']
                    try:
                        error_positions = [int(pos) - 1 for pos in error_pos.split(',')] if error_pos else []
                    except ValueError:
                        sg.popup_error("Позиции ошибок должны быть числами")
                        return
                else:
                    try:
                        num_errors = int(values['-NUM_ERRORS-'])
                        error_positions = random.sample(range(len(encoded_data)),
                                                        min(num_errors, len(encoded_data)))
                    except ValueError:
                        sg.popup_error("Количество ошибок должно быть числом")
                        return

                data_with_errors = list(encoded_data)
                for pos in error_positions:
                    if pos < len(data_with_errors):
                        data_with_errors[pos] = '1' if data_with_errors[pos] == '0' else '0'
                data_with_errors = ''.join(data_with_errors)

                decoded, steps = self.megitt_decode(data_with_errors, g, n, k)

                G = self.poly_to_matrix(g_str, n, k)
                matrix_str = '\n'.join(''.join(str(bit) for bit in row) for row in G)

                info = f"Порождающий полином: {g_str}\n"
                info += f"Полиномиальное представление: {self.binary_to_poly(g_str)}\n\n"
                info += f"Порождающая матрица:\n{matrix_str}\n\n"
                info += f"Закодированные данные: {encoded_data}\n"
                info += f"Ошибки на позициях: {[p + 1 for p in error_positions]}\n"
                info += f"Данные с ошибками: {data_with_errors}\n\n"
                info += "Процесс декодирования:\n" + steps

            else:
                matrix_text = values['-DECODE_MATRIX_TEXT-']
                if not matrix_text:
                    sg.popup_error("Введите порождающую матрицу")
                    return

                G = []
                for line in matrix_text.split('\n'):
                    row = [int(bit) for bit in line.strip()]
                    G.append(row)

                try:
                    n = len(G[0])
                    k = len(G)
                except IndexError:
                    sg.popup_error("Некорректная порождающая матрица")
                    return

                if len(encoded_data) % n != 0:
                    sg.popup_error(f"Длина данных ({len(encoded_data)}) должна быть кратна n ({n})")
                    return

                if values['-MANUAL_ERRORS-']:
                    error_pos = values['-ERROR_POSITIONS-']
                    try:
                        error_positions = [int(pos) - 1 for pos in error_pos.split(',')] if error_pos else []
                    except ValueError:
                        sg.popup_error("Позиции ошибок должны быть числами")
                        return
                else:
                    try:
                        num_errors = int(values['-NUM_ERRORS-'])
                        error_positions = random.sample(range(len(encoded_data)),
                                                        min(num_errors, len(encoded_data)))
                    except ValueError:
                        sg.popup_error("Количество ошибок должно быть числом")
                        return

                data_with_errors = list(encoded_data)
                for pos in error_positions:
                    if pos < len(data_with_errors):
                        data_with_errors[pos] = '1' if data_with_errors[pos] == '0' else '0'
                data_with_errors = ''.join(data_with_errors)

                poly_str = self.matrix_to_poly(G)
                g = [int(bit) for bit in poly_str]
                decoded, steps = self.megitt_decode(data_with_errors, g, n, k)

                info = f"Порождающая матрица:\n{matrix_text}\n\n"
                info += f"Порождающий полином (двоичный): {poly_str}\n"
                info += f"Полиномиальное представление: {self.binary_to_poly(poly_str)}\n\n"
                info += f"Закодированные данные: {encoded_data}\n"
                info += f"Ошибки на позициях: {[p + 1 for p in error_positions]}\n"
                info += f"Данные с ошибками: {data_with_errors}\n\n"
                info += "Процесс декодирования:\n" + steps

            self.window['-DECODED_TEXT-'].update(decoded)
            self.window['-DECODE_INFO-'].update(info)

        except Exception as e:
            sg.popup_error(f"Ошибка декодирования: {str(e)}")

    def megitt_decode(self, encoded_data, g, n, k):
        m = len(g) - 1  # степень порождающего полинома
        steps = ""
        blocks = [encoded_data[i:i + n] for i in range(0, len(encoded_data), n)]
        decoded_blocks = []

        # Строим таблицу синдромов для всех возможных ошибок
        error_patterns = {}
        for i in range(n):
            error = [0] * n
            error[i] = 1
            remainder = self.polynomial_division(''.join(map(str, error)), ''.join(map(str, g)))
            error_patterns[remainder.zfill(m)] = i

        steps += "Таблица синдромов и ошибок:\n"
        for pattern, pos in error_patterns.items():
            steps += f"Синдром: {pattern} -> Ошибка в позиции {pos + 1}\n"
        steps += "\n"

        for block in blocks:
            if len(block) < n:
                block = block.ljust(n, '0')

            steps += f"\nДекодирование блока: {block}\n"

            received = [int(bit) for bit in block]
            corrected = received.copy()
            syndrome = [0] * m

            # Вычисляем начальный синдром
            remainder = self.polynomial_division(block, ''.join(map(str, g)))
            syndrome = [int(bit) for bit in remainder.zfill(m)]
            steps += f"Начальный синдром: {''.join(map(str, syndrome))}\n"

            # Основной цикл декодирования
            for shift in range(n):
                current_syndrome = ''.join(map(str, syndrome))
                steps += f"\nШаг {shift + 1}: Текущий синдром: {current_syndrome}\n"

                # Проверяем, соответствует ли синдром известной ошибке
                if current_syndrome in error_patterns:
                    error_pos = error_patterns[current_syndrome]
                    steps += f"Найдена ошибка в позиции {error_pos + 1}\n"

                    # Исправляем ошибку
                    corrected[error_pos] ^= 1
                    steps += f"Исправленный блок: {''.join(map(str, corrected))}\n"

                    # Пересчитываем синдром после исправления
                    remainder = self.polynomial_division(''.join(map(str, corrected)), ''.join(map(str, g)))
                    syndrome = [int(bit) for bit in remainder.zfill(m)]
                    steps += f"Новый синдром: {''.join(map(str, syndrome))}\n"

                # Циклический сдвиг и вычисление нового синдрома
                feedback = syndrome[0]
                syndrome = syndrome[1:] + [0]

                if feedback:
                    for i in range(m):
                        syndrome[i] ^= g[i + 1]

                steps += f"После сдвига: синдром = {''.join(map(str, syndrome))}\n"

            # После всех итераций получаем информационные биты
            decoded_block = ''.join(map(str, corrected[:k]))
            decoded_blocks.append(decoded_block)
            steps += f"\nДекодированный блок: {decoded_block}\n"

        decoded_data = ''.join(decoded_blocks)

        # Преобразуем бинарные данные обратно в текст
        try:
            # Удаляем возможные нули в конце
            decoded_data = decoded_data.rstrip('0')
            # Дополняем до целого числа байт
            if len(decoded_data) % 8 != 0:
                decoded_data = decoded_data.ljust((len(decoded_data) // 8 + 1) * 8, '0')

            chars = []
            for i in range(0, len(decoded_data), 8):
                byte = decoded_data[i:i + 8]
                if len(byte) == 8:
                    chars.append(chr(int(byte, 2)))
            decoded_text = ''.join(chars)
        except:
            decoded_text = decoded_data

        return decoded_text, steps

    def poly_to_matrix(self, poly_str, n, k):
        g = [int(bit) for bit in poly_str]
        m = len(g) - 1
        G = []
        for i in range(k):
            row = [0] * i + g + [0] * (k - i - 1)
            row = row[:n]
            G.append(row)
        return G

    def matrix_to_poly(self, matrix):
        n = len(matrix[0])
        k = len(matrix)
        last_row = matrix[-1]
        binary_str = ''.join(str(bit) for bit in last_row)
        binary_str = binary_str.lstrip('0')
        if not binary_str:
            binary_str = '0'
        return binary_str


if __name__ == "__main__":
    app = CyclicCodeApp()
    app.run()
