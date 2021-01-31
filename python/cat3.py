from scipy.optimize import differential_evolution

'''
Consider a SINGLE customer at a SINGLE location at a two operating points, with a SINGLE emission type.

Map out the functional depenencies. Limit indirection (if you see multiple arguments, there could be another function.)

This idea can be continued to encompass the entire enterprise.

WE ARE OPTIMIZING A CONVERGING DYNAMIC SYSTEM. IFF WE can define
a system that fills in these "functions" for us is a kind of "adaptive"
neural network that changes itself

- EmissionRequirement = f(EngineBore, Location)
- EngineBore = f(Engine)
- MaxPowerRequirement = maximize
- FuelConsumptionRequirement = minimize
- MaxPowerSimulation = f(Engine, EmissionRequirement)
- MaxPower = f(MaxPowerSimulation)
- LongetevityRequirement = maximize
- Engine = f(ExistingEngines) # development cost?
- LifeUse = f(MaxPower, Application)
- LifeSimulation = f(LifeUse, Engine)
- Longetevity = f(LifeSimulation)
- FuelConsumption = f(LifeUse, Engine)

'''


class Locations():

    class India():
        pass

    class Japan():
        pass


def emission_requirement(engine_bore: EngineBore, location: Location):
    if location == Locations.India:
        if engine_bore > 10:
            return 1.0
        else:
            return 0.5
    elif location == Locations.Japan:
        return 2.0


def engine_bore(engine: Engine):
    return engine.bore


simulate(engine, emission_requirement)


def max_power(engine: Engine, emission_requirement: EmissionRequirement):

    # MIN/MAX


def max_power_requirement():
    ''' Maximize? '''


def fuel_consumption_requirement():
    ''' minimize? '''
