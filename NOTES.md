# Example
- Rotating shaft with external disturbance adding / reducing energy.
- External disturbance is estimated by measuring difference in measured shaft energy vs no-disturbance predicted shaft energy (Kalman?)
- Assume 0 external disturbance for now.
- Control law is a 'hand' pressing on the rotating shaft to achieve desired speed.

# Note
- Desired speed, control law, and external disturbance can all be random. It is left for algorithm to decide how to handle this
- The algorithm may 'learn' the external disturbance.
- Try to 'normalize' effects (everything 0->1)
- If we can simulate all the disturbances we'll see irl, we can design the controller programmatically.
- It looks like functions should always take a type and return a type for
  maximum transparency and flexibility
- NEED TO DEFINE 'COST' IN THE TIME DOMAIN AS LAG, ABS ERROR, ETC? BASICALLY COST IS NOT ONLY FUNC OF X ERROR, BUT ALSO TIME ERROR
- What we're basically doing is trying to come up with some 'control model' that is connected to the 'plant model' that effectively modifies the plant model to achieve the desired plant model state (the control model should be made of the same things that the plant model is made of, I.E. a network of PID components with weights). Weights are adjusted during optimization against a large set of 'desired' plant model state data, or how we WANT the plant to act (aka, tracking data. )
- Kind of like a neural net 'parameterized' with time
- Training data is basically all of the internal, disturbed, and desired states that could be encountered during actual operation. Cost is the vector error (x time error and x tracking value error)
- Can use assumption of no limitation on u, although, irl, we need to put some limit on this (how fast can you actuate a valve? Need to model the valve?)
- Model 'wear' as a function of time, cycle that thing runs usually, instead
  of a constant value

NN training process:
- Compute offline optimal commands using high-fidelity model or real plant over all desired trajectories and with usual cost function (hw lims, cycle results, etc)
- Train NN controller on the optimal commands that the offline optimizer found
- Implmement NN controller on the ECM
- Note: could combine this with machine vision.