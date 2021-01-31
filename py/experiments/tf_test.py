import tensorflow as tf
from datetime import datetime
from math import sqrt


class Dense(tf.Module):
    """ Dense neural network layer. """

    def __init__(self, in_features, out_features, name=None):
        super().__init__(name=name)
        self.w = tf.Variable(
            tf.random.normal([in_features, out_features]), name='w')
        self.b = tf.Variable(tf.zeros([out_features]), name='b')

    def __call__(self, x):
        y = tf.matmul(x, self.w) + self.b
        return tf.nn.relu(y)


class Controller(tf.Module):
    """ Dense neural net controller. 
    To be embedded on the ECM after training.
    See https://www.tensorflow.org/lite/microcontrollers
    """

    def __init__(self, name=None):
        super().__init__(name=name)

        self.dense_1 = Dense(1, 3)
        self.dense_2 = Dense(3, 1)

    def __call__(self, x):
        x = self.dense_1(x)
        return self.dense_2(x)


class Plant(tf.Module):
    """
    Plant model is currently empirically defined and trained to match data. 
    Could instead be completely data-based.
    TODO: Design as a sparse matrix (tensors) instead of equations.
    """

    def __init__(self, name=None, mass=1, radius=1):
        super().__init__(name=name)
        self.shaft_mass = tf.Variable(1, trainable=False)
        self.shaft_radius = tf.Variable(2, trainable=False)
        self.hand_friction = tf.Variable(1, trainable=False)
        self.I = tf.Variable(.5*mass*sqrt(radius), trainable=False)

    def __call__(self, x, u, d):
        radicand = 2/I*(d*x + u*self.shaft_radius*x)
        if radicand > 0:
            sign = 1
        else:
            sign = -1

        return sign*tf.sqrt(sign*radicand)
        return self.a_variable * x + self.non_trainable_variable


# Make the NN controller
controller = Controller(name="the_model")

plant = Plant(name="my_plant")

# Call it, with random results
print("Model results:", plant(tf.constant([[2.0, 2.0, 2.0]])))


# class SimpleModule(tf.Module):
#     def __init__(self, name=None):
#         super().__init__(name=name)
#         self.a_variable = tf.Variable(5.0, name="train_me")
#         self.non_trainable_variable = tf.Variable(
#             5.0, trainable=False, name="do_not_train_me")

#     def __call__(self, x):
#         return self.a_variable * x + self.non_trainable_variable


# simple_module = SimpleModule(name="simple")

# result = simple_module(tf.constant(5.0))
# print(result)
