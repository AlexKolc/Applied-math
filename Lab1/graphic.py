# coding=utf-8
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class Graphic:
    """
        Класс для построения графиков
    """

    def __init__(self):
        pass

    def histogram(self, ax, data, n_bins=10):
        """Метод для построения гистограммы"""
        ax.set_title("Histogram")
        ax.set_ylabel("Frequency * " + str(len(data)))
        ax.set_xlabel("Value")
        ax.hist(data, bins=n_bins, color='#539caf', edgecolor='black')
        # ax1.grid(axis='y', linestyle=':', linewidth='0.5')
        ax.minorticks_on()
        ax.grid(which='major', linestyle=':', linewidth=0.25)
        ax.grid(which='minor', linestyle=':', linewidth=0.125)
        # ax.set_xticks(np.unique(data))
        return ax

    def empirical_with_points(self, ax, data):
        """Метод для построения графика эмпирической функции распределения"""
        ax.set_title("Empirical distribution function graph")
        ax.set_ylabel("F(x)")
        ax.set_xlabel("x")
        # ax2.grid(True, linestyle=':', linewidth='0.5')
        ax.minorticks_on()
        ax.grid(which='major', linestyle=':', linewidth=0.25)
        ax.grid(which='minor', linestyle=':', linewidth=0.125)

        value, count = [], []
        for x in np.unique(data):
            value.append(x)
            count.append(np.count_nonzero(np.less_equal(data, x) == True))

        x_points_opened = []
        y_points_opened = []
        x_points_closed = []
        y_points_closed = []
        first_last = 5  # для первой и последней линии
        for i in range(len(value) + 1):
            if i == 0:
                x = np.linspace(value[i] - first_last, value[i], 2)
                y = [count[i] / len(data), count[i] / len(data)]
                x_points_opened.append(value[i])
                y_points_opened.append(count[i] / len(data))
            elif i == len(value):
                x = np.linspace(value[-1], value[-1] + first_last, 2)
                y = [count[-1] / len(data), count[-1] / len(data)]
                x_points_closed.append(value[-1])
                y_points_closed.append(count[-1] / len(data))
            else:
                x = np.linspace(value[i - 1], value[i], 2)
                y = [count[i] / len(data), count[i] / len(data)]
                x_points_opened.append(value[i])
                y_points_opened.append(count[i] / len(data))
                x_points_closed.append(value[i - 1])
                y_points_closed.append(count[i] / len(data))
            ax.plot(
                x, y,
                linewidth=1,
                color='blue'
            )

        ax.plot(x_points_closed, y_points_closed, 'ro', color='blue', alpha=0.75)

        df = pd.DataFrame({'x': np.array(x_points_opened),
                           'y': np.array(y_points_opened)})
        ax.scatter(df.x.values, df.y.values, facecolors='none', edgecolors='blue', alpha=1)
        return ax

    def empirical_arrows(self, ax, data):
        """Метод для построения графика эмпирической функции распределения (в виде стрелок)"""
        ax.set_title("Empirical distribution function graph")
        ax.set_ylabel("F(x)")
        ax.set_xlabel("x")
        # ax2.grid(True, linestyle=':', linewidth='0.5')
        ax.minorticks_on()
        ax.grid(which='major', linestyle=':', linewidth=0.25)
        ax.grid(which='minor', linestyle=':', linewidth=0.125)
        # ax.set_xticks(np.unique(data))

        value, count = [], []
        for x in np.unique(data):
            value.append(x)
            count.append(np.count_nonzero(np.less_equal(data, x) == True))

        first_last = 5  # для первой и последней линии
        for i in range(len(value) + 1):
            if i == 0:
                x = value[i]
                y = count[i] / len(data)
                dx = -first_last
                dy = 0
            elif i == len(value):
                x = value[-1] + first_last
                y = count[-1] / len(data)
                dx = -first_last
                dy = 0

                ax.plot(
                    [value[-1], value[-1]], [count[-1] / len(data), 0],
                    linewidth=0.6,
                    color='black',
                    linestyle='--'
                )
            else:
                x = value[i]
                y = count[i] / len(data)
                dx = value[i - 1] - value[i]
                dy = 0

                ax.plot(
                    [value[i - 1], value[i - 1]], [count[i] / len(data), 0],
                    linewidth=0.6,
                    color='black',
                    linestyle='--'
                )
            ax.arrow(x, y, dx, dy,
                     width=0.001,
                     length_includes_head=True,
                     head_width=0.015,
                     head_length=0.3,
                     color='black',
                     overhang=0
                     )
            ax.set_ylim(bottom=0, top=1.05)
        return ax

    def build_box_plot(self, data, q1, q2, q3, min_x, max_x, file="box_plot.png"):
        fig, ax = plt.subplots()
        ax.set_title("Box plot")
        # ax2.grid(True, linestyle=':', linewidth='0.5')
        ax.minorticks_on()
        ax.grid(which='major', linestyle=':', linewidth=0.25)
        ax.grid(which='minor', linestyle=':', linewidth=0.125)

        ax.boxplot(data)
        ax.text(1.2, min_x - 0.1, "min")
        ax.text(1.2, max_x - 0.1, "max")
        ax.text(1.2, q1 - 0.1, "quartile 1")
        ax.text(1.2, q2 - 0.1, "median")
        ax.text(1.2, q3 - 0.1, "quartile 3")
        ylim = ax.get_ylim()
        xlim = ax.get_xlim()
        ax.plot([0, 1.18], [max_x, max_x], linewidth=0.6, color='black', linestyle='--', alpha=0.3)
        ax.plot([0, 1.18], [min_x, min_x], linewidth=0.6, color='black', linestyle='--', alpha=0.3)
        ax.plot([0, 1.18], [q1, q1], linewidth=0.6, color='black', linestyle='--', alpha=0.3)
        ax.plot([0, 1.18], [q2, q2], linewidth=0.6, color='orange', linestyle='--', alpha=0.3)
        ax.plot([0, 1.18], [q3, q3], linewidth=0.6, color='black', linestyle='--', alpha=0.3)
        ax.set_ylim(ylim)
        ax.set_xlim(xlim)
        # plt.show()
        fig.savefig(file)

    def build_hist_and_emp(self, data, n_bins=10, file="graphics.png"):
        """Метод для построения 2х графиков в одном файле"""
        fig, (ax1, ax2) = plt.subplots(
            nrows=2, ncols=1,
            figsize=(8, 10)
        )
        ax1 = self.histogram(ax1, data)
        ax2 = self.empirical_arrows(ax2, data)

        fig.savefig(file)
