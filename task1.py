import numpy as np
import matplotlib.pyplot as plt
import math
import plotly.graph_objects as go


# Var 3
# Y=|x|; a=-3; b=3;

# Random Variable Yi
def make_y_i(n, a, b):
    sigma_i = np.random.sample(n)
    x_i = list(map(lambda x: x * (b - a) + a, sigma_i))
    y_i = list(map(lambda y: math.fabs(y), x_i))
    y_i.sort()
    return y_i

def M(a, b):
    return (a + b) / 2


def D(a, b):
    return ((b - a) ** 2)/12


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
    temp = 1
    for i in range(1, n + 1):
        n_x.append(temp)
        temp += 1
    # Найдем эмпирическую функцию распределения
    F_practical = list(map(lambda x: x / n, n_x))
    # И теоритическую, через формулы нахождения функции СВ (посчитала для конкретной функции вручную)
    F_theoretical = list(map(lambda y: 1 / 3 * y, y_i))
    # Строим графики и таблицы
    figure = plt.figure()
    subplot = figure.add_subplot(111)
    subplot.plot(y_i, F_theoretical)
    subplot.step(y_i, F_practical, "g-o", where="pre")
    fig = go.Figure(
        data=[
            go.Table(header=dict(values=['Эмпирическая функция распределения', 'Теоретическая функция распределения']),
                     cells=dict(values=[F_practical, F_theoretical]))
        ])
    fig.write_html('tmp.html', auto_open=True)
    plt.show()
