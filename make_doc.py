from solver import Solver
import matplotlib.pyplot as plt
from docxtpl import DocxTemplate, InlineImage

c = 0.0
omega = 1.0

def equations(y: list, t: float) -> list:
    dydt = y[1]
    dzdt = -c * y[1] - omega ** 2 * y[0]
    return [dydt, dzdt]

def save_fig(file_name: str, sol: Solver) -> None:
    fig, ax = plt.subplots(figsize=(6,3), layout='tight')
    ax.grid(True)
    
    ax.plot(sol.t, sol.y[0, :], color='blue', linewidth=3)
    fig.savefig('images/' + file_name + '.png')

tpl = DocxTemplate('Шаблон.docx')
context = dict()
fig_all, ax_all = plt.subplots(figsize=(6,3), layout='tight') # График со всеми движениями
ax_all.grid(True)

for i in range(4):
    context[f'omega_{i}'] = omega
    context[f'demp_{i}'] = c
    sol = Solver(equations)
    sol.solve(nu=(1.0, 0.0), end_time=10.0, step=0.001)
    save_fig(f'img_{i}', sol)
    ax_all.plot(sol.t, sol.y[0, :], label=f'c={c}', linewidth=3)

    omega += 0.2
    c += 0.05
    context[f'img_{i}'] = InlineImage(tpl, image_descriptor=f'images/img_{i}.png')

ax_all.legend()
fig_all.savefig('images/img_4.png')
context['img_4'] = InlineImage(tpl, image_descriptor='images/img_4.png')

tpl.render(context)
tpl.save('result.docx')

