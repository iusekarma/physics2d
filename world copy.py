import numpy as np
import collisions
from typing import Protocol

class Shape(Protocol):
    class Circle(Protocol):
        radius:float|int

class RigidBody(Protocol):
    position:np.ndarray
    shape:Shape
    mass:float|int
    
    def step():
        ...
    def move():
        ...
    def move_to():
        ...

class World:
    def __init__(self) -> None:
        self.body_list:list[RigidBody] = []
        self.gravity = np.array([0,9.81])

    def update(self,time,iterations=1) -> None:
        dt = time/iterations
        for i in range(iterations):
            for body in self.body_list:
                body.step(dt,self.gravity)

            # Check collisions between bodies
            collisions_list = []
            for i in range(len(self.body_list)-1):
                for j in range(i+1,len(self.body_list)):
                    if out:=collisions.check_collision(self.body_list[i],
                                                       self.body_list[j]):
                        collisions_list.append((i,j,*out))

            # Resolve those collisions
            for i,j,normal,depth in collisions_list:
                if self.body_list[i].is_static:
                    self.body_list[j].move(normal*depth)
                elif self.body_list[j].is_static:
                    self.body_list[i].move(-normal*depth)
                else:
                    self.body_list[i].move(-normal*depth/2)
                    self.body_list[j].move(normal*depth/2)
                collisions.resolve_collision(self.body_list[i],
                                             self.body_list[j],
                                             normal,depth)

    def add_body(self,body:RigidBody):
        self.body_list.append(body)

    # def printpv(self):
    #     for i,body in enumerate(self.body_list):
    #         print(f'Body {i} : {body.position=} {body.linear_velocity=}')
