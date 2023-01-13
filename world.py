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
    body_list:list[RigidBody] = []
    gravity = np.array([0,9.81])

    @classmethod
    def update(cls,time,iterations=1) -> None:
        dt = time/iterations
        for i in range(iterations):
            for body in cls.body_list:
                body.step(dt,cls.gravity)

            # Check collisions between bodies
            collisions_list = []
            for i in range(len(cls.body_list)-1):
                for j in range(i+1,len(cls.body_list)):
                    if out:=collisions.check_collision(cls.body_list[i],
                                                       cls.body_list[j]):
                        collisions_list.append((i,j,*out))

            # Resolve those collisions
            for i,j,normal,depth in collisions_list:
                if cls.body_list[i].is_static and cls.body_list[j].is_static:
                    continue
                elif cls.body_list[i].is_static:
                    cls.body_list[j].move(normal*depth)
                elif cls.body_list[j].is_static:
                    cls.body_list[i].move(-normal*depth)
                else:
                    cls.body_list[i].move(-normal*depth/2)
                    cls.body_list[j].move(normal*depth/2)
                collisions.resolve_collision(cls.body_list[i],
                                             cls.body_list[j],
                                             normal)
    @classmethod
    def add_body(cls,body:RigidBody) -> None:
        cls.body_list.append(body)

    @classmethod
    def printpv(cls) -> None:
        for i,body in enumerate(cls.body_list):
            print(f'Body {i} : {body.position=} {body.linear_velocity=}')
