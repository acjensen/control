
@dataclass
class Shaft:
    radius: float
    mass: float


@dataclass
class Hand:
    friction: float


    
def shaft_hand_plant(shaft: Shaft, hand: Hand):

    I = 1/2*shaft.mass*sqrt(shaft.radius)

    def parameterized_shaft_hand_plant(x, u, d):
        radicand = 2/I*(d*x + u*shaft.radius*x)
        if radicand > 0:
            sign = 1
        else:
            sign = -1
        return sign*sqrt(sign*radicand)

    return parameterized_shaft_hand_plant