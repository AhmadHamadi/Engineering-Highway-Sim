import math

import globalprops
from road.road import Road
from road.type import Type
import pygame
from geometry.Point import Point
from geometry.line import Line


class StraightRoad(Road):

    def __init__(self, p1: Point, p2: Point):

        Road.__init__(self, p1, p2, Type.straight)
        self.dir_vector = None

        if p2 is not None:
            self.dir_vector = (p2.x - p1.x, p2.y - p1.y)
            self.length = math.sqrt((self.end_p.x - self.start_p.x)**2 + (self.end_p.y - self.start_p.y)**2) * globalprops.KM_PER_UNIT

    def draw(self, surface, color=(0, 0, 255)):

        if globalprops.EDITING_MODE:
            # pygame.draw.circle(surface, (255, 0, 0), self.start_p, 10)
            pygame.draw.circle(surface, (255, 0, 0), self.end_p.get_tuple(), 10)

        if (self.start_p is not None) and (self.end_p is not None):
            pygame.draw.line(surface, color, self.start_p.get_tuple(), self.end_p.get_tuple())

    def get_length(self):
        return self.length

    def calculate_parameter_distance(self, distance):
        return distance / self.get_length()

    def calculate_point(self, t):
        return Point(self.start_p.x + self.dir_vector[0] * t, self.start_p.y + self.dir_vector[1] * t)

    def calculate_point_distance(self, distance):
        return self.calculate_point(self.calculate_parameter_distance(distance))

    def calculate_tangent(self, pos: Point):
        line = Line(self.start_p.x, self.start_p.y, self.end_p.x, self.end_p.y)
        return line.get_perpendicular_point(pos)

    def get_dir_vector(self, pos: Point):
        line = Line(pos.x, pos.y, self.end_p.x, self.end_p.y)
        return line

    def calculate_intersection_perp(self, segment: Road, pos: Point):
        perp_direction = segment.calculate_tangent(pos)
        parallel_direction = Line(self.start_p.x, self.start_p.y, self.end_p.x, self.end_p.y)

        intx = perp_direction.get_intersection(parallel_direction)
        param_intx = parallel_direction.get_param_for_point(intx)

        if 0.0 <= param_intx <= 1.0:
            return intx

    def get_curvature_factor(self, pos):
        return 1

    def get_distance_to_point(self, pos):
        return self.start_p.distance_to(pos) * globalprops.KM_PER_UNIT

    def export(self):
        return "STRAIGHT," + self.start_p.toString() + "," + self.end_p.toString()
