import time

from statistics import Statistics
from graphic import Graphic


def main():
    stat = Statistics()
    stat.load_data("data.txt")
    # print(stat.get_data())

    gr = Graphic()
    gr.build_hist_and_emp(stat.get_data())

    print("Среднее значение выборки: ", stat.find_average_sample_value())
    print("Выборочная дисперсия: ", stat.find_selective_dispersion())
    print("Стандартная ошибка: ", stat.find_standard_error())
    print("Мода: ", stat.find_mode())
    print("Медиана: ", stat.find_median())
    print("Квартили: ", (stat.find_quartiles()))
    # print("Квартили: ", (stat.find_quartiles()))
    print("Стандартное отклонени: ", (stat.find_standard_deviation()))
    print("Эксцесс: ", (stat.find_kurtosis()))
    print("Асимметричность: ", (stat.find_skewness()))
    print("Минимум: ", (stat.find_min()))
    print("Максимум: ", (stat.find_max()))


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
