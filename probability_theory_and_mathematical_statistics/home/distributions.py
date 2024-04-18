import matplotlib.pyplot as plt


def plot_frequency_polygon(data):  # Печать полигона частот
    data_counts = {}
    for value in data:
        if value in data_counts:
            data_counts[value] += 1
        else:
            data_counts[value] = 1

    values = sorted(data_counts.keys())
    frequencies = [data_counts[value] for value in values]  # Update frequencies to display count

    plt.figure(figsize=(10, 6))
    plt.plot(values, frequencies, linestyle='-')  # Plot values against frequencies
    plt.xlabel('Значения выборки')
    plt.ylabel('Количество совпадений')
    plt.title('Полигон частот')
    plt.grid(True)

    plt.show()


def plot_histogram(data):  # Печать гистограммы
    plt.hist(data, bins=25)
    plt.xlabel('Значения выборки')
    plt.ylabel('Высота')
    plt.title('Гистограмма (25 отрезков)')
    plt.grid(True)
    plt.show()
