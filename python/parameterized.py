from sympy import *


# class Parameter():
#     ''' Constant parameters. '''

#     def __init__(self, **kwargs):
#         self.__dict__ = kwargs


# class Derivatives():
#     pass


# class Derivative():
#     ''' '''


# class Real():
#     ''' '''


# class Eq():
#     pass


# class Model():
#     pass


# def main():
#     '''
#     model FirstOrder
#     parameter Real c=1 "Time constant";
#     Real x (start=10) "An unknown";
#     equation
#     der(x) = -c*x "A first order differential equation";
#     end FirstOrder;
#     '''
#     pass

#     c = Parameter(name='c', value=1)
#     x = Real(name='x', start=10)
#     eq = Eq(name='A first order differential equation.',
#             lhs=Derivative(state=x), rhs=-c*x)

#     simulate(Eq)

def main2():

    x = RealNumber()
    print(x)
    print("dklasfjd")
