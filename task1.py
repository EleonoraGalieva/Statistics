import numpy as np
import matplotlib.pyplot as plt
import math
import plotly.graph_objects as go


# Var 3
# Y=|x|; a=-3; b=3;

# Random Variable Yi
def make_y_i(n, a, b):
    sigma_i = np.random.rand(n)
    x_i = list(map(lambda x: x * (b - a) + a, sigma_i))
    y_i = list(map(lambda y: math.fabs(y), x_i))
    y_i.sort()
    return y_i

def M(a, b):
    return (a + b) / 2


def D(a, b):
    return ((b - a) ** 2)/12


def M(a, b):
    return (a + b) / 2


def D(a, b):
    return (b - a) ** 2


if __name__ == '__main__':
    # Lab1
    a = -3
    b = 3
    n = int(input())
    # Формирование выборки СВ
    y_i = make_y_i(n, a, b)
    # Тк вероятность того, что в выборке встретится два одинаковых числа -> 0, будем считать,
    # что частота появления каждой величины = 1
    n_i = [1] * n
    # Посчитаем кол-во наборов, при которых случайное значение Y<y
    n_x = []
    temp = 0
    for i in range(0, n):
        temp += n_i[i]
        n_x.append(temp)
    # Найдем эмпирическую функцию распределения
    F_practical = list(map(lambda x: x / n, n_x))
    # И теоритическую, через формулы нахождения функции СВ (посчитала для конкретной функции вручную)
    F_theoretical = list(map(lambda y: 1 / 3 * y, y_i))
    # Строим графики и таблицы
    figure = plt.figure()
    subplot = figure.add_subplot(111)
    subplot.plot([y_i[0] - 1, y_i[0]], [0, 0], color="green")
    subplot.scatter(y_i[0], 0, color="green")
    subplot.plot(y_i, F_theoretical)
    subplot.step(y_i, F_practical, "g-o", where="post")
    subplot.plot([y_i[-1], y_i[-1] + 1], [1, 1], color="green")
    fig = go.Figure(
        data=[
            go.Table(header=dict(values=['Вариационный ряд', 'Эмпирическая функция распределения',
                                         'Теоретическая функция распределения']),
                     cells=dict(values=[y_i, F_practical, F_theoretical]))
        ])
    fig.write_html('tmp.html', auto_open=True)
    plt.show()
