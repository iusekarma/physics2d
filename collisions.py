import numpy as np
from rigidbody import RigidBody
from shape import Shape
from utils import zero_vector, distance, normalise

def check_circle_collision(body1_radius,body2_radius,body1_position,body2_position):
    normal = zero_vector()
    depth = 0.0
    dist=distance(body1_position,body2_position)
    if (body1_radius + body2_radius) < dist:
        return False
    else:
        normal = normalise((body2_position - body1_position))
        depth = body1_radius + body2_radius - dist
        return normal, depth

def resolve_collision(body1:RigidBody,body2:RigidBody,normal):
    relative_velocity = body2.linear_velocity - body1.linear_velocity
    
    restitution = min(body1.restitution,body2.restitution)
    
    impulse_magnitude = -(1+restitution) * np.dot(relative_velocity,normal) / ((1/body1.mass)+(1/body2.mass))
    
    impulse = impulse_magnitude * normal
    
    body1.linear_velocity -= impulse * (1/body1.mass)
    body2.linear_velocity += impulse * (1/body2.mass)

def check_collision(body1:RigidBody,body2:RigidBody):
    if type(body1.shape) == Shape.Circle and type(body2.shape) == Shape.Circle:
        return check_circle_collision(body1.shape.radius,body2.shape.radius,body1.position,body2.position)
    