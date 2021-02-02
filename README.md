# Goal
Train a control law (offline) to minimize an objective function over a series of external disturbances to a dynamical system.

# Terms
- system state 'x'
  - measured
  - unmeasured
  - predicted (over horizon)
- external disturbance 'd'
  - measured
  - unmeasured
  - predicted (over horizon)
- plant function 'dxdt = f(x, u, d)'
- controlled parameter 'u'
 
# Basic idea
Train an MPC or similar controller with various forcast horizons and learn the optimal commands u to minimize measured - predicted disturbance and an arbitrary objective function based on the plant's state.