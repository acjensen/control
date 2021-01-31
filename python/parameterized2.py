from sympy.solvers.ode.systems import canonical_odes
from sympy import *
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass


class Flow():
    ''' Mass / Energy flow '''
    pass


def my_plot(tout, yout, params, xlbl='time / a.u.', ylabel=None, analytic=None):
    fig, axes = plt.subplots(1, 2 if analytic else 1, figsize=(14, 4))
    axes = np.atleast_1d(axes)
    for i in range(yout.shape[1]):
        axes[0].plot(tout, yout[:, i], label='y%d' % i)
    if ylabel:
        axes[0].set_ylabel(ylabel)
    for ax in axes:
        ax.set_xlabel(xlbl)
    if analytic:
        axes[0].plot(tout, analytic(tout, yout, params), '--')
        axes[1].plot(tout, yout[:, 0] - yout[0] *
                     np.exp(-params[0]*(tout-tout[0])))
        if ylabel:
            axes[1].set_ylabel('Error in ' + ylabel)


def analytic(tout, yout, params):
    return yout[0, 0]*np.exp(-params[0]*tout)


def main():
    '''
    model FirstOrder
    parameter Real c=1 "Time constant";
    Real x (start=10) "An unknown";
    equation
    der(x) = -c*x "A first order differential equation";
    end FirstOrder;
    '''

    def canonical():
        ''' m*xdd + k*x = 0 '''
        t, x = symbols('t x')
        m, k = symbols('m k')
        x = Function('x')(t)
        funcs = [x]
        eqs = [Eq(m*x.diff(t).diff(t) + k*x, 0)]
        print(eqs)
        can = canonical_odes(eqs, funcs, t)
        print(can)

    @dataclass
    class MasterModel():
        """ MasterModel includes the environment and any/all implementations
        of controls, sensors, engine configs, etc"""
        states: []
        equations: []
        maps_tunes_ovs_params: []

    def symbolic():
        ''' Future: determine control interface vs plant change '''

        # Set up the problem.
        t, x = symbols('t x')
        x = Function('y')(t)
        c = symbols('c')
        dxdt = x.diff(t)
        eq = Eq(dxdt, -c*x)

        # Solve symbolically.
        print(dsolve(eq))

        # Parameterize this control system / dynamic system
        maps_tunes_ovs_params = [c]
        states = [x]
        equations = [eq]
        return MasterModel(states, equations, maps_tunes_ovs_params)

    def numeric():

        # set up the problem.
        def rhs(x, t, c):
            return -c*x
        tout = np.linspace(0, 2e9, 100)
        x0 = 3  # initial condition
        params = (1.78e-9,)  # 1 parameter, decay constant of tritium

        # Solve numerically.
        # yout = euler_fw(rhs, y0, tout, params)
        xout, info = odeint(rhs, x0, tout, params, full_output=True)
        my_plot(tout, xout, params, analytic=analytic)
        plt.show()
        print("Number of function evaluations: %d" % info['nfe'][-1])

    def master_model():
        return symbolic()

    def simulate(compiled_model, overrides):
        """ Simulate the compiled model. """
        return 0

    def compile(model):
        """Compile the model to C.
        In reality everything after this step is "dynamic"...
        In other words, to use it, you need to query/anticipate the generated interface.
        Ideally we would have access to the original paramters.
        If not, this compilation step should generate a "Protobuffer" (basically an API
        for other programming languages to use.)
        """
        return model

    my_model = master_model()
    # "FORCAST"
    # Intermediate compile step.
    # You must specify the variants to compile.
    c_param = my_model.maps_tunes_ovs_params[0]
    my_model.equations[0].subs([(c_param, 1.78e-9)])

    # "COMPILE"
    # We now have a "workorder", which is really just a set of maps/tunes/ov/param
    # generated from the huge optimization process.
    my_compiled_model = compile(my_model)
    result = simulate(my_compiled_model)

    # "Wiring Harness"

    canonical()

# sympy.solvers.ode.systems.canonical_odes


if __name__ == "__main__":
    main()
