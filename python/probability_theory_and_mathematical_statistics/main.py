from python.probability_theory_and_mathematical_statistics.home import (count_seconds_from_file, calculate_mean,
                                                                        range_every_four_odd,
                                                                        calculate_dispersion,
                                                                        calculate_correct_dispersion,
                                                                        calculate_standard_deviation,
                                                                        variation_range, plot_histogram,
                                                                        plot_frequency_polygon)

general = count_seconds_from_file()
selection = range_every_four_odd(general)
variation_range = variation_range(selection)
mean = calculate_mean(variation_range)
dispersion = calculate_dispersion(variation_range, mean)
correct_dispersion = calculate_correct_dispersion(dispersion, selection)
standard_deviation = calculate_standard_deviation(dispersion)
correct_standard_deviation = calculate_standard_deviation(correct_dispersion)

print("Выборка из Генеральной Совокупности: {}".format(selection))
print('Вариационный ряд выборки: {}'.format(variation_range))
print('Среднее значение выборки: {}'.format(mean))
print('Дисперсия выборки: {}'.format(dispersion))
print('Дисперсия исправленная: {}'.format(correct_dispersion))
print('Среднее квадратичное отклонение выборки: {}'.format(standard_deviation))
print('Среднее квадратичное отклонение исправленное: {}'.format(correct_standard_deviation))

# Здесь не обязательно выводить полигон частот и гистограмму
plot_frequency_polygon(variation_range)
plot_histogram(variation_range)

print("n = ", len(selection))
