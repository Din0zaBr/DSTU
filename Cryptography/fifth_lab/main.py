"""
Точка запуска приложения для шифра Гронсфельда.

Этот модуль содержит главную функцию для запуска графического интерфейса.
"""

import tkinter as tk
from gui import GronsfeldApp


def main() -> None:
    """
    Главная функция - запускает GUI приложение.
    """
    root: tk.Tk = tk.Tk()
    app: GronsfeldApp = GronsfeldApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
