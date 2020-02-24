# coding=utf-8
import numpy as np


class Statistics:
    """
        Класс для нахождения всяких статистических величин.
    """

    def __init__(self, ):
        self.data = []
        self.n = 0

    def load_data(self, file):
        """Метод для загрузки данных из файла."""
        with open(file) as f:
            for line in f:
                for x in line.split():
                    self.data.append(float(x))
        self.n = len(self.data)
        self.data = np.sort(self.data)

    def get_data(self):
        return self.data

    # среднее значение выборки
    def find_average_sample_value(self):
        """Метод для вычисления среднего значения выборки."""
        return np.sum(self.data) / self.n

    # Выборочная дисперсия
    def find_selective_dispersion(self):
        """Метод для вычисления выборочной дисперсии."""
        return np.sum(np.array(self.data) ** 2) / self.n - self.find_average_sample_value() ** 2

    # стандартная ошибка
    def find_standard_error(self):
        """Метод для вычисления стандартной ошибки."""
        return (self.find_selective_dispersion() * self.n
                / (self.n - 1)) / np.sqrt(self.n)

    # мода
    def find_mode(self):
        """Метод для вычисления моды."""
        value, count = np.unique(self.data, return_counts=True)
        return value[np.argmax(count)]

    # медиана
    def find_median(self, data=[]):
        """Метод для вычисления медианы."""
        if len(data) == 0:
            data = self.data
            n = self.n
        else:
            n = len(data)
        median = data[n // 2]
        if n % 2 == 0:
            median += data[n // 2 - 1]
            median /= 2
        return median

    # 1, 2, 3 квартили
    def find_quartiles(self):
        """Метод для вычисления квартилей."""
        data1 = self.data[:self.n // 2]
        data2 = self.data[self.n // 2:]
        q1 = self.find_median(data1)
        q2 = self.find_median()
        q3 = self.find_median(data2)
        return q1, q2, q3

    # ящик с усами
    def find_box_plot(self):
        """Метод для вычисления ящика с усами."""
        q1, _, q3 = self.find_quartiles()
        k = 1.5  # коэффициент, наиболее часто употребляемое значение которого равно 1,5
        X1 = q1 - k * (q3 - q1)
        X2 = q3 + k * (q3 - q1)
        ## це график
        return 0

    # стандартное отклонение
    def find_standard_deviation(self):
        """Метод для вычисления стандартного отклонения."""
        asv = self.find_average_sample_value()
        return np.sqrt(
            np.sum(np.array(self.data - asv) ** 2) / (self.n - 1)
        )

    # эксцесс
    def find_kurtosis(self):
        """Метод для вычисления коэффициента эксцесса."""
        asv = self.find_average_sample_value()
        return np.sqrt(
            np.sum(np.array(self.data - asv) ** 4) / self.n
        )

    # Асимметричность
    def find_skewness(self):  # ????
        """Метод для вычисления коэффициента ассиметричности."""
        asv = self.find_average_sample_value()
        skewness = (np.sum(np.array(self.data - asv) ** 3) / self.n) / (self.find_selective_dispersion() ** 3)
        result = "распределение "

        if np.abs(skewness) < 0.25:
            result += "незначительно"
        elif np.abs(skewness) > 0.5:
            result += "существенно "
        else:
            result += "умеренно "

        if skewness > 0:
            result += " скошено вправо"
        elif skewness < 0:
            result += " скошено влево"
        return skewness, result

    # минимум
    def find_min(self):
        """Метод для нахождения мининума."""
        return np.min(self.data)

    # максимум
    def find_max(self):
        """Метод для нахождения максимума."""
        return np.max(self.data)
