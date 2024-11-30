import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class Solver:
    def __init__(self, system_DU: object) -> object:
        """
        Конструктор для класса Solver

        Args:
            system_DU (function): Функция, представляющая систему ДУ,
            решение которой необходимо получить
        Returns:
            object: объект класса Solver
        """
        self.system = system_DU
        self.t = [] # время
        self.y = [] # найденные функции

    def solve(self, nu: tuple, end_time: float, step: float, t_eval:list = None) -> None:
        """
        Функция решателя, получающая решение для `self.system`
        Данный решатель получает решение с постоянным шагом, если не
        переданы временные точки интегрирования в параметр t_eval

        Args:
            nu (tuple): набор начальных условий
            end_time (float): время окончания интегрирования
            step (float): шаг решателя
            t_eval (list, optional): Заданные пользователем временные 
            точки интегрирования. Defaults to None.
        
        Returns:
            None
        """
        if t_eval is None:
            self.t = np.linspace(0, end_time, int(end_time / step))
        else:
            self.t = t_eval
        self.y = odeint(self.system, nu, self.t)

    def eiler(self, end_time: float, nu: tuple, acc: float) -> tuple:
        """
        Численное решение ДУ методом Эйлера

        Args:
            end_time (float): время окончания интегрирования
            nu (tuple): набор начальных условий
            acc (float): Начальный шаг интегрирования

        Returns:
            tuple: Набор временных точек и решения
        """
        step = acc**(1/2)
        t_pnt, sol_y, sol_z = [0.0], [nu[0]], [nu[1]]
        while t_pnt[-1] < end_time:    
            next_y = sol_y[-1] + step * self.system([sol_y[-1], sol_z[-1]], t_pnt[-1])[0]
            next_z = sol_z[-1] + step * self.system([sol_y[-1], sol_z[-1]], t_pnt[-1])[1]
            next_y2n = sol_y[-1] + step / 2 * self.system([sol_y[-1], sol_z[-1]], t_pnt[-1])[0]
            next_z2n = sol_z[-1] + step / 2 * self.system([sol_y[-1], sol_z[-1]], t_pnt[-1])[1]
            if abs(next_y2n - next_y) < acc:
                t_pnt.append(t_pnt[-1] + step)
                sol_y.append(next_y)
                sol_z.append(next_z)
                step = 2 * step
            else:
                step = step / 2
                continue
        return t_pnt, sol_y, sol_z
    
    def plot_solution(self,
                      func_numb=0,
                      fig_size=(12,8),
                      x_scale=None,
                      y_scale=None,
                      labels_name=None,
                      title=None) -> None:
        """
        Функция визуализация решения

        Args:
            func_numb (int, optional): номер найденной функции в self.y. Defaults to 0.
            fig_size (tuple, optional): размер области графика - (length, width). Defaults to (12,8).
            x_scale (_type_, optional): масштаб по X - (x_min, x_max). Defaults to None.
            y_scale (_type_, optional):  масштаб по Y - (y_min, y_max). Defaults to None.
            labels_name (_type_, optional): подписи по осям - (X, Y). Defaults to None.
            title (_type_, optional): название графика. Defaults to None.
        """
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


