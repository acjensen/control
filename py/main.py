
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
