# Similar: tax bracket
from dataclasses import dataclass
'''
goal: select engine that satisfies optimization problem (lowest fuel consumption, highest power, within emiss constaints.)
'''


@dataclass
class Cycle():
    seconds: int
    limit: float


@dataclass
class Engine():
    max_power: float


def emission_cycle(location, application):
    ''' How long at max power and what the limit is. '''
    if application == 'non-road':
        seconds = 5
        limit = 1.0
        return Cycle(seconds, limit)


def app_cycle():
    seconds = 1
    limit = 2
    return Cycle(seconds, limit)


def simulate(cycle: Cycle, engine: Engine):
    ''' Simulate the cycle with a given engine to get total fuel, total emissions. '''
    emissions = engine.max_power * cycle.seconds
    fuel = engine.max_power * cycle.seconds
    return emissions, fuel


def cost_function(result):
