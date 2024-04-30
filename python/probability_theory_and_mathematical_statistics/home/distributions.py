import matplotlib.pyplot as plt


def plot_frequency_polygon(data):
    """
    Рисует полигон частот для данных.

    Параметры:
    data (list): Список чисел.

    Возвращает:
    None
    """
    data_counts = {}
    for value in data:
        if value in data_counts:
            data_counts[value] += 1
        else:
            data_counts[value] = 1

    values = sorted(data_counts.keys())
    frequencies = [data_counts[value] for value in values]

    plt.figure(figsize=(10, 6))
    plt.plot(values, frequencies, linestyle='-')
    plt.xlabel('Значения выборки')
    plt.ylabel('Количество совпадений')
    plt.title('Полигон частот')
    plt.grid(True)
    plt.show()


def plot_histogram(data):
    """
    Рисует гистограмму для данных.

    Параметры:
    data (list): Список чисел.

    Возвращает:
    None
    """
    plt.hist(data, bins=25)
    plt.xlabel('Значения выборки')
    plt.ylabel('Высота')
    plt.title('Гистограмма (25 отрезков)')
    plt.grid(True)
    plt.show()
