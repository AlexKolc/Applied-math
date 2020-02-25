# coding=utf-8
import numpy as np
from scipy import stats
from scipy import special

from scipy.stats import chi2


class Statistic:
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
        asv = self.find_average_sample_value()
        return np.sum((np.array(self.data) - asv) ** 2) / (self.n - 1)

    # стандартная ошибка
    def find_standard_error(self):
        """Метод для вычисления стандартной ошибки."""
        sd = self.find_selective_dispersion()
        return np.sqrt(sd / self.n)

    # мода
    def find_mode(self):
        """Метод для вычисления моды."""
        value, count = np.unique(self.data, return_counts=True)
        return [value[i] for i in np.where(count == count[count.argmax()])]

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
        dispersion = self.find_selective_dispersion()
        return np.sqrt(dispersion)

    # эксцесс
    def find_kurtosis(self):
        """Метод для вычисления коэффициента эксцесса."""
        asv = self.find_average_sample_value()
        deviation = self.find_standard_deviation()
        moment4 = np.sum((np.array(self.data) - asv) ** 4) / self.n
        return moment4 / (deviation ** 4) - 3

    # Асимметричность
    def find_skewness(self):  # ????
        """Метод для вычисления коэффициента ассиметричности."""
        asv = self.find_average_sample_value()
        deviation = self.find_standard_deviation()
        moment3 = np.sum((np.array(self.data) - asv) ** 3) / self.n
        skewness = moment3 / (deviation ** 3)

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

    def split_data(self, n_bins=10):
        """Метод разбивающий датасет на интервалы одинаковой длины
        с подсчетом элементов входящих в каждый интервал"""
        eps = 1e-10
        min_d = self.find_min()
        max_d = self.find_max()
        h = (max_d - min_d + eps) / n_bins

        inter, count = [], []
        for i in range(n_bins):
            if i == 0:
                inter.append(min_d)
                inter.append(min_d + h)
            else:
                inter.append(inter[-1] + h)
            greater = np.greater_equal(self.data, inter[-2])
            less = np.less(self.data, inter[-1])
            count.append(np.count_nonzero(greater == less))
            # print(inter[-2], inter[-1], count[-1])
        # print(len(self.data), np.sum(count))
        return inter, count

    def laplace_function(self, x):
        """Метод расчитывающий значение функции Лапласа в x"""
        # helped https://stackoverflow.com/questions/56016484/how-to-calculate-laplace-function-in-python-3
        return special.erf(x / 2 ** 0.5) / 2

    def pearson_criterion(self, alpha=0.025):
        """Метод приверки гипотезы H0 с помощью критерия Пирсона."""
        inter, count = self.split_data(9)

        asv = self.find_average_sample_value()
        disp = np.sqrt(self.find_selective_dispersion())

        theor_freq = []
        n = len(count)
        inter[0] = -np.inf
        inter[-1] = np.inf
        # print("   xi      xi1    Fi      Fi1      n'       n")
        for i in range(len(inter) - 1):
            inter[i + 1] -= asv
            inter[i + 1] /= disp
            pi = self.laplace_function(inter[i + 1]) - self.laplace_function(inter[i])
            theor_freq.append(len(self.data) * pi)
            # print("%6.3f  %6.3f  %6.3f  %6.3f  %6.3f %6d" % (inter[i], inter[i + 1]
            #                                                  , self.laplace_function(inter[i])
            #                                                  , self.laplace_function(inter[i + 1])
            #                                                  , theor_freq[-1], count[i]))
        count = np.array(count)
        theor_freq = np.array(theor_freq)
        chi2_observed = np.sum((count - theor_freq) ** 2 / theor_freq)
        k = n - 3
        chi2_critical = chi2.ppf(1 - alpha, k)
        print("Наблюдаемое значение: %.3f" % (chi2_observed))
        print("Критическое значение %.3f" % (chi2_critical))

        if chi2_observed < chi2_critical:
            print("Наблюдаемое < критического => ")
            print("Нет оснований отвергнуть гипотезу H_0 о нормальном "
                  "распределении генеральной совокупности.")
        else:
            print("Наблюдаемое > критического =>")
            print("Гипотезу H_0 отвергаем.")

    def expected_value_interval(self, gamma=0.95):
        asv = self.find_average_sample_value()
        n = len(self.data)
        s = np.sqrt(n / (n - 1) * self.find_selective_dispersion())
        t = stats.t.ppf(gamma, n - 1)
        left = asv - (t * s) / np.sqrt(n)
        right = asv + (t * s) / np.sqrt(n)
        return left, right

    def standard_deviation_interval(self, gamma=0.95):
        n = len(self.data)
        s = np.sqrt(n / (n - 1) * self.find_selective_dispersion())
        chi_1 = np.sqrt(chi2.ppf((1 - gamma) / 2, n - 1))
        chi_2 = np.sqrt(chi2.ppf(1 - (1 - gamma) / 2, n - 1))
        left = (np.sqrt(n - 1) * s) / chi_2
        right = (np.sqrt(n - 1) * s) / chi_1
        return left, right