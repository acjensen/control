# "Interface" in programming is a set of methods.
# "Interface" in physical modelling & control is a set of signals (a struct in Go)

from dataclasses import dataclass


class Test():
    pass


class Cycle():
    pass


class Emissions():
    pass


class Master():
    pass


class MasterPlant():
    pass


class MasterController():
    pass


class Controller():
    ''' Control signals are forced states. '''
    pass


class CausalInterface():
    ''' Simulink "Signal" (1 directional) '''
    pass


class AcausalInterface():
    ''' Modelica "Flow" (2 directional) '''
    pass


def human(process):
    return process


def process():
    customer()
    cost = 1
    return cost


def main():
    while True:
        new_process = human(process)
        process = new_process
