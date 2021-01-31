import tensorflow as tf
import matplotlib.pyplot as plt

t = tf.linspace(-10.0, 10.0, 200+1)
b = tf.Variable(0.0)

with tf.GradientTape() as tape:
    y = tf.nn.sigmoid(t+b)

dy_dx = tape.jacobian(y, b)
print(dy_dx.shape)

x = tf.random.normal([7, 5])
print(x)
