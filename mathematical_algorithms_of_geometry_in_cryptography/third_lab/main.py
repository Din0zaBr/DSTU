import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
from typing import Tuple, List, Optional


def calculate_discriminant(a: float, b: float) -> float:
    """
    Вычисляет дискриминант эллиптической кривой y² = x³ + ax + b.
    
    Формула: D = 4a³ + 27b²
    
    Args:
        a: Коэффициент a
        b: Коэффициент b
    
    Returns:
        Значение дискриминанта
    """
    return 4 * a ** 3 + 27 * b ** 2


def is_singular(discriminant: float, tolerance: float = 1e-10) -> bool:
    """
    Проверяет, является ли эллиптическая кривая сингулярной.
    
    Кривая сингулярна, если дискриминант равен нулю.
    
    Args:
        discriminant: Значение дискриминанта
        tolerance: Допустимая погрешность для сравнения с нулем
    
    Returns:
        True, если кривая сингулярна, False иначе
    """
    return abs(discriminant) < tolerance


def find_singular_points(a: float, b: float) -> List[Tuple[float, float]]:
    """
    Находит сингулярные точки эллиптической кривой.
    
    Сингулярные точки находятся из условия: 3x² + a = 0 и y² = x³ + ax + b = 0
    
    Args:
        a: Коэффициент a
        b: Коэффициент b
    
    Returns:
        Список сингулярных точек (x, y)
    """
    singular_points: List[Tuple[float, float]] = []
    discriminant = calculate_discriminant(a, b)
    
    # Если дискриминант не равен нулю, сингулярных точек нет
    if not is_singular(discriminant):
        return singular_points
    
    # Находим x из условия 3x² + a = 0
    if abs(a) < 1e-10:  # a ≈ 0
        x = 0.0
    else:
        # x² = -a/3
        if -a / 3 >= 0:
            x = (-a / 3) ** 0.5
        else:
            return singular_points  # Нет действительных решений
    
    # Проверяем, что точка лежит на кривой (y² = x³ + ax + b = 0)
    y_squared = x ** 3 + a * x + b
    if abs(y_squared) < 1e-10:  # y² ≈ 0
        singular_points.append((x, 0.0))
        # Если есть вторая точка (симметричная)
        if x != 0:
            x2 = -x
            y_squared2 = x2 ** 3 + a * x2 + b
            if abs(y_squared2) < 1e-10:
                singular_points.append((x2, 0.0))
    
    return singular_points


def split_curve(x: np.ndarray, y2: np.ndarray) -> Tuple[List[List[float]], List[List[float]]]:
    """
    Разбивает кривую на сегменты, где y² >= 0 (кривая существует).
    
    Args:
        x: Массив значений x
        y2: Массив значений y² = x³ + ax + b
    
    Returns:
        Кортеж из двух списков: (segments_x, segments_y) - сегменты кривой
    """
    segments_x: List[List[float]] = []
    segments_y: List[List[float]] = []
    current_x: List[float] = []
    current_y: List[float] = []

    for i in range(len(x)):
        if y2[i] >= 0:
            current_x.append(float(x[i]))
            current_y.append(float(np.sqrt(y2[i])))
        else:
            # Завершаем текущий сегмент, если он есть
            if current_x:
                segments_x.append(current_x)
                segments_y.append(current_y)
                current_x = []
                current_y = []

    # Добавляем последний сегмент, если он есть
    if current_x:
        segments_x.append(current_x)
        segments_y.append(current_y)

    return segments_x, segments_y


def plot_elliptic_curve() -> None:
    """
    Строит график эллиптической кривой и проверяет её на сингулярность.
    """
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите числовые значения a и b!")
        return

    # Вычисляем дискриминант
    discriminant = calculate_discriminant(a, b)
    
    # Проверяем сингулярность
    singular = is_singular(discriminant)
    singular_points = find_singular_points(a, b) if singular else []
    
    # Обновляем информацию о результате
    if singular:
        result_text = f"Кривая сингулярна.\nДискриминант: {discriminant:.5f}"
        if singular_points:
            result_text += f"\nСингулярные точки: {singular_points}"
        label_result.config(text=result_text, fg="red")
    else:
        label_result.config(
            text=f"Кривая НЕ сингулярна.\nДискриминант: {discriminant:.5f}",
            fg="green"
        )

    # Генерируем точки для построения графика
    x = np.linspace(-10, 10, 10000)
    y2 = x ** 3 + a * x + b

    # Создаем график
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True, linestyle='--', linewidth=0.5)

    # Разбиваем кривую на сегменты и строим
    segments_x, segments_y = split_curve(x, y2)

    for x_seg, y_seg in zip(segments_x, segments_y):
        ax.plot(x_seg, y_seg, 'r', linewidth=1.5, label='y² = x³ + ax + b' if x_seg == segments_x[0] else '')
        ax.plot(x_seg, [-y for y in y_seg], 'r', linewidth=1.5)

    # Отмечаем сингулярные точки
    if singular_points:
        sx, sy = zip(*singular_points)
        ax.scatter(sx, sy, color='#000000', s=5, marker='o',
                  zorder=5, label='Сингулярные точки', linewidths=2)

    ax.set_title(f"Эллиптическая кривая: y² = x³ + {a}x + {b}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.legend(loc='best')

    # Очищаем предыдущий график и добавляем новый
    for widget in frame_plot.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack()


def main() -> None:
    """Основная функция для создания GUI приложения."""
    global entry_a, entry_b, label_result, frame_plot
    
    root = tk.Tk()
    root.title("Эллиптические кривые")
    root.geometry("700x700")

    # Фрейм для элементов управления
    frame_controls = tk.Frame(root)
    frame_controls.pack(pady=10)

    tk.Label(frame_controls, text="Введите a:", font=("Arial", 10)).grid(row=0, column=0, padx=5)
    entry_a = tk.Entry(frame_controls, width=15, font=("Arial", 10))
    entry_a.grid(row=0, column=1, padx=5)
    entry_a.insert(0, "0")

    tk.Label(frame_controls, text="Введите b:", font=("Arial", 10)).grid(row=1, column=0, padx=5)
    entry_b = tk.Entry(frame_controls, width=15, font=("Arial", 10))
    entry_b.grid(row=1, column=1, padx=5)
    entry_b.insert(0, "0")

    btn_plot = tk.Button(
        frame_controls, 
        text="Построить график", 
        command=plot_elliptic_curve,
        font=("Arial", 10),
        bg="#4CAF50",
        fg="white",
        padx=10,
        pady=5
    )
    btn_plot.grid(row=2, columnspan=2, pady=10)

    # Метка для отображения результата
    label_result = tk.Label(
        root, 
        text="Введите параметры a и b, затем нажмите 'Построить график'", 
        font=("Arial", 11, "bold"),
        wraplength=600
    )
    label_result.pack(pady=10)

    # Фрейм для графика
    frame_plot = tk.Frame(root)
    frame_plot.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
