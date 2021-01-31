from tensorflow.keras import layers
from tensorflow import keras
import tensorflow as tf
from scipy import optimize
import matplotlib.pyplot as plt
import matplotlib.style as style
import numpy as np
from math import sqrt, sin, cos
from dataclasses import dataclass, field
from typing import List, Set
style.use('fast')


def runge_kutta_4th_order(f):
    """Finds value of y for a given x using step size h
    and initial value y0 at x0."""

    def parameterized_runge_kutta(x, u, d):

        k1 = f(x, u, d)
        k2 = f(x + 0.5 * k1, u, d)
        k3 = f(x + 0.5 * k2, u, d)
        k4 = f(x + k3, u, d)

        return x + (1.0 / 6.0)*(k1 + 2*k2 + 2*k3 + k4)

    return parameterized_runge_kutta


def euler(f):
    """Finds value of y for a given x using step size h
    and initial value y0 at x0."""

    def parameterized_euler(x, u, d):
        return x + f(x, u, d)

    return parameterized_euler


@dataclass
class TimeSetting:
    """ note: this is basically a parameterized function... """
    start: float = 0
    stop: float = 3
    step: float = .01


def times(ts: TimeSetting):
    return np.arange(ts.start, ts.stop, ts.step)


@dataclass
class Result:
    x: np.array
    cost: np.array
    tracking_error_squared: np.array
    d: np.array
    u: np.array



def simulate(plant, solver, times, x0, controller, x_desired, d, possible_states, cost=None):
    """ Runs the simulation. """
    solver = solver(plant)
    x = x0

    result = Result(
        x=np.full_like(times, 0),
        cost=np.full_like(times, 0),
        tracking_error_squared=np.full_like(times, 0),
        d=np.full_like(times, 0),
        u=np.full_like(times, 0),
    )

    for t_idx, t in enumerate(times):
        u = controller(x_desired[t_idx], x)
        x = solver(x, u, d[t_idx])
        # cost and u can be calculated offline instead of here for machine learning / DOE run
        if cost:
            result.cost[t_idx], result.tracking_error_squared[t_idx] = cost(
                x, x_desired[t_idx], u)
        result.u[t_idx] = u
        result.x[t_idx] = x

    return result
