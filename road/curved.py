import math

import globalprops
from road.road import Road
from road.type import Type
import pygame
from geometry.Point import Point
from typing import List
from geometry.line import Line

BEZIER_RESOLUTION = 300


class CurvedRoad(Road):

    def __init__(self, begin_point: Point, control_point: Point, end_point: Point):
        Road.__init__(self, begin_point, end_point, Type.curved)
        self.control_point = control_point
        self.segments: List[Line] = []
        self.curvatures: List[float] = []

        self.calculate_curve()
        self.calculate_length()

    def calculate_point(self, t):
        x = (1 - t) * (1 - t) * self.start_p.x + 2 * (1 - t) * t * self.control_point.x + t * t * self.end_p.x
        y = (1 - t) * (1 - t) * self.start_p.y + 2 * (1 - t) * t * self.control_point.y + t * t * self.end_p.y

        return Point(x, y)

    def calculate_curve(self):
        self.segments = []
        prev_point = self.start_p

        for i in range(1, BEZIER_RESOLUTION):
            parameter = (1 / BEZIER_RESOLUTION) * i
            point = self.calculate_point(parameter)
            self.segments.append(Line(prev_point.x, prev_point.y, point.x, point.y))

            if self.start_p and self.end_p and self.control_point:
                curvature_calc = self.calculate_curvature(parameter)
                curvature_calc = 1 if curvature_calc == 0 else curvature_calc
                curvature = (1 / curvature_calc) * globalprops.KM_PER_UNIT
                self.curvatures.append(round(curvature, 3))

            prev_point = point

    def calculate_curvature(self, t):
        d = self.calculate_first_derivative(t)
        dd = self.calculate_second_derivative(t)
        numerator = (d.x * dd.y) - (dd.x * d.y)
        denom = math.pow(d.x**2 + d.y**2, 3/2)

        if denom == 0:
            return -1  # no curvature
        else:
            return abs(numerator/denom)

    def calculate_first_derivative(self, t):
        p1p0 = self.control_point.subtract(self.start_p)
        first_term = p1p0.multiply(2*(1-t))
        p2p1 = self.end_p.subtract(self.control_point)
        second_term = p2p1.multiply(2*t)
        return first_term.add(second_term)

    def calculate_second_derivative(self, t):
        p2p1p0 = self.end_p.subtract(self.control_point.multiply(2)).add(self.start_p)
        return p2p1p0.multiply(2)

    def points(self):
        return [self.start_p, self.control_point, self.end_p]

    def draw(self, surface, color=(0, 255, 0)):

        if globalprops.EDITING_MODE:
            self.calculate_curve()
            pygame.draw.circle(surface, (255, 0, 0), self.control_point.get_tuple(), 10)
            pygame.draw.circle(surface, (255, 0, 0), self.end_p.get_tuple(), 10)

        for line in self.segments:
            # i = self.segments.index(line)
            # if i % 100 == 0:
            #     txt_surface = pygame.font.Font(None, 15).render(str(self.curvatures[i]), True, (0, 0, 0))
            #     surface.blit(txt_surface, (line.x, line.y))

            pygame.draw.line(surface, color, (line.x, line.y), (line.x1, line.y1))

    def calculate_length(self):
        calculated_length = 0
        for line in self.segments:
            calculated_length = calculated_length + line.get_length()

        self.length = calculated_length

    def get_length(self):
        return self.length

    def calculate_parameter_distance(self, distance):
        pass

    def calculate_point_distance(self, distance):
        distance_accum = 0

        for segment in self.segments:
            distance_accum = distance_accum + segment.get_length()
            if distance_accum >= distance:
                remain_distance = distance_accum - distance
                return segment.get_point_for_distance(remain_distance)

    def calculate_tangent(self, pos: Point):
        segment, i = self.find_segment_for_point(pos)
        return segment.get_perpendicular_point(pos)

    def find_segment_for_point(self, pos: Point):
        i = 0
        for segment in self.segments:
            if segment.is_point_on_line(pos):
                return segment, i

            i = i + 1

        return None, -1

    def get_curvature_factor(self, pos):
        segment, index = self.find_segment_for_point(pos)
        return self.curvatures[index] if segment is not None else 1

    def get_dir_vector(self, pos: Point):
        segment, i = self.find_segment_for_point(pos)
        return Line(pos.x, pos.y, segment.x1, segment.y1)

    def calculate_intersection_perp(self, segment: Road, pos: Point):
        closest_dist = 1000000.0
        closest_intx = None
        perp_direction = segment.calculate_tangent(pos)

        for segment in self.segments:
            intx = segment.get_intersection(perp_direction)
            param_intx = segment.get_param_for_point(intx)

            if not 0.0 <= param_intx <= 1.0:
                continue

            dist_intx = intx.distance_to(pos)

            if dist_intx < closest_dist:
                closest_intx = intx
                closest_dist = dist_intx

        return closest_intx

    def get_distance_to_point(self, pos):
        accum_distance = 0

        for segment in self.segments:
            if segment.is_point_on_line(pos):
                accum_distance = accum_distance + Point(segment.x, segment.y).distance_to(pos) * globalprops.KM_PER_UNIT
                break

            accum_distance = accum_distance + segment.get_length()

        return accum_distance

    def export(self):
        return "CURVED," + self.start_p.toString() + "," + self.control_point.toString() + "," + self.end_p.toString()
