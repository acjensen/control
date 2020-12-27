''' Mechanical and thermal energy conversions '''
from sympy import symbols, lambdify, Eq, Symbol
from sympy.core.numbers import Zero
import numpy as np
# x = symbols('x')
# expr = x*x
# f = lambdify(x, expr, 'numpy')
# r=f(np.array([0]))
# print(r)

system_energy_dot, hand_energy_dot, shaft_energy_dot = symbols(["system_energy_dot", "hand_energy_dot", "shaft_energy_dot"])
conservation_of_energy = Eq(system_energy_dot, hand_energy_dot + shaft_energy_dot)
print("conservation_of_energy:", conservation_of_energy)

hand_specific_heat = 3.5 # kJ/(kg K)
