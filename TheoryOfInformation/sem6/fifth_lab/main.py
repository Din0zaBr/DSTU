import customtkinter as ctk
from tkinter import filedialog
from block_code import BlockCodeModule
from convolutional_code import ConvolutionalCodeModule

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class CommunicationChannelApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Настройка основного окна
        self.title("Система моделирования каналов связи")
        self.geometry("1280x720")
        self.minsize(1024, 600)

        # Создание переменных для хранения данных
        self.input_text = ""
        self.encoded_text = ""
        self.noisy_text = ""
        self.decoded_text = ""

        # Создание основных фреймов
        self.create_sidebar()
        self.create_main_frame()

        # Создание модулей для работы с кодами
        self.block_code_module = BlockCodeModule(self)
        self.convolutional_code_module = ConvolutionalCodeModule(self)

        # Показать стартовую страницу
        self.show_module("block_code")

    def create_sidebar(self):
        # Создание боковой панели
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)

        # Заголовок боковой панели
        self.sidebar_label = ctk.CTkLabel(self.sidebar_frame, text="Меню",
                                          font=ctk.CTkFont(size=18, weight="bold"))
        self.sidebar_label.pack(padx=20, pady=(20, 10))

        # Кнопка для перехода к модулю с блочными кодами
        self.block_code_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Блочные коды",
            font=ctk.CTkFont(size=14),
            height=40,
            command=lambda: self.show_module("block_code")
        )
        self.block_code_button.pack(padx=20, pady=10, fill="x")

        # Кнопка для перехода к модулю со сверточными кодами
        self.conv_code_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Сверточные коды",
            font=ctk.CTkFont(size=14),
            height=40,
            command=lambda: self.show_module("convolutional_code")
        )
        self.conv_code_button.pack(padx=20, pady=10, fill="x")

        # Разделитель
        self.separator = ctk.CTkLabel(self.sidebar_frame, text="", height=1)
        self.separator.pack(fill="x", padx=10, pady=10)

        # Информация о программе
        self.info_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Каналы связи v1.0\n\n© 2025",
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        self.info_label.pack(side="bottom", padx=20, pady=20)

    def create_main_frame(self):
        # Основной фрейм для содержимого
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def show_module(self, module_name):
        # Очистка основного фрейма
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Подсветка активной кнопки
        self.block_code_button.configure(
            fg_color=("#3B8ED0", "#1F6AA5") if module_name == "block_code" else "transparent",
            text_color=("white", "white") if module_name == "block_code" else ("gray85", "gray85")
        )
        self.conv_code_button.configure(
            fg_color=("#3B8ED0", "#1F6AA5") if module_name == "convolutional_code" else "transparent",
            text_color=("white", "white") if module_name == "convolutional_code" else ("gray85", "gray85")
        )

        # Отображение выбранного модуля
        if module_name == "block_code":
            self.block_code_module.create_widgets(self.main_frame)
        elif module_name == "convolutional_code":
            self.convolutional_code_module.create_widgets(self.main_frame)

    def load_text_from_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")
        return None


if __name__ == "__main__":
    app = CommunicationChannelApp()
    app.mainloop()
