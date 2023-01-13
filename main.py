from world import World
from render import Renderer
from rigidbody import RigidBody
from shape import Shape
from random import randint
import cv2 as cv

FRAMERATE = 60

def init():
    # Add Bodies to the World
    for _ in range(30):
        World.add_body(RigidBody(mass=randint(1,10)/10,
                                 position=(randint(-20,20)/10,randint(-20,20)/10),
                                 restitution=randint(1,100)/100,
                                 shape=Shape.Circle(radius=randint(4,8)/50,
                                                    color=(randint(0,255),randint(0,255),randint(0,255)))))

    # Set scaling and center of the render viewport
    Renderer.setup(World.body_list)
    
    # Add bounding box (using 4 big circle static bodies to make a box)
    World.add_body(RigidBody(position=(0,52),shape=Shape.Circle(radius=50),is_static=True))
    World.add_body(RigidBody(position=(52,0),shape=Shape.Circle(radius=50),is_static=True))
    World.add_body(RigidBody(position=(0,-52),shape=Shape.Circle(radius=50),is_static=True))
    World.add_body(RigidBody(position=(-52,0),shape=Shape.Circle(radius=50),is_static=True))

def main(save_video:bool=False):
    if save_video:
        video = cv.VideoWriter("E:/out.mp4",cv.VideoWriter_fourcc(*'MP4V'),FRAMERATE,Renderer.resolution[::-1])
    
    # Main loop
    while True:
        World.update(1/FRAMERATE,3)
        
        # Remove the comment to follow the bodies throughout the sim.
        # Renderer.setup([body for body in World.body_list if not body.is_static])
        
        Renderer.render_frame(World.body_list)
        
        cv.imshow('Render',Renderer.frame)
        if cv.waitKey(int(1000/FRAMERATE)) == ord('q'):
            break
        
        if save_video:
            video.write(Renderer.frame)

if __name__ == '__main__':
    init()
    main()