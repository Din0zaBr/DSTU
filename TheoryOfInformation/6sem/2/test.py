import customtkinter as ctk
from tkinter import messagebox


class ConvCodecApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Сверточный кодек")
        self.geometry("800x600")

        # Конфигурация стилей
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Переменные
        self.polynomials = []
        self.encoded_bits = ""

        # Создание виджетов
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для ввода параметров
        params_frame = ctk.CTkFrame(self)
        params_frame.pack(pady=10, padx=10, fill="x")

        # Поле для сумматоров
        ctk.CTkLabel(params_frame, text="Сумматоры (каждый на новой строке):").grid(row=1, column=0, padx=5, pady=5)
        self.poly_text = ctk.CTkTextbox(params_frame, height=100, width=200)
        self.poly_text.grid(row=1, column=1, columnspan=2, padx=5)

        # Поле ввода данных
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(input_frame, text="Исходные данные:").pack(anchor="w")
        self.input_entry = ctk.CTkTextbox(input_frame, height=50)
        self.input_entry.pack(fill="x", pady=5)

        # Кнопки действий
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Закодировать", command=self.encode).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Раскодировать", command=self.decode).pack(side="left", padx=5)

        # Поле вывода результатов
        output_frame = ctk.CTkFrame(self)
        output_frame.pack(pady=10, padx=10, fill="both", expand=True)

        ctk.CTkLabel(output_frame, text="Закодированные данные:").pack(anchor="w")
        self.encoded_text = ctk.CTkTextbox(output_frame, height=100)
        self.encoded_text.pack(fill="x", pady=5)

        ctk.CTkLabel(output_frame, text="Декодированные данные:").pack(anchor="w")
        self.decoded_text = ctk.CTkTextbox(output_frame, height=100)
        self.decoded_text.pack(fill="x", pady=5)

    def get_polynomials(self):
        try:
            poly_str = self.poly_text.get("1.0", "end").strip()
            return [[int(x) for x in line.split(",")] for line in poly_str.split("\n") if line]
        except:
            messagebox.showerror("Ошибка", "Некорректный формат сумматоров")
            return None

    def encode(self):
        try:
            # Получение параметров
            self.polynomials = self.get_polynomials()
            input_data = self.input_entry.get("1.0", "end").strip()

            # Определение типа входных данных
            if all(c in '01' for c in input_data):
                binary = input_data
            else:
                binary = text_to_binary(input_data)

            self.original_binary = binary
            encoded = convolutional_encode(binary, self.polynomials)
            self.encoded_bits = encoded
            self.encoded_text.delete("1.0", "end")
            self.encoded_text.insert("1.0", encoded)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def decode(self):
        try:
            # Получение закодированных данных
            encoded = self.encoded_text.get("1.0", "end").strip()

            # Декодирование
            decoded_bits = viterbi_decode(encoded, self.polynomials)

            # Попытка преобразовать в текст
            try:
                decoded = binary_to_text(decoded_bits)
                original_text = binary_to_text(self.original_binary)
                output = f"Результат:\nТекст: {decoded}\nБиты: {decoded_bits}"
                if decoded != original_text:
                    output += "\n\nОбнаружены неисправленные ошибки!"
                self.decoded_text.delete("1.0", "end")
                self.decoded_text.insert("1.0", f"Текст: {decoded}\nБиты: {decoded_bits}")
            except:
                self.decoded_text.delete("1.0", "end")
                self.decoded_text.insert("1.0", decoded_bits)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


# Вспомогательные функции кодека
def text_to_binary(text):
    """Переводит текст в двоичную строку (ASCII)"""
    return ''.join(f"{ord(c):08b}" for c in text)


def binary_to_text(binary):
    """Преобразует двоичную строку обратно в текст"""
    try:
        # Добавляем padding если необходимо
        padding = (8 - (len(binary) % 8)) % 8
        binary_padded = binary + '0' * padding

        chars = []
        for i in range(0, len(binary_padded), 8):
            byte = binary_padded[i:i + 8]
            chars.append(chr(int(byte, 2)))
        return ''.join(chars).rstrip('\x00')
    except Exception as e:
        return f"Ошибка декодирования: {str(e)}"


def convolutional_encode(input_bits, polynomials):
    """Сверточное кодирование"""
    if not input_bits:
        return ''

    max_register = max(max(p) for p in polynomials)
    registers = [0] * (max_register + 1)
    encoded = []

    for bit in input_bits:
        registers.insert(0, int(bit))
        registers.pop()

        for poly in polynomials:
            xor = 0
            for idx in poly:
                xor ^= registers[idx]
            encoded.append(str(xor))

    return ''.join(encoded)


def viterbi_decode(encoded_bits, polynomials):
    """Алгоритм Витерби с подробным выводом в консоль"""
    if not encoded_bits:
        return ''

    n_outputs = len(polynomials)
    max_register = max(max(p) for p in polynomials)
    n_states = 2 ** max_register
    states = [format(i, f'0{max_register}b') for i in range(n_states)]

    print("\n" + "═" * 50)
    print(f"Начало декодирования. Параметры:")
    print(f"Количество состояний: {n_states}")
    print(f"Длина закодированной последовательности: {len(encoded_bits)} бит")
    print(f"Количество шагов: {len(encoded_bits) // n_outputs}")

    path_metrics = {s: float('inf') for s in states}
    path_metrics['0' * max_register] = 0
    paths = {s: [] for s in states}

    for step in range(0, len(encoded_bits) // n_outputs):
        current_bits = encoded_bits[step * n_outputs: (step + 1) * n_outputs]
        new_metrics = {s: float('inf') for s in states}
        new_paths = {s: [] for s in states}

        print("\n" + "─" * 50)
        print(f"Шаг {step + 1}. Полученные биты: {current_bits}")

        for state in states:
            if path_metrics[state] == float('inf'):
                continue

            print(f"\nСостояние: {state} (метрика: {path_metrics[state]:.1f})")

            for input_bit in ['0', '1']:
                next_state = (input_bit + state)[:-1]
                tmp_registers = list(map(int, input_bit + state))

                # Вычисляем ожидаемые выходные биты
                expected = []
                for poly in polynomials:
                    xor = sum(tmp_registers[idx] for idx in poly) % 2
                    expected.append(str(xor))
                expected_str = ''.join(expected)

                # Вычисляем метрику Хэмминга
                metric = sum(1 for a, b in zip(current_bits, expected_str) if a != b)
                total_metric = path_metrics[state] + metric

                print(f"  Вход: {input_bit} -> Состояние: {next_state}")
                print(f"  Ожидаемые: {expected_str} vs Фактические: {current_bits}")
                print(f"  Метрика шага: {metric}, Общая метрика: {total_metric:.1f}")

                if total_metric < new_metrics[next_state]:
                    new_metrics[next_state] = total_metric
                    new_paths[next_state] = paths[state] + [input_bit]
                    print("  ✔ Обновление метрики")
                else:
                    print("  ✖ Метрика хуже текущей")

        path_metrics, paths = new_metrics, new_paths

    print("\n" + "═" * 50)
    print("Финальные метрики состояний:")
    for state in sorted(path_metrics, key=lambda x: path_metrics[x]):
        print(f"{state}: {path_metrics[state]:.1f} → {paths[state]}")

    final_state = min(path_metrics, key=path_metrics.get)
    result = ''.join(paths[final_state])
    print("\n" + "═" * 50)
    print(f"Выбран путь: {paths[final_state]}")
    print(f"Финальная метрика: {path_metrics[final_state]:.1f}")
    print(f"Результат декодирования: {result}")

    return result[:len(encoded_bits) // len(polynomials)]


if __name__ == "__main__":
    app = ConvCodecApp()
    app.mainloop()

