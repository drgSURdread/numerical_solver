# %%
from solver import Solver
# %%
# Протестируем функционал класса на простом ДУ
# %%
def equations(y, t):
    dydt = y[1]
    dzdt = -0.1 * y[1] - 3 * y[0]
    return [dydt, dzdt]
# %%
nu = (0.1, 0.0) # Начальные условия
end_time = 10.0 # Время конца решения

sol = Solver(equations) # Объект решателя
# %%
sol.solve(
    nu, 
    end_time=end_time,
    step=0.1
)
# %%
# Значение функции
sol.plot_solution(
    func_numb=0,
    labels_name=("Время, c", "Значение функции")
)
# %%
# Значение производной
sol.plot_solution(
    func_numb=1,
    labels_name=("Время, c", "Значение функции")
)

# %% 
# Решение уравнения `equation` методом Эйлера
# %%
sol.eiler(
    end_time=end_time,
    nu=nu,
    acc=1e-5,
)
# %%
# Значение функции
sol.plot_solution(
    func_numb=0,
    labels_name=("Время, c", "Значение функции")
)
# %%
# Значение функции
sol.plot_solution(
    func_numb=1,
    labels_name=("Время, c", "Значение функции")
)