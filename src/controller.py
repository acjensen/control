''' Run sim a bunch of times with diff ucmd to find optimal '''
''' Offline mpc learning could provide 'warm start' or 'good initial guess'
for the online mpc'''

@dataclass
class Bound:
    lower: float
    upper: float

def nn_controller_2():
    pass


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