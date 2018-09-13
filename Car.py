from math import *
from pygame.math import Vector2
import pygame

from utils import line_intersection
from Config import *

class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 10
        self.brake_deceleration = 10
        self.free_deceleration = 2

        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(0, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / tan(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

class NonStopCar:
    def __init__(self, start_pos):
        self.position = Vector2(start_pos[0], start_pos[1])
        self.velocity = Vector2(0.0, 0.0)

        self.angle = 0.0
        self.length = 4
        self.max_steering = 45
        self.max_velocity = 6
        self.steering = 0.0
        self.drive = True

        self.front_point = (0,0)
        self.back_point = (0,0)
        self.corners = []
        self.sensors = []

    def update(self, action):
        if action == 1:
            self.steering = -self.max_steering
        elif action == 2:
            self.steering = self.max_steering
        else:
            self.steering = 0

        det = 0.032
        if (self.drive):
            self.velocity.x = self.max_velocity
        else:
            self.velocity.x = 0

        if self.steering:
            turning_radius = self.length / tan(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * det
        self.angle += degrees(angular_velocity) * det

        (c1f, c2f) = self.position * ppu
        (c1, c2) = (int(c1f), int(c2f))

        self.front_point = (xp1,yp1) = (int(c1+car_length/2*cos(radians(-self.angle))), int(c2+car_length/2*sin(radians(-self.angle))))
        self.back_point = (xp2,yp2) = (int(c1-car_length/2*cos(radians(-self.angle))), int(c2-car_length/2*sin(radians(-self.angle))))

        self.corners = []
        self.corners.append((int(xp1-car_width/2*cos(radians(-self.angle+90))), int(yp1-car_width/2*sin(radians(-self.angle+90)))))
        self.corners.append((int(xp1+car_width/2*cos(radians(-self.angle+90))), int(yp1+car_width/2*sin(radians(-self.angle+90)))))
        self.corners.append((int(xp2+(car_width/2-3)*cos(radians(-self.angle+90))), int(yp2+(car_width/2-3)*sin(radians(-self.angle+90)))))
        self.corners.append((int(xp2-(car_width/2-3)*cos(radians(-self.angle+90))), int(yp2-(car_width/2-3)*sin(radians(-self.angle+90)))))

        self.sensors = []
        self.sensors.append((int(c1+sensor_length*cos(radians(-self.angle-60))), int(c2+sensor_length*sin(radians(-self.angle-60)))))
        self.sensors.append((int(c1+sensor_length*cos(radians(-self.angle-30))), int(c2+sensor_length*sin(radians(-self.angle-30)))))
        self.sensors.append((int(c1+sensor_length*cos(radians(-self.angle))), int(c2+sensor_length*sin(radians(-self.angle)))))
        self.sensors.append((int(c1+sensor_length*cos(radians(-self.angle+30))), int(c2+sensor_length*sin(radians(-self.angle+30)))))
        self.sensors.append((int(c1+sensor_length*cos(radians(-self.angle+60))), int(c2+sensor_length*sin(radians(-self.angle+60)))))