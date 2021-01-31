import tensorflow as tf
import tensorflow_probability as tfp
import matplotlib.pyplot as plt

t_init, t0, t1 = 0., 0.5, 1.
y_init = tf.constant([1., 1.], dtype=tf.float64)
A = tf.constant([[-1., -2.], [-3., -4.]], dtype=tf.float64)


def ode_fn(t, y):
    return tf.linalg.matvec(A, y)


results = tfp.math.ode.BDF().solve(ode_fn, t_init, y_init,
                                   solution_times=[t0, t1])
y0 = results.states[0]  # == dot(matrix_exp(A * t0), y_init)
y1 = results.states[1]  # == dot(matrix_exp(A * t1), y_init)

print(y0)
print(y1)
