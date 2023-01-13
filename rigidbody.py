import numpy as np
from shape import Shape
from utils import zero_vector

class RigidBody:
    def __init__(self,mass=0.0,position=None,restitution=1,shape:Shape=None,is_static=False) -> None:

        if is_static:
            self.mass = float('inf')
        else:
            self.mass = float(mass)

        self.restitution = restitution
        self.position = zero_vector() if not position else np.array(position,dtype='float')
        self.linear_velocity = zero_vector()
        self.acceleration = zero_vector()
        # self.rotation = 0.0
        # self.rotationalVelocity = 0.0
        self.shape = shape
        self.is_static = is_static
        self.force = zero_vector()

    def step(self,dt,gravity) -> None:
        if self.is_static:
            return
        
        self.linear_velocity += (self.acceleration + gravity) * dt
        self.position += self.linear_velocity * dt

        # add rotational motion eq

        self.acceleration = zero_vector()
        self.force = zero_vector()

    def move(self,amount) -> None:
        self.position += amount

    def move_to(self,position) -> None:
        self.position = position

    def add_force(self,force) -> None:
        self.force += force