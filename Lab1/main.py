import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from statistics import Statistics


def build_graphics(data, n_bins=10):
    # x_min = np.min(data)
    # x_max = np.max(data) + 0.3
    # l = 10
    # delta = (x_max - x_min) / l
    # n = len(data)
    #
    # si = [x_min]
    # pi = []
    # for i in range(l):
    #     si.append(si[-1] + delta)
    #     pi.append(np.count_nonzero(np.greater_equal(data, si[i]) == np.less(data, si[i + 1])))
    #     print(si[i], si[i+1], pi[i])

    fig, (ax1, ax2) = plt.subplots(
        nrows=2, ncols=1,
        figsize=(8, 10)
    )
    ax1.set_title("Histogram")
    ax1.set_ylabel("Frequency * " + str(len(data)))
    ax1.set_xlabel("Value")
    ax1.hist(data, bins=n_bins, color='#539caf', edgecolor='black')
    ax1.grid(axis='y', linestyle=':', linewidth='0.5')

    ax2.set_title("Empirical distribution function graph")
    ax2.set_ylabel("F(x)")
    ax2.set_xlabel("x")
    ax2.grid(axis='y', linestyle=':', linewidth='0.5')
    value, count = [], []
    for x in np.unique(data):
        value.append(x)
        count.append(np.count_nonzero(np.less_equal(data, x) == True))

    x_points = []
    y_points = []
    first_last = 5  # для первой и последней линии
    for i in range(len(value) + 1):
        if i == 0:
            x = np.linspace(value[i] - first_last, value[i], 2)
            y = [count[i] / len(data), count[i] / len(data)]
            x_points.append(value[i])
            y_points.append(count[i] / len(data))
        elif i == len(value):
            x = np.linspace(value[-1], value[-1] + first_last, 2)
            y = [count[-1] / len(data), count[-1] / len(data)]
            plt.plot([value[-1]], [count[-1] / len(data)], 'ro', color='blue')
        else:
            x = np.linspace(value[i - 1], value[i], 2)
            y = [count[i] / len(data), count[i] / len(data)]
            x_points.append(value[i])
            y_points.append(count[i] / len(data))
            plt.plot([value[i - 1]], [count[i] / len(data)], 'ro', color='blue')
        ax2.plot(
            x, y,
            linewidth=1,
            color='blue'
        )

    df = pd.DataFrame({'x': np.array(x_points),
                       'y': np.array(y_points)})
    ax2.scatter(df.x.values, df.y.values, facecolors='none', edgecolors='blue')
    # levels = np.linspace(0, 1, len(data) + 1)  # endpoint 1 is included by default
    # ax2.step(sorted(list(data) + [max(data)]), levels)
    # plt.show()
    fig.savefig("graphics.png")


def main():
    stat = Statistics()
    stat.load_data("data.txt")
    print(stat.get_data())

    build_graphics(stat.get_data())
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
