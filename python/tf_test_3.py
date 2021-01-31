import tensorflow as tf
import matplotlib.pyplot as plt
from math import sqrt


class Plant(tf.Module):
    """
    Plant model is currently empirically defined and trained to match data. 
    Could instead be completely data-based.
    TODO: Design as a sparse matrix (tensors) instead of equations.
    """

    def __init__(self, name=None, mass=1.0, radius=1.0, friction=1):
        super().__init__(name=name)
        self.shaft_mass = tf.Variable(mass, trainable=False)
        self.shaft_radius = tf.Variable(radius, trainable=False)
        self.hand_friction = tf.Variable(friction, trainable=False)
        self.I = tf.Variable(.5*mass*sqrt(radius), trainable=False)

    def __call__(self, x, u, d):
        radicand = tf.divide(2, tf.multiply(
            self.I, (tf.multiply(d, x) + tf.multiply(u, tf.multiply(self.shaft_radius, x)))))
        if radicand > 0.0:
            sign = 1.0
        else:
            sign = -1.0

        # sqrt is sus...
        return tf.multiply(sign, tf.sqrt(tf.multiply(sign, radicand)))


my_plant = Plant()
r = my_plant(tf.constant(1.0), tf.constant(1.0), tf.constant(1.0))
print(r)

t = tf.linspace(0.0, 6.0, 200+1)
print(t)
r = my_plant(t, t, t)
