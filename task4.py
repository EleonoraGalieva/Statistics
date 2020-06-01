import scipy.stats as sts
import math
import matplotlib.pyplot as plt
from task1 import make_y_i
from task1 import D
from task1 import M


def evaluation_of_M(n, y_i):
    temp = 0
    for i in range(0, n):
        temp += y_i[i]
    temp /= n
    return temp


def evaluation_of_D(n, y_i, m):
    temp = 0
    for i in range(0, n):
        temp += (y_i[i] - m) ** 2
    temp /= (n - 1)
    return temp


def intervals_for_M(n, d, m):
    tt = sts.t(n)
    arr = tt.rvs(1000000)
    delta1 = sts.mstats.mquantiles(arr, prob=0.9) * math.sqrt(d / (n - 1))
    delta2 = sts.mstats.mquantiles(arr, prob=0.94) * math.sqrt(d / (n - 1))
    delta3 = sts.mstats.mquantiles(arr, prob=0.98) * math.sqrt(d / (n - 1))
    delta4 = sts.mstats.mquantiles(arr, prob=0.99) * math.sqrt(d / (n - 1))
    interval_for_m_1 = [m - delta1, m + delta1]
    print("Доверительный интервал для мат ожидания при уровне значимости 0.9 и n = " + str(n) + ": " + str(
        interval_for_m_1))
    interval_for_m_2 = [m - delta2, m + delta2]
    print(
        "Доверительный интервал для мат ожидания при уровне значимости 0.94 и n = " + str(n) + ": " + str(
            interval_for_m_2))
    interval_for_m_3 = [m - delta3, m + delta3]
    print(
        "Доверительный интервал для мат ожидания при уровне значимости 0.98 и n = " + str(n) + ": " + str(
            interval_for_m_3))
    interval_for_m_4 = [m - delta4, m + delta4]
    print(
        "Доверительный интервал для мат ожидания при уровне значимости 0.99 и n = " + str(n) + ": " + str(
            interval_for_m_4))
    # m+delta-m+delta=2delta
    #plt.plot([0.9, 0.94, 0.98, 0.99], [2 * delta1, 2 * delta2, 2 * delta3, 2 * delta4])
    #plt.show()
    return [interval_for_m_1, interval_for_m_2, interval_for_m_3, interval_for_m_4]


def intervals_for_D(n, d, m):
    CHI2 = sts.chi2(n - 1)
    arr = CHI2.rvs(1000000)
    delta1 = sts.mstats.mquantiles(arr, prob=[0.025, 0.975])
    delta2 = sts.mstats.mquantiles(arr, prob=[0.01, 0.99])
    delta3 = sts.mstats.mquantiles(arr, prob=[0.005, 0.995])
    interval_for_d_1 = [d - (n - 1) * d / delta1[1], d + (n - 1) * d / delta1[0]]
    print("Доверительный интервал для мат ожидания при уровне значимости 0.9 и n = " + str(n) + ": " + str(
        interval_for_d_1))
    interval_for_d_2 = [d - (n - 1) * d / delta2[1], d + (n - 1) * d / delta2[0]]
    print(
        "Доверительный интервал для мат ожидания при уровне значимости 0.94 и n = " + str(n) + ": " + str(
            interval_for_d_2))
    interval_for_d_3 = [d - (n - 1) * d / delta3[1], d + (n - 1) * d / delta3[0]]
    print(
        "Доверительный интервал для мат ожидания при уровне значимости 0.98 и n = " + str(n) + ": " + str(
            interval_for_d_3))
    # m+delta-m+delta=2delta
    #plt.plot([0.95, 0.98, 0.99],
             # [interval_for_d_1[1] - interval_for_d_1[0], interval_for_d_2[1] - interval_for_d_2[0],
             #  interval_for_d_3[1] - interval_for_d_3[0]])
    #plt.show()
    return [interval_for_d_1, interval_for_d_2, interval_for_d_3]


def intervals_task_1(n):
    y_i = make_y_i(n, -3, 3)
    m = evaluation_of_M(n, y_i)
    print("Точечная оценка мат ожидания при n = " + str(n) + ": " + str(m))
    S = evaluation_of_D(n, y_i, m)
    print("Точечная оценка дисперсии при n = " + str(n) + ": " + str(S))
    arr = intervals_for_M(n, S, m)
    D_theoretical = D(-3, 3)
    intervals_for_M(n, D_theoretical, m)
    return arr[0][1] - arr[0][0] #Для построения графика зависимости величины доверительного интервала от объема выборки
                                 #использовала значения интервала для точечной дисперсии при уровне значимости 0.9


def intervals_task_2(n):
    y_i = make_y_i(n, -3, 3)
    m = evaluation_of_M(n, y_i)
    print("Точечная оценка мат ожидания при n = " + str(n) + ": " + str(m))
    S = evaluation_of_D(n, y_i, m)
    print("Точечная оценка дисперсии при n = " + str(n) + ": " + str(S))
    arr = intervals_for_D(n, S, m)
    M_theoretical = M(-3, 3)
    intervals_for_D(n, S, M_theoretical)
    return arr[0][1] - arr[0][0]


if __name__ == '__main__':
    interval1 = intervals_task_1(20)
    interval2 = intervals_task_1(50)
    interval3 = intervals_task_1(70)
    interval4 = intervals_task_1(100)
    interval5 = intervals_task_1(150)
    #plt.plot([20, 50, 70, 100, 150], [interval1, interval2, interval3, interval4, interval5])
    #plt.show()

    interval1 = intervals_task_2(20)
    interval2 = intervals_task_2(50)
    interval3 = intervals_task_2(70)
    interval4 = intervals_task_2(100)
    interval5 = intervals_task_2(150)
    plt.plot([20, 50, 70, 100, 150], [interval1, interval2, interval3, interval4, interval5])
    plt.show()
