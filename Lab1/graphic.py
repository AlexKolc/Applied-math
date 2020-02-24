import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class Graphic:
    def __init__(self):
        pass

    def histogram(self, ax, data, n_bins=10):
        ax.set_title("Histogram")
        ax.set_ylabel("Frequency * " + str(len(data)))
        ax.set_xlabel("Value")
        ax.hist(data, bins=n_bins, color='#539caf', edgecolor='black')
        # ax1.grid(axis='y', linestyle=':', linewidth='0.5')
        ax.minorticks_on()
        ax.grid(which='major', linestyle=':', linewidth=0.25)
        ax.grid(which='minor', linestyle=':', linewidth=0.125)
        return ax

    def empirical(self, ax, data):
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

    def build_hist_and_emp(self, data, n_bins=10, file="graphics.png"):
        fig, (ax1, ax2) = plt.subplots(
            nrows=2, ncols=1,
            figsize=(8, 10)
        )
        ax1 = self.histogram(ax1, data)
        ax2 = self.empirical(ax2, data)

        fig.savefig(file)
