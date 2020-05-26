import math
import random
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from task1 import make_y_i


# Получаем ряд накопленных частот
def make_n_x(n_i):
    n_x = []
    temp = n_i[0]
    for i in range(1, len(n_i)):
        n_x.append(temp)
        temp += n_i[i]
    n_x.append(temp)
    return n_x


# Функция для определения кол-ва интервалов, на которые нужно разбить выборку
def find_amount_of_intervals(n):
    if n <= 100:
        amount_of_intervals = int(math.sqrt(n))
    else:
        amount_of_intervals = int(3 * math.log(n, 2))
    return amount_of_intervals


# Используется для равновероятностного метода.
# Если размер выборки нацело не делится на кол-во интервалов, то
# Случайным образом выбираем число из выборки и удаляем его
def check_amount_of_intervals(n, amount_of_intervals, y):
    while n % amount_of_intervals != 0:
        temp = random.choice(y)
        y.remove(temp)
        n -= 1
    return amount_of_intervals, y, n


# Середины интервалов для построения полигона
def make_middle_of_intervals(A_i, B_i):
    middles = []
    for i in range(0, len(A_i)):
        middles.append(A_i[i] + ((B_i[i] - A_i[i]) / 2))
    return middles


# Графики и таблицы
def visualisation(A_i, B_i, n_i, f_i):
    xlist = []
    ylist = []
    for i in range(0, amount_of_intervals):
        xlist.append(A_i[i])
        xlist.append(B_i[i])
        ylist.append(f_i[i])
        ylist.append(f_i[i])
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(
        nrows=1, ncols=4,
        figsize=(8, 4)
    )
    ax1.plot(xlist, ylist)
    ax1.set_title("Гистограмма")
    mid = make_middle_of_intervals(A_i, B_i)
    ax2.plot(mid, f_i, "g-o")
    ax2.set_title("Полигон относительных частот")
    n_x = make_n_x(n_i)
    F_practical = list(map(lambda x: x / n, n_x))
    ax3.step(n_x, F_practical, "g-o", where="pre")
    ax3.set_title("Эмпирическая F")
    ylist = []
    for i in range(0, len(xlist)):
        ylist.append(1 / 3)  # плотность для конкретной функции
    ax4.plot(xlist, ylist)
    ax4.set_title("Теоретическая плотность распределения")
    table1 = go.Figure(
        data=[
            go.Table(header=dict(values=['Ai', 'Bi', 'Количество СВ на данном интервале', 'Значения F эмпирической']),
                     cells=dict(values=[A_i, B_i, n_i, F_practical]))
        ])
    return table1, plt


if __name__ == '__main__':
    # Lab2
    n = int(input())
    y_i = make_y_i(n, -3, 3)
    # Равноинтервальный
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
    n_i_lr2 = []
    amount_of_nums_in_interval = 0
    ind = 0
    for i in range(0, len(A_i)):
        for j in range(ind, len(y_i)):
            if B_i[i] >= y_i[j] >= A_i[i]:
                amount_of_nums_in_interval += 1
                ind = j
        n_i_lr2.append(amount_of_nums_in_interval)
        amount_of_nums_in_interval = 0
    # Вычисляем среднюю плотность вероятности для каждого интервала
    f_i = []
    for i in range(0, amount_of_intervals):
        f_i.append(n_i_lr2[i] / (n * len_of_interval))
    table1, plt1 = visualisation(A_i, B_i, n_i_lr2, f_i)

    # Равновероятностный
    amount_of_intervals = find_amount_of_intervals(n)
    # Вычисляем оптимальное кол-во СВ
    amount_of_intervals, y_i, n = check_amount_of_intervals(n, amount_of_intervals, y_i)
    amount_of_nums_in_interval = n // amount_of_intervals
    n_i_lr2 = []
    for i in range(0, amount_of_intervals):
        n_i_lr2.append(amount_of_nums_in_interval)
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
    # Вычисляем длину каждого из интервалов
    h_i = []
    for i in range(0, len(A_i)):
        h_i.append(B_i[i] - A_i[i])
    # Вычисляем среднюю плотность вероятности для каждого интервала
    f_i = []
    for i in range(0, amount_of_intervals):
        f_i.append(n_i_lr2[i] / (n * h_i[i]))
    table2, plt2 = visualisation(A_i, B_i, n_i_lr2, f_i)

    table1.write_html('tmp1.html', auto_open=True)
    table2.write_html('tmp2.html', auto_open=True)
    plt1.show()
    plt2.show()
