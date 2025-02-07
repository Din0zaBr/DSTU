from probability_theory_and_mathematical_statistics.home import (count_seconds_from_file, compute_average,
                                                                 filter_data,
                                                                 compute_variance,
                                                                 adjust_variance,
                                                                 compute_std_dev,
                                                                 get_variation_range, plot_histogram,
                                                                 plot_frequency_polygon,
                                                                 calculate_length)

general_data = count_seconds_from_file()
selected_data = filter_data(general_data)
print(f'Выборка из Генеральной Совокупности: {selected_data}')

var_range = get_variation_range(selected_data)
print(f'Вариационный ряд выборки: {var_range}')

mean_value = compute_average(var_range)
print(f'Среднее значение выборки: {mean_value}')

dispersion_value = compute_variance(var_range, mean_value)
print(f'Дисперсия выборки: {dispersion_value}')

corrected_dispersion = adjust_variance(dispersion_value, selected_data)
print(f'Дисперсия исправленная: {corrected_dispersion}')

std_dev = compute_std_dev(dispersion_value)
print(f'Среднее квадратичное отклонение выборки: {std_dev}')

correct_std_dev = compute_std_dev(corrected_dispersion)
print(f'Среднее квадратичное отклонение исправленное: {correct_std_dev}')

# Здесь не обязательно выводить полигон частот и гистограмму
plot_frequency_polygon(var_range)
plot_histogram(var_range)

print("n = ", calculate_length(selected_data))
