"""
import cv2 as cv
import numpy as np
# from world import World
# from rigidbody import RigidBody
# from shape import Shape


SCALE = 50
WORLD_CENTER = (640,360)
FRAMERATE = 60

view = np.zeros([720,1280],dtype='uint8')

World.body_list.append(RigidBody(mass=2,position=(0,0),shape=Shape.Circle(radius=0.2),is_static=True))
World.body_list.append(RigidBody(mass=3,position=(4,0),shape=Shape.Circle(radius=0.3)))
World.body_list.append(RigidBody(mass=5,position=(0.1,-10),shape=Shape.Circle(radius=0.5)))
World.body_list.append(RigidBody(mass=4,position=(-7,7),shape=Shape.Circle(radius=0.4)))

def d_c(position,rad,mass):
    try:
        x = int(position[0]*SCALE+WORLD_CENTER[0])
        y = int(position[1]*SCALE+WORLD_CENTER[1])
        r = int(rad*SCALE)
        cv.circle(img=view,center=(x,y),radius=r,color=255,thickness=-1)
    except Exception as e:
        print('error',e,position,rad,mass)

while True:
    World.update(1/FRAMERATE,3)
    view[:] = 0
    view[360,640] = 255
    for body in World.body_list:
        d_c(body.position,body.shape.radius,body.mass)
    cv.imshow('Render',view)
    if cv.waitKey(int(1000/FRAMERATE)) == ord('q'):
        break
"""

from typing import Protocol
import cv2 as cv
import numpy as np

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

class World(Protocol):
    body_list:list[RigidBody]
    
    def update():
        ...

class Renderer:
    def __init__(self,background_color=(0,0,0)) -> None:
        self.scale = 1
        self.resolution = np.array([720,1280],dtype='int')
        self.center = self.resolution//2
        self.background_color = background_color
        self.frame = np.zeros(list(self.resolution)+[3],dtype='uint8')
        
    def _set_scale(self,body_list:list[RigidBody],padding=20) -> None:
        min_x , *_ , max_x = sorted([body.position[0] for body in body_list])
        min_y , *_ , max_y = sorted([body.position[1] for body in body_list])
        
        if (max_x-min_x) >= (max_y-min_y):
            self.scale = (self.resolution[1]-(2*padding))//(max_x-min_x)
        else:
            self.scale = (self.resolution[0]-(2*padding))//(max_y-min_y)
            
    def _set_center(self,body_list:list[RigidBody]) -> None:
        min_x , *_ , max_x = sorted([body.position[0] for body in body_list])
        min_y , *_ , max_y = sorted([body.position[1] for body in body_list])
        
        center = np.array([(min_y + max_y)/2,
                           (min_x + max_x)/2])
        print(center)
        self.center = self.resolution//2 - (self.scale*center)
    
    def setup(self) -> None:
        self._set_scale()
        self._set_center()
    
    def draw_circle_body(self,position,rad,mass,color=(255,255,255)) -> None:
        try:
            x,y = map(int,position*self.scale+self.center[::-1])
            r = int(rad*self.scale)
            cv.circle(img=self.frame,center=(x,y),radius=r,color=color,thickness=-1)
        except Exception as e:
            print('error',e,position,rad,mass)
    
    def render_frame(self,body_list:list[RigidBody]) -> None:
        self.frame[::] = self.background_color
        for body in body_list:
            self.draw_circle_body(body.position,body.shape.radius,body.mass)
        
if __name__ == '__main__':
    from rigidbody import RigidBody
    from shape import Shape
    from world import World
    
    World()
    World.body_list.append(RigidBody(mass=3,position=(4,0),shape=Shape.Circle(radius=0.3)))
    World.body_list.append(RigidBody(mass=2,position=(0,0),shape=Shape.Circle(radius=0.2),is_static=True))
    World.body_list.append(RigidBody(mass=5,position=(0.1,-10),shape=Shape.Circle(radius=0.5)))
    World.body_list.append(RigidBody(mass=4,position=(-7,7),shape=Shape.Circle(radius=0.4)))
    
    World.printpv()
    print('...\n')
    
    r = Renderer()
    print(r.scale,r.resolution,r.center)
    print('...\n')
    
    r._set_scale(World.body_list,40)
    # r.scale =10
    r._set_center(World.body_list)
    print(r.scale,r.resolution,r.center)
    print('...\n')
        
    view = np.zeros(r.resolution,dtype='uint8')
    
    

    FRAMERATE = 60
    
    while True:
        World.update(1/FRAMERATE,3)
        r.render_frame(World.body_list)
        cv.imshow('Render',r.frame)
        if cv.waitKey(int(1000/FRAMERATE)) == ord('q'):
            break