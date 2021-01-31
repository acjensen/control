import matplotlib.pyplot as plt
from functools import partial

dt = .1

times = range(start=0, stop=6, step=dt)


param = {
    'a': 2,
    'b': 1,
}


def x(time):
    state = time


def func(param, state, time):
    return param['b']*state*state + state*param['a'] + time


def simulate(func, state, init, times):
    for time in times:
        func(state=state(time), time=time)

    return states


simulate(func=partial(func, param), state=state, times=times)
