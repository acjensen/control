// Title: "What do Parameterized Design, Controller Design,
//        Plant Design, Model-Matching, and Computation Graphs
//        have in common?"
//
//        Exploring time evolution of dynamical systems, controllers,
//        and eventually leading to computational graphs.
//
// Future:
// - State-based control policy based on desired objective evaluated over whole cycle optimized with genetic algorithm or other.
// - Web page to manage the simulations and plants.
// - Parameterized and modularized plant components.
//
// Comparison to Matlab:
//
//   I suspect this project will lead to a computational graph, or a kind of virtual sub-computer you can define that chunks thru calcs and integrations (tensorflow?).
//
//   The sub-computer that does the algebra and derivatives
//   can be written in the same language as the design code; there is no
//   need for simulink's GUI, 'code-gen' from simulink, etc. to get speedy execution.
//
//   When everything is in the same language, it is much nicer to define optimization algorithms
//   for tuning your plant to data, or tuning your controller to a desired operating state, or
//   even to programmatically evaluate different plant designs against constraints.
//
// Just ignore this comment:
// Note that all we've really done is created a bunch of memory address with floats in them that we write read/values to.
// It is important to seperate the creation of this "Plant" collection of memory addresses, operations, and derivatives,
// from the execution, so that we can "parameterize" the plant.

package main

import (
	"fmt"
	"gosim/utils"
	"math"

	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	// "gonum.org/v1/gonum/mat"
	//https://github.com/gorgonia/gorgonia
)

// Simulation result.
type Result struct {
	times  []float64 // Time vector used in the simulation.
	states []State   // States recorded throughout the simulation.
}

// A Test is just a single "simulation" and any supporting materials.
// In the future, can be paired with test requirements, other settings.
// Not really used yet.
type Test struct {
	simulation Simulation
	project    Project
	result     Result
}

// Batch is just a collection of tests.
// Not really used yet.
type Batch []Test

// Dumb project struct I came up with to keep track of my simulations.
type Project struct {
	name string
}

// See the utils subpackage for method descriptions.
type State = utils.Vector

// A Plant is defined by its derivative function.
// A Derivative is a function dxdt = Derivative(x(t), etc)
type Plant interface {
	Derivative(State) State
}

// Deltatime is just a type alias for float64 time intervals.
// Ideally it is a very small value that the Integrator will integrate over.
type DeltaTime = float64

// An integrator simply uses the derivative defined in the Plant to
// calculate the next State based on the current State and the timestep DeltaTime.
type Integrator interface {
	Forward(Plant, State, DeltaTime) State
}

type Euler struct{}
type RungeKutta4 struct{}

func (e Euler) Forward(p Plant, s State, dt DeltaTime) State {
	// Explicit forward Euler integration.
	// See https://en.wikipedia.org/wiki/Euler_method.
	return s.AddVec(p.Derivative(s).MultTime(dt))
}

func (rk RungeKutta4) Forward(p Plant, s State, dt DeltaTime) State {
	// Explicit forward 4th order Runge Kutta integration. Recommended for any system greater than 1st order.
	// See https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods.
	k1 := p.Derivative(s)
	k2 := p.Derivative(s.AddVec(k1.MultTime(dt * .5)))
	k3 := p.Derivative(s.AddVec(k2.MultTime(dt * .5)))
	k4 := p.Derivative(s.AddVec(k3.MultTime(dt)))
	temp := k1.AddVec(
		k2.MultTime(2.0).AddVec(
			k3.MultTime(2.0).AddVec(
				k4)))
	s_new := s.AddVec(temp.MultTime(dt / 6.0))
	return s_new
}

// The controlled value to be injected into the plant at each timestep.
type Controlled struct {
	value float64
}

// Returns a controlled value based on the current state of the plant.
func (c *Controlled) Control(s State) float64 {
	c.value = math.Sin(s[0])
	return c.value
}

// g, l, m are constants for a regular old pendulum.
type Pendulum struct {
	g float64    // Gravity [m/s^2]
	l float64    // Length of pendulum [m]
	m float64    // Mass at the end of the pendulum [kg]
	r Controlled // Distance from the pendulum's fulcrum to the mass [m]
}

// Define the derivative of a Pendulum dynamical (plant) system: 'dxdt = f(x(t), u(x), d(t))'.
// The controller that injects the controlled command 'u' is seen below as 'Control(s)'.
//
// Future: parameterize the ODE automatically.
// Future: allow all degrees of energy (temp, pressure, xyz motion, etc) and
//    generate all possible systems by elimination.
// Future: follow computation graph instead of explicitly
//   rearranging expressions to derivatives.
func (p Pendulum) Derivative(s State) State {
	s_new := make(State, len(s))
	s_new[0] = s[1]
	s_new[1] = -p.g/p.l*math.Sin(s[0]) + s[1]*1.0*p.m*p.r.Control(s)*p.r.Control(s)*math.Sin(s[0])
	return s_new
}

// Plot the states over time. 'path' is the output filepath.
func Plot(path string, xys plotter.XYs) {
	plt, _ := plot.New()
	scatter, _ := plotter.NewScatter(xys)
	plt.Add(scatter)
	plt.Save(600, 600, path)
}

// Convert a list of states and times to a plotter-compatible format.
func StatesToXys(time_vec []float64, data []State, State_idx int) plotter.XYs {
	xys := make([]plotter.XY, len(time_vec))
	for step_n, s := range data {
		xys[step_n] = plotter.XY{X: time_vec[step_n], Y: s[State_idx]}
	}
	return xys
}

// Parameters needed to generate a time vector.
type TimeSpec struct {
	num_steps, t_end int
}

// Create a time vector from number of steps and the end time.
func MakeTime(ts TimeSpec) ([]float64, float64) {
	time := make([]float64, ts.num_steps)
	for step_n := 0; step_n < ts.num_steps; step_n++ {
		time[step_n] = float64(step_n) / float64(ts.num_steps)
	}
	dt := float64(ts.t_end) / float64(ts.num_steps)
	return time, dt
}

type Simulation struct {
	integrator Integrator
	state0     State
	ts         TimeSpec
	plant      Plant
	plot_name  string
}

func (sim Simulation) simulate() ([]float64, []State) {

	current_state := sim.state0
	new_state := make(State, len(sim.state0))
	times, dt := MakeTime(sim.ts)
	states := make([]State, sim.ts.num_steps)

	// Step through each time, recording each state as we go in 'states'.
	fmt.Println("Starting the simulation.")
	for step_n, _ := range times {
		states[step_n] = current_state
		new_state = sim.integrator.Forward(sim.plant, current_state, dt)
		current_state = new_state
		step_n += 1
	}
	fmt.Println("Finished the simulation.")

	return times, states
}

func main() {

	proj1 := Project{"My cool project!"}
	sim1 := Simulation{
		integrator: RungeKutta4{},
		state0:     State{0, .0001},
		ts:         TimeSpec{num_steps: 10000, t_end: 10},
		plant:      Pendulum{9.81, 1.0, 1, Controlled{}},
	}

	times, states := sim1.simulate()
	// Plot the velocity and acceleration of the pendulum angle.
	Plot("artifacts/rk4_velocity.png", StatesToXys(times, states, 0))
	Plot("artifacts/rk4_accel.png", StatesToXys(times, states, 1))

	// Run the sim again, this time with the Euler integrator.
	sim1.integrator = Euler{}
	times, states = sim1.simulate()
	// Plot the velocity and acceleration of the pendulum angle.
	Plot("artifacts/euler_velocity.png", StatesToXys(times, states, 0))
	Plot("artifacts/euler_accel.png", StatesToXys(times, states, 1))

	fmt.Println(proj1)
}
