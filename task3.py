import math
from task1 import make_y_i
from task2 import find_amount_of_intervals
from task2 import make_n_x


# Пусть
# Гипотетический закон распределения равномерный
# Гипотеза H0 - распределение равномерное

# Функция распределения гипотетического закона распределения (для моего варианта)
def F0(y):
    return y / 3


# Теоретическая вероятность попадания случайной величины в данный интервал,
# при условии, что гипотеза H0 верна
def integral_f_0(Ai, Bi):
    return F0(Bi) - F0(Ai)


def intervals(n, y_i):
    # Использовала равноинтервальный статистический ряд
    amount_of_intervals = find_amount_of_intervals(n)
    # Получаем длину интервала
    len_of_interval = (y_i[-1] - y_i[0]) / amount_of_intervals
    # Находим границы каждого из интервалов
    A_i = []
    B_i = []
    i = 0
    temp = y_i[0]
    while i != amount_of_intervals:
        A_i.append(temp)
        temp = A_i[-1] + len_of_interval
        i += 1
    for i in range(1, len(A_i)):
        B_i.append(A_i[i])
    B_i.append(A_i[-1] + len_of_interval)
    # Находим кол-во СВ, которые попали в данный интервал
    n_i = []
    amount_of_nums_in_interval = 0
    ind = 0
    for i in range(0, len(A_i)):
        for j in range(ind, len(y_i)):
            if B_i[i] >= y_i[j] >= A_i[i]:
                amount_of_nums_in_interval += 1
                ind = j
        n_i.append(amount_of_nums_in_interval)
        amount_of_nums_in_interval = 0
    return A_i, B_i, n_i, amount_of_intervals


# Критерий Присона
def pearson_criterion(n, y_i):
    A_i, B_i, p_j_pr, amount_of_intervals = intervals(n, y_i)
    CHI_PR = 0
    for j in range(0, amount_of_intervals):
        p_j = integral_f_0(A_i[j], B_i[j])
        CHI_PR += ((p_j_pr[j] - n * p_j) ** 2) / n * p_j
    # k = 19, alpha = 0.01
    CHI2 = 27.2
    if CHI_PR <= CHI2:
        return True
    else:
        return False


def kolmogorov_criterion(n, y_i):
    A_i, B_i, n_i, amount_of_intervals = intervals(n, y_i)
    n_i = [1] * n
    n_x = make_n_x(n_i)
    F_practical = list(map(lambda x: x / n, n_x))
    F_theoretical = list(map(lambda y: F0(y), y_i))
    Z = max([math.fabs(F_practical[i] - F_theoretical[i]) for i in range(0, n)])
    lam_pr = math.sqrt(n) * Z
    # alpha = 0.01
    lam = 1.63
    if lam_pr <= lam:
        return True
    else:
        return False


def mizes_criterion(n, y_i):
    A_i, B_i, n_i, amount_of_intervals = intervals(n, y_i)
    n_i = [1] * n
    n_x = make_n_x(n_i)
    F_practical = list(map(lambda x: x / n, n_x))
    F_theoretical = list(map(lambda y: F0(y), y_i))
    omega_pr = 0
    for i in range(0, n):
        omega_pr += (F_theoretical[i] - F_practical[i]) ** 2
    omega_pr += 1 / (12 * n)
    # alpha = 0.01
    omega = 0.744
    if omega_pr <= omega:
        return True
    else:
        return False


if __name__ == '__main__':
    n = 200
    y_i = make_y_i(n, -3, 3)
    pearson = pearson_criterion(n, y_i)
    if pearson:
        print("Гипотеза H0 верна по критерию согласия Присона")
    n = 30
    y_i = make_y_i(n, -3, 3)
    kolmogorov = kolmogorov_criterion(n, y_i)
    if kolmogorov:
        print("Гипотеза H0 верна по критерию согласия Колмогорова")
    mizes = mizes_criterion(n, y_i)
    if mizes:
        print("Гипотеза H0 верна по критерию согласия Мизеса")
