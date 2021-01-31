import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from abc import abstractmethod


air_charge_cooler_effectiveness = 1


def air_charge_cooler(inlet_air_temp, ambient_air_temp, inlet_air_pressure):
    outlet_air_pressure = inlet_air_pressure
    inlet_air_temp - air_charge_cooler_effectiveness * \
        (inlet_air_temp - ambient_air_temp)
    return inlet_air_temp, outlet_air_pressure


def unmixed_inlet_volume(mass_flow_to_inlet_system, mass_flow_from_compressor, mass_flow_from_compressor_temp):
    mass_flow_from_compressor * mass_flow_from_compressor_temp - mass_flow_to_inlet_system
    return air_charge_cooler_out_pressure, air_charge_cooler_in_temp

    # Input constants
m = 1  # mass (kg)
L = 1  # length (m)
b = 0  # damping value (kg/m^2-s)
g = 9.81  # gravity (m/s^2)
delta_t = 0.02  # time step size (seconds)
t_max = 10  # max sim time (seconds)
theta1_0 = np.pi/2  # initial angle (radians)
theta2_0 = 0  # initial angular velocity (rad/s)
theta_init = (theta1_0, theta2_0)
# Get timesteps
t = np.linspace(0, t_max, int(t_max/delta_t))


def int_pendulum_sim(theta_init, t, L=1, m=1, b=0, g=9.81):
    theta_dot_1 = theta_init[1]
    theta_dot_2 = -b/m*theta_init[1] - g/L*np.sin(theta_init[0])
    return theta_dot_1, theta_dot_2


theta_vals_int = integrate.odeint(int_pendulum_sim, theta_init, t)

fig, axs = plt.subplots(2, 1, sharex=True)
axs[0].plot(t, theta_vals_int[:, 0])
axs[1].plot(t, theta_vals_int[:, 1])
plt.show()
