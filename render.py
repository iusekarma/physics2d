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
    scale = 1
    resolution = np.array([720,1280],dtype='int')
    center = resolution//2
    background_color = (0,0,0)
    frame = np.zeros(list(resolution)+[3],dtype='uint8')
    
    @classmethod
    def _set_scale(cls,body_list:list[RigidBody],padding=50) -> None:
        min_x , *_ , max_x = sorted([body.position[0] for body in body_list])
        min_y , *_ , max_y = sorted([body.position[1] for body in body_list])

        cls.scale = min((cls.resolution[1]-(2*padding))/(max_x-min_x),
                        (cls.resolution[0]-(2*padding))/(max_y-min_y))

    
    @classmethod  
    def _set_center(cls,body_list:list[RigidBody]) -> None:
        min_x , *_ , max_x = sorted([body.position[0] for body in body_list])
        min_y , *_ , max_y = sorted([body.position[1] for body in body_list])
        
        center = np.array([(min_y + max_y)/2,
                           (min_x + max_x)/2])
        cls.center = cls.resolution/2 - (cls.scale*center)
    
    @classmethod
    def setup(cls,body_list:list[RigidBody]) -> None:
        cls._set_scale(body_list)
        cls._set_center(body_list)
    
    @classmethod
    def draw_circle_body(cls,position,rad,mass,color=(255,255,255)) -> None:
        try:
            x,y = map(int,(position*cls.scale)+cls.center[::-1])
            r = int(rad*cls.scale)
            cv.circle(img=cls.frame,center=(x,y),radius=r,color=color,thickness=-1)
        except Exception as e:
            print('error',e,position,rad,mass)
    
    @classmethod
    def render_frame(cls,body_list:list[RigidBody]) -> None:
        cls.frame[::] = cls.background_color
        for body in body_list:
            cls.draw_circle_body(body.position,body.shape.radius,body.mass,color=body.shape.color)
            
    @classmethod
    def change_background(cls,color:tuple=(0,0,0)) -> None:
        cls.background_color = color
