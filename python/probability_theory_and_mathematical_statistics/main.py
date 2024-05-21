from python.probability_theory_and_mathematical_statistics.home import (count_seconds_from_file, compute_average,
                                                                        filter_data,
                                                                        compute_variance,
                                                                        adjust_variance,
                                                                        compute_std_dev,
                                                                        get_variation_range, plot_histogram,
                                                                        plot_frequency_polygon)
from pprint import pprint

general_data = count_seconds_from_file()
selected_data = filter_data(general_data)
var_range = get_variation_range(selected_data)
mean_value = compute_average(var_range)
dispersion_value = compute_variance(var_range, mean_value)
corrected_dispersion = adjust_variance(dispersion_value, selected_data)
std_dev = compute_std_dev(dispersion_value)
correct_std_dev = compute_std_dev(corrected_dispersion)
print(f'Выборка из Генеральной Совокупности: {selected_data}')
print()
print(f'Вариационный ряд выборки: {var_range}')
print()
print(f'Среднее значение выборки: {mean_value}')
print(f'Дисперсия выборки: {dispersion_value}')
print(f'Дисперсия исправленная: {corrected_dispersion}')
print(f'Среднее квадратичное отклонение выборки: {std_dev}')
print(f'Среднее квадратичное отклонение исправленное: {correct_std_dev}')

# Здесь не обязательно выводить полигон частот и гистограмму
plot_frequency_polygon(var_range)
plot_histogram(var_range)

print("n = ", len(selected_data))
