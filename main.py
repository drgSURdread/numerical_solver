import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, signal

class du_solver:
    def __init__(self, func) -> None:
        '''
        @args:
        func: система ДУ, которую неолбходимо решить;
        nu: начальные условия;
        t_0: начальный момент интегрирования
        '''
        self.__system = func

        # Results
        self.y_sol = [] #функция
        self.v_sol = [] #производная
        self.t_sol = []
    
    
    def __get_integrator(self, method: str):
        methods = {'RK45': integrate.RK45}
        assert method in methods.keys(), \
                'Данный решатель не поддерживает метод {}'.format(method)   
        return methods[method]

    def solution(self, method: str, nu: list, 
                 t_interval: tuple = [0.0, 100], 
                 max_step: float = 0.05) -> (list, list):
        '''
        Решатель системы ДУ.
        @args:
        method: Метод численного решения (RK45, )
        nu: Начальные условия;
        t_interval: Время интегрирования;
        max_step: Максимальный шаг интегрирования
        '''
        integrator = self.__get_integrator(method)(
                            self.__system, 
                            t_interval[0],
                            nu,
                            t_bound=t_interval[1],
                            max_step=max_step)
        while not(integrator.status == 'finished'):
            integrator.step()
            self.t_sol.append(integrator.t)
            self.y_sol.append(integrator.y[0])
            self.v_sol.append(integrator.y[1])
        return (self.t_sol, self.y_sol, self.v_sol)
    
    def __get_range(self, is_x: bool = False, is_y: bool = False):
        if is_x:
            return [self.t_sol[0], self.t_sol[len(self.t_sol) - 1]]
        else:
            return [min(self.y_sol), max(self.y_sol)]

    def plot_solution(self, x_range: list = None,
                            y_range: list = None,
                            color: str = 'b'):
        '''
        Рисует график численного решения ДУ
        @args:
        x_range: Диапазон вывода графика по оси абсцисс, по умолчанию программа сама выбирает масштаб
        y_range: Диапазон вывода графика по оси ординат, по умолчанию программа сама выбирает масштаб
        color: Цвет графика
        '''
        if x_range is None:
            x_range = self.__get_range(is_x=True)
        if y_range is None:
            y_range = self.__get_range(is_y=True)
        plt.rcParams["figure.figsize"] = (10,6)
        plt.plot(self.t_sol, self.y_sol, color)
        plt.xlim(x_range)
        plt.ylim(y_range)
        plt.xlabel('t')
        plt.ylabel('y')
        plt.grid(True)
        #plt.legend(['Численное решение'])
        #plt.title('Решение ДУ методом Рунге-Кутты 4-го порядка')
        plt.show()

    def lowpass_filter(self, cutoff_freq: float, poles: int = 5) -> list:
        '''
        Фильтр решения на низкие частоты
        @args:
        '''
        filter_ = signal.butter(poles, cutoff_freq, 'lowpass', output='sos')
        filtered_data = signal.sosfiltfilt(filter_, list(zip(self.t_sol, self.y_sol)))
        return filtered_data
    
    #TODO: Добавить постройку фазового портрета для системы ДУ
    def plot_phase_portrait(self, x_range: list = [-5, 5],
                            y_range: list = [-5, 5],
                            step_x: int = 10,
                            step_y: int = 10,
                            t_final: float = 1500,
                            color: str = 'r'):
        '''
        Рисует фазовый портрет решения ДУ
        @args:
        x_range: Диапазон вывода графика по оси абсцисс, по умолчанию программа сама выбирает масштаб
        y_range: Диапазон вывода графика по оси ординат, по умолчанию программа сама выбирает масштаб
        color: Цвет графика;
        step_x: Шаг начального условия функции;
        step_y: Шаг начального условия производной;
        t_final: Время окончания интегрирования
        '''
        #TODO: Поправить, проблемы с перебором значений
        plt.rcParams["figure.figsize"] = (10,6)
        plt.grid(True)
        for x0 in np.linspace(x_range[0], x_range[1], step_x):
            for y0 in np.linspace(y_range[0], y_range[1], step_y):
                y_0 = [x0, y0]
                t_0 = 0
                t_final = 1500
                t, y, v = self.solution(method='RK45', 
                                    nu=y_0,
                                    t_interval=[t_0, t_final],
                                    max_step=0.5)
                plt.plot(t, v, color)
        plt.show()



    
def function(t, y):
    '''
    Функция, которую должен написать сам пользователь. 
    Система уравнений или просто ДУ, которое необходимо решить
    '''
    return [
        y[1],
        -3/2*0.00101**2/285.14*(363.86-233.96)*np.sin(2*(y[0] - 0.004))/np.cos(2*0.004)
        ]


obj = du_solver(function)
obj.plot_phase_portrait(x_range=[-np.pi, np.pi], y_range=[-0.001, 0.001])
