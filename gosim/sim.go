// Post: "What do Parameterized Design, Controller Design,
//        Plant Design, Model-Matching, and Computation Graphs
//        have in common?"
//
//        Exploring time evolution of dynamical systems, controllers,
//        and leading to computational graphs.
//
// Future:
// - Measured-state-based control policy based on desired objective evaluated over whole cycle optimized with genetic algorithm.
// - Web page for all the structs and plots.
// - Parameterized and modularized components.
//
// Comparison to Matlab:
// - The sub-computer that just does the algebra and derivatives
//   is the same language as the sub-computer-design code; there is no
//   need to 'code-gen' or lose yourself in a GUI to get speedy execution,
//   optimization algorithms for tuning your plant to data or tuning your
//   controller to a desired operating state, or even trying out different
//   plants.

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

type Result struct {
	times  []float64
	states []State
}

// Basically a single "simulation" and any supporting materials. Can be paired with test requirements, other settings.
type Test struct {
	simulation Simulation
	project    Project
	result     Result
}

// Arbitrary group of tests.
type Batch []Test

type Project struct {
	name string
}

// See the utils subpackage for method descriptions.
type State = utils.Vector

// A plant is any type that has defined a derivative.
type Plant interface {
	Derivative(State) State
}

// Deltatime is just a type alias for float64 time intervals.
type DeltaTime = float64

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

type Pendulum struct {
	g float64
	l float64
	m float64
	r float64
}

// Future: parameterize the ODE automatically.
// Future: allow all degrees of energy (temp, pressure, xyz motion, etc) and
//    generate all possible systems by elimination.
func (p Pendulum) Derivative(s State) State {
	// Future: follow computation graph instead of explicitly
	//   rearranging expressions to derivatives.
	s_new := make(State, len(s))
	s_new[0] = s[1]
	s_new[1] = -p.g/p.l*math.Sin(s[0]) + s[1]*1.0*p.m*p.r*p.r*math.Sin(s[0])
	return s_new
}

func Plot(path string, xys plotter.XYs) {
	plt, _ := plot.New()
	scatter, _ := plotter.NewScatter(xys)
	plt.Add(scatter)
	plt.Save(600, 600, path)
}

func StatesToXys(time_vec []float64, data []State, State_idx int) plotter.XYs {
	xys := make([]plotter.XY, len(time_vec))
	for step_n, s := range data {
		xys[step_n] = plotter.XY{X: time_vec[step_n], Y: s[State_idx]}
	}
	return xys
}

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
		plant:      Pendulum{9.81, 1.0, .1, 1.0},
	}

	times, states := sim1.simulate()
	Plot("rk4.png", StatesToXys(times, states, 0))
	Plot("rk4_.png", StatesToXys(times, states, 1))

	sim1.integrator = Euler{}
	times, states = sim1.simulate()
	Plot("euler.png", StatesToXys(times, states, 0))
	Plot("euler_.png", StatesToXys(times, states, 1))

	fmt.Println(proj1)
}
