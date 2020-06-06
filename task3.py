import math
from task1 import make_y_i
from task2 import find_amount_of_intervals, check_amount_of_intervals, make_n_x


# Пусть
# Гипотетический закон распределения равномерный
# Гипотеза H0 - распределение равномерное

# Функция распределения гипотетического закона распределения (для моего варианта)
def F0(y):
    return y / 3


def intervals(n, y_i):
    # Равновероятностный
    amount_of_intervals = find_amount_of_intervals(n)
    # Вычисляем оптимальное кол-во СВ
    amount_of_intervals, y_i, n = check_amount_of_intervals(n, amount_of_intervals, y_i)
    amount_of_nums_in_interval = n // amount_of_intervals
    n_i = []
    for i in range(0, amount_of_intervals):
        n_i.append(amount_of_nums_in_interval)
    # Находим границы каждого из интервалов
    A_i = []
    B_i = []
    i = 0
    while i != n:
        A_i.append(y_i[i])
        i += amount_of_nums_in_interval
    for i in range(1, len(A_i)):
        B_i.append(A_i[i])
    B_i.append(y_i[-1])
    return A_i, B_i, n_i, amount_of_intervals


# Критерий Пирсона
def pearson_criterion(n, y_i):
    A_i, B_i, p_j_pr, amount_of_intervals = intervals(n, y_i)
    CHI_PR = 0
    for j in range(0, amount_of_intervals):
        # Теоретическая вероятность попадания СВ в j-тый интервал при условии, что гипотеза H0 верна
        p_j = (B_i[j] - A_i[j]) / (y_i[-1] - y_i[0])
        CHI_PR += ((p_j_pr[j] - n * p_j) ** 2) / (n * p_j)
    # k = 19, alpha = 0.01
    CHI2 = 36.2
    if CHI_PR <= CHI2:
        return True
    else:
        return False


def kolmogorov_criterion(n, y_i):
    F_theoretical = list(map(lambda y: F0(y), y_i))
    d = []
    for i in range(0, n):
        d1 = math.fabs(i / n - F_theoretical[i])
        d2 = math.fabs(F_theoretical[i] - (i - 1) / n)
        d.append(max(d1, d2))
    Z = max(d)
    lam_pr = math.sqrt(n) * Z
    # alpha = 0.01
    lam = 1.63
    if lam_pr <= lam:
        return True
    else:
        return False


def mizes_criterion(n, y_i):
    F_theoretical = list(map(lambda y: F0(y), y_i))
    omega_pr = 0
    for i in range(0, n):
        omega_pr += (F_theoretical[i] - (i - 0.5) / n) ** 2
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
        print("Гипотеза H0 верна по критерию согласия Пирсона")
    n = 200
    y_i = make_y_i(n, -3, 3)
    kolmogorov = kolmogorov_criterion(n, y_i)
    if kolmogorov:
        print("Гипотеза H0 верна по критерию согласия Колмогорова")
    mizes = mizes_criterion(n, y_i)
    if mizes:
        print("Гипотеза H0 верна по критерию согласия Мизеса")
