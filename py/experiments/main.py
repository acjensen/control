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


@dataclass
class Bound:
    lower: float
    upper: float


# def doe(list_of_range_or_set_or_pair, numeric_doe_method=None):

#     def genperm(theset):
#         """A generator which returns the permutations of the presented set."""
#         if (len(theset) <= 1):
#             yield theset
#         else:
#             for i in range(len(theset)):
#                 for restperm in genperm(theset[:i] + theset[i+1:]):
#                     yield [theset[i]] + restperm

#     for o in list_of_range_or_set_or_pair:
#         if type(o) is List:

#         if type(o) is Set:

#         if type(o) is Pair:


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
class Shaft:
    radius: float
    mass: float


@dataclass
class Hand:
    friction: float


@dataclass
class TimeSetting:
    """ note: this is basically a parameterized function... """
    start: float = 0
    stop: float = 3
    step: float = .01


def times(ts: TimeSetting):
    return np.arange(ts.start, ts.stop, ts.step)


def shaft_hand_plant(shaft: Shaft, hand: Hand):

    I = 1/2*shaft.mass*sqrt(shaft.radius)
    # shaft_energy = 1/2*I*angledot*angledot

    def parameterized_shaft_hand_plant(x, u, d):
        # shaft_energy_dot = stored rotational energy + friction work
        #
        # work = force * distance
        # work + hand_delta_thermal = der(system_energy) = 0
        # distance = radius*theta
        # theta and distance are infantesimal
        # system_energy_dot = hand_energy_dot + shaft_energy_dot = 0
        # Effectively transfer energy from rotating shaft to hand heat
        # how to quantify? modulate force of hand.
        # work = force*distance
        # workdot = force*distancedot
        # workdot = force*radius*thetadot
        #
        # now we can quantify the *energy distribution* within our system (the state)
        # as a function of current 'force' and previous state.
        #
        # essentially, there's now a function `x_next = f(force, x)`.
        #
        # now, lets find out what 'x' is:
        #
        # system_energy_dot = hand_energy_dot + shaft_energy_dot = 0
        # thermal_energy_dot + kinetic_energy_dot = 0
        #
        # when we derive by time... THATS when force comes in to play
        # there is another factor... internal param f modifies the
        # energy distribution/state.
        #
        # Actually lets assume in vacuum, no gravity, no thermal transfer...
        #
        # energy in + internal energy + energy out = 0
        #
        # d_torque + d_internal_energy + d_hand = 0
        #
        # where:
        #   d_torque is uncontrolled disturbance
        #   d_hand is controlled disturbance (removes energy... could be different control problem than valves)
        #   d_internal_energy is the energy storage dynamic
        #
        # solving for state variables...
        #   1/2*I*angledot*angledot = torque*angle + force*radius*angle
        #   angledot = der(angle)
        #   => sqrt(2/I*(torque*angle + force*radius*angle)) = der(angle)
        #
        # Two state variables -> need two equations -> second order system:
        #   - system_energy = 1/2*I*angledot*angledot
        #   - der(system_energy) = I*angledot*angledotdot + hand_internal_thermal = 0
        #   - der(angledot) = angledotdot
        #   -
        #
        # Internal states:
        #   - der(angle) = angledot
        #
        # Observation: this is kind of like when we used to 'parameterize' theta with t in school.
        #
        radicand = 2/I*(d*x + u*shaft.radius*x)
        if radicand > 0:
            sign = 1
        else:
            sign = -1
        return sign*sqrt(sign*radicand)

    return parameterized_shaft_hand_plant


@dataclass
class Result:
    x: np.array
    cost: np.array
    tracking_error_squared: np.array
    d: np.array
    u: np.array


''' Run sim a bunch of times with diff ucmd to find optimal '''
''' Offline mpc learning could provide 'warm start' or 'good initial guess'
for the online mpc'''


def nn_controller(plant):

    # 1. Compute optimal commands over all expected conditions OFFLINE
    # There are two options here:
    #   a) Run a set of MPC strategies or similar on field data and train nn to that, or
    #   b) Optimize total cost over entire field data and train nn on that
    # I suspect b) will be more accurate, but much more complex to compute.
    # However, using a) gives opportunity for 'online' learning, aka, adjusting
    # the plant/controllaw on the fly by comparing prediction vs measured,
    # and backpropogating accordingly.

    # Generate optimzied operation training data.

    def cost_function(x_desired_all, x_all):
        tracking_cost = x_desired_all - x_all
        minimization_cost = 0  # energy ratio
        constraint_cost = 0  # hw limits, or cycle results

    # 2. Train the neural net to output the optimal commands from step 1.

    # Set up controller layers. Input is desired state, output is ucmd
    inputs = keras.Input(shape=(1,), name="digits")
    x = layers.Dense(4, activation="relu", name="dense_1")(inputs)
    x = layers.Dense(4, activation="relu", name="dense_2")(x)
    outputs = layers.Dense(1, activation="softmax", name="predictions")(x)
    # additional layer for x_plant(x, u) during training, then take it out when
    # using the actual model on the controller (or just learn implicit?)

    model = keras.Model(inputs=inputs, outputs=outputs)

    # 3. Return model for running on the ECM itself.

    def nn_controller_parameterized(x_desired, x):
        """
        Args:
            Current state (may need state estimator, or make state estimator implicit in nn model)
            Current desired state
            Current measured disturbance

        Returns:
            u
            state estimators (can use for health monitor)

        Neurons in the controller are trained to the cost funcion "achieved state - desired state" over a state-time vector of all operating conditions.
        desired state -> NN controller
        NN controller -> ucmd
        ucmd -> plant model (empirical or test data)
        plant model -> state achieved
        The neural net has then implicitly learned to modulate ucmd to bring plant towards desired state within constraints, anticipated disturbances, anticipated tracking, etc.
        A more general model can be achieved by providing tons and tons of noise instead of anticipated operating conditions, but that destroys the benefit of optimizing to the task at hand (particular country regulation, particular constraints/hardware, particular application)

        Care must be taken to distinguish the full system you're training (neural controller + plant) vs the neural model controller input/output itself. They are different!
        """
        u = 0
        return u

    return nn_controller_parameterized


# @dataclass
# class MPC_Controller():
#     plant
#     cost_function
#     optimization_function


# def implicit_mpc_controller(plant, cost, optimization_function, x0=0):

#     def cost_function(x, u):
#         x_next = plant(x, u)
#         return cost(x_next, u)

#     def mpc_controller_parameterized(x_desired):
#         """
#         MPC controller has:
#         - an internal dynamic model of the process
#         - a cost function J over the receding horizon
#         - an optimization algorithm minimizing the cost function J using the control input u
#         """
#         # Horizon length is highly dependent on response speed of plant dynamics to commands.
#         horizon_length = .25
#         horizon_count = 5
#         horizon_step = horizon_length / horizon_split
#         cost = x - x_desired
#         u = [0]*horizon_count
#         for idx, h in enumerate(range(0, horizon_length, horizon_step)):
#             u[idx] = optimize.minimize(
#                 cost_function, x0, args=(), method='SLSQP')
#             x0 = u[idx]
#         return u[0]

#     return mpc_controller_parameterized


def explicit_mpc_controller(plant, cost_function, optimization_function):
    pass


def const_controller(const):
    def const_controller_parameterized(x_desired, x):
        return const
    return const_controller_parameterized


def pid_controller(kp, ki, kd, dt):
    '''
    Simple PID controller

    Future: Network of PID, or adjust kp, ki, kd with learned NN/table
            based on state.
    Two methods:
    1. Match with algorithm to data.
    2. Match manually.
    '''

    def pid_controller_parameterized(x_desired, x, previous_cost=0, i=0):
        cost = x_desired - x

        p = kp*cost
        i = i + ki*cost*dt
        d = kd*(cost - previous_cost)/dt

        u = p + i + d

        previous_cost = cost

        return u

    return pid_controller_parameterized


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


if __name__ == "__main__":

    # plant is x_next = f(x, u)
    plant = shaft_hand_plant(Shaft(1, 2), Hand(1))

    solver = runge_kutta_4th_order

    time = TimeSetting(
        start=0,
        stop=3,
        step=.01,
    )

    times = times(TimeSetting)

    # Never ask for anything outside 'possible' states.
    # Somewhat related to the need for 'real' tracking/training data.
    possible_states = Bound(lower=-20, upper=20)

    # Desired state to control to.
    x_desired = [possible_states.upper*sin(t*3) for t in times]

    # Uncontrolled disturbance. (in other words... external parameter or energy change.)
    # This should represent every disturbance we'll see IRL.
    d = [.3*sin(t) + 1 + .1*cos(t*5) for t in times]

    # Initial state.
    x0 = 2

    # Cost function.
    x_constraint = 20
    x_constraint_weight = 1
    # u is added energy to the system, so keep it minimal (add as generalized real energy/mass minimization later)
    u_constraint_weight = 1
    x_tracking_weight = 1

    def cost(x, x_desired, u):
        """ Cost can include current state x, command param u, or internal state (tbd) """
        # make this a NN with weights as nodes??????
        # in the future... this 'cost' should be a continous function, not
        # the harsh x^2 when over.
        constaint_error = x_constraint - x
        if constaint_error < 0:
            constaint_error = 0
        tracking_error = x_desired - x

        total_cost = \
            x_constraint_weight * constaint_error**2 + \
            u_constraint_weight * u**2 + \
            x_tracking_weight * tracking_error**2
        return total_cost, tracking_error**2

    # Controller
    controller = pid_controller(.1, .1, 0, time.step)
    # controller = const_controller(1)

    # Run the simulations (here is where we try many many controllers out)
    results = []
    result = simulate(plant, solver, times, x0, controller,
                      x_desired, d, possible_states, cost)
    result.d = d
    result.x_desired = x_desired
    results.append(result)

    # Plot
    fig, axs = plt.subplots(4, 1, constrained_layout=True)
    plt.xlabel('time')

    for result in results:
        axs[0].plot(times, result.x, label="RK4")
        axs[0].plot(times, result.x_desired, label="desired state")
        axs[0].legend()
        axs[0].set(ylabel="state")
        axs[1].stackplot(times, [result.tracking_error_squared, result.cost],
                         labels=(f"tracking_error_squared: {sum(result.tracking_error_squared)}", f"total_cost: {sum(result.cost)}"))
        axs[1].legend()
        axs[1].set(ylabel="cost")
        axs[2].plot(times, result.d,
                    label=f"total_d_measured: {0}")
        axs[2].legend()
        axs[2].set(ylabel="d")
        axs[3].plot(times, result.u,
                    label=f"total_u: {0}")
        axs[3].legend()
        axs[3].set(ylabel="u")

    plt.show()
