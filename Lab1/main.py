# coding=utf-8
import time

from statistic import Statistic
from graphic import Graphic


def main():
    stat = Statistic()
    stat.load_data("data.txt")
    # print(stat.get_data())

    gr = Graphic()
    gr.build_hist_and_emp(stat.get_data())

    print("Среднее значение выборки: %.3f" % (stat.find_average_sample_value()))
    print("Выборочная дисперсия: %.3f" % (stat.find_selective_dispersion()))
    print("Стандартная ошибка: %.3f" % (stat.find_standard_error()))
    print("Мода: ", stat.find_mode())
    print("Медиана: ", stat.find_median())
    print("Квартили: ", (stat.find_quartiles()))
    q1, q2, q3 = stat.find_quartiles()
    gr.build_box_plot(stat.get_data()
                      , q1, q2, q3
                      , stat.find_min()
                      , stat.find_max()
                      )
    print("Ящик с усами построен. ")
    print("Стандартное отклонени: %.3f" % (stat.find_standard_deviation()))
    print("Эксцесс: %.3f" % (stat.find_kurtosis()))
    print("Асимметричность: %.3f (%s)" % (stat.find_skewness()))
    print("Минимум: ", (stat.find_min()))
    print("Максимум: ", (stat.find_max()))

    print("\nПроверка гипотезы H_0:")
    stat.pearson_criterion()

    print("\nДоверительный интервал матожидания: (%.3f; %.3f)" % (stat.expected_value_interval()))
    print("\nДоверительный интервал среднеквадратичного "
          "отклонения: (%.3f; %.3f)" % (stat.standard_deviation_interval()))


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
