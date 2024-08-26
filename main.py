import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class Solver:
    def __init__(self, system_DU):
        '''
        param
        -----
        system_DU: function_object
                функция с системой ДУ (объявляет пользователь)
        t: list
                временной отрезок
        y: list
                хранит искомые функции
        '''
        self.system = system_DU
        self.t = [] # время
        self.y = [] # опред. ф-ии

    def solve(self, nu, end_time, step, t_eval=None, args=()):
        '''
        Решатель
        param
        -----
        nu: list
                начальные условия
        end_time: float
                время окончания интегрирования
        step: float
                шаг интегрирования
        t_eval: list
                массив временных точек для индивидуального решения
        args: tuple
                внешние параметры для передачи в систему ДУ
        '''
        p1, p2 = args
        if t_eval is None:
            self.t = np.linspace(0, end_time, int(end_time / step))
        else:
            self.t = t_eval
        self.y = odeint(self.system, nu, self.t, args=(p1, p2))

    def plot_solution(self,
                      func_numb=0,
                      fig_size=(12,8),
                      x_scale=None,
                      y_scale=None,
                      labels_name=None,
                      title=None):
        '''
        Графически отображает решение
        params
        ------
        func_numb: int
                номер найденной функции в self.y
        fig_size: tuple
                размер области графика - (length, width)
        x_scale: tuple
                масштаб по X - (x_min, x_max)
        y_scale: tuple
                масштаб по Y - (y_min, y_max)
        labels_name: tuple
                подписи по осям - (X, Y)
        title: str
                название графика
        '''
        fig, ax = plt.subplots(figsize=fig_size, layout='tight')
        
        ax.grid(which='major', color='#DDDDDD', linewidth=1.5)
        ax.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=1)
        ax.minorticks_on()
        ax.grid(True)
        
        ax.plot(self.t, self.y[:, func_numb], color='blue', linewidth=3)
        if not(x_scale is None):
            ax.set_xlim(x_scale[0], x_scale[1])
        if not(y_scale is None):
            ax.set_ylim(y_scale[0], y_scale[1])

        if not(labels_name is None):
            plt.xlabel(labels_name[0], fontsize=15, fontweight="bold")
            plt.ylabel(labels_name[1], fontsize=15, fontweight="bold")
        if not(title is None):
            plt.title(title, fontsize=15, fontweight="bold")


