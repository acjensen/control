system view

	u_next, x_next, d_next = f(x, u, d)

controller (aritifical system)

	u_next = f(x, u, d)

plant

	x_next = f(x, u, d)

disturbance (environment)

	d_next = f(x, u, d)

desired state

    x_des_next = f(??)

disturbance (live)

    Estimated with x_model - x_live

training
	
	err_next = x_des_next - x_next
	err_next = x_des_next(??) - x_next(x, u, d)
	minimize (x_des - x_next) / (t_des - t_next)
 => minimize dx_err/dt

Goal:
1. Control u indirectly by comparing x with x_next and inverting (f_inv)
2. Seperate the modelling of the system inverse f_inv and what it takes to get
   to the tracking signal.

Methods:
1. Run system through all test data multiple times to figure out optimal u_next function (reinforcement learning)

Design a system with a PID, neural net, feedback thing, idk doesn't matter, then tune the weights against test data with the 'system' function.

u, x, d are state variables (all things required to define the state like derivatives, etc)

Controlling adding of energy to system vs controlling its distribution? Kinematics is the data structure you need to simulate the general situation, what variables with what range of values. Dynamics is the actual algorithm that simulates the motion (flow of energy from one part to another)

An engine is similar in that you're adding energy with fuel to cause some desired machine dynamics. The internal parameters can change the kinematics such that the desired dynamics occur within constaints and with optimal energy transfer to the machine dynamics and not heat and stuff