import tensorflow as tf
from sympy import *


# my custom class with description attribute
class MySymbol(Symbol):
    def __new__(self, name, description=''):
        obj = Symbol.__new__(self, name)
        obj.description = description
        return obj


T_t, P_t, A_r, C, c_p, D, I_en, I_tc, M, mdot_as, m_ae, mdot_c, mdot_c_corr, me, m_dot_ex_a, mdot_egr, m_f, m_i, mdot_t, mdot_th, m_x_i, P_a, P_e, P_i, P_p, p_r_egr, p_r_t, p_r_th, PW_c, PW_t, T_a, T_c, T_cool, T_e, T_egr, T_ex, T_i, T_ic, T_p, U, V, V_e, V_i, X_e, x_egr, X_i, x_th, x_vgt = symbols(
    "T_t, P_t, A_r, C, c_p, D, I_en, I_tc, M, mdot_as, m_ae, mdot_c, mdot_c_corr, me, m_dot_ex_a, mdot_egr, m_f, m_i, mdot_t, mdot_th, m_x_i, P_a, P_e, P_i, P_p, p_r_egr, p_r_t, p_r_th, PW_c, PW_t, T_a, T_c, T_cool, T_e, T_egr, T_ex, T_i, T_ic, T_p, U, V, V_e, V_i, X_e, x_egr, X_i, x_th, x_vgt")
eff_c, eff_ic_c, eff_ic_egr, eff_t, w_eng, w_tc_corr, isentropic_work_coefficient, gamma, throttle_valve_angle, flow_coefficient, tau_b, tau_l = symbols(
    "eff_c, eff_ic_c, eff_ic_egr, eff_t, w_eng, w_tc_corr, isentropic_work_coefficient, gamma, throttle_valve_angle, flow_coefficient, tau_b, tau_l")

# Power to increase ideal gas pressure on the compressor side.
compressor_power_eq = Eq(PW_c, mdot_c*c_p*T_a/eff_c *
                         (pow(P_p/P_a, (gamma-1 / gamma))-1))

# Power to increase ideal gas pressure on the turbine side.
turbine_power_eq = Eq(PW_t, mdot_t*c_p*T_e*eff_t *
                      (1-pow(P_t/P_e, (gamma-1)/gamma)))

#
compressor_temp_eq = Eq(T_c/T_a, 1 + 1/eff_c *
                        (pow(P_p/P_a, (gamma-1)/gamma) - 1))

#
turbine_temp_eq = Eq(T_t/T_e, 1 - eff_t *
                     (1 - pow(P_t/P_e, (gamma-1)/gamma)))
#


# use nn to predict exh temp and inducted air instead of exh pressure because thermal reactions
# EGR is input to NN

eqs = [compressor_power_eq, turbine_power_eq,
       compressor_temp_eq, turbine_temp_eq]

for eq in eqs:
    print(eq)
