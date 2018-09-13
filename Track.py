import pygame
from shapely.geometry import LinearRing, LineString, Point
 
from Config import *

class Track:

  def __init__(self, screen, track_number, color=(255, 255, 255), width=3):
    self.screen = screen
    self.color = color
    self.width = width
    self.track_number = track_number
    self.initialize_track(track_number)


  def initialize_track(self, track_number):
    if track_number == 0:
      self.pointlist_out = track_out_1
      self.pointlist_in = track_in_1
      self.start_pos = track_start_1
    elif track_number == 1:
      self.pointlist_out = track_out_2
      self.pointlist_in = track_in_2
      self.start_pos = track_start_2
    elif track_number == 2:
      self.pointlist_out = track_out_3
      self.pointlist_in = track_in_3
      self.start_pos = track_start_3
    elif track_number == 3:
      self.pointlist_out = track_out_4
      self.pointlist_in = track_in_4
      self.start_pos = track_start_4
    elif track_number ==4:
      self.pointlist_out = track_out_5
      self.pointlist_in = track_in_5
      self.start_pos = track_start_5
      self.super_reward = super_reward_coords
    else:
      print("WRONG TRACK NUMNER PROVIDED")
      self.pointlist_out = track_out_1
      self.pointlist_in = track_in_1
      self.start_pos = track_start_1

  def draw(self):
    pygame.draw.polygon(self.screen, self.color, self.pointlist_out, self.width)
    pygame.draw.polygon(self.screen, self.color, self.pointlist_in, self.width)

  def check_collision(self, car_point):
    car = LinearRing(car_point)
    outer = LinearRing(self.pointlist_out)
    inner = LinearRing(self.pointlist_in)

    if outer.intersects(car) or inner.intersects(car):
      return True
    else:
      return False

  def measure_intersections(self, center_point, line_points):
    result = []
    outer = LinearRing(self.pointlist_out)
    inner = LinearRing(self.pointlist_in)
    for end_point in line_points:
      line = LineString([center_point, end_point])
      
      distances = []
      if inner.intersects(line):
        distances.append(Point(center_point).distance(inner.intersection(line)))

      if outer.intersects(line):
        distances.append(Point(center_point).distance(outer.intersection(line)))

      if len(distances) == 0:
        result.append(None)
      else:
        result.append(int(min(distances)))

    return result