from abc import ABC, abstractmethod
from road.type import Type
from geometry.Point import Point


class Road(ABC):

    def __init__(self, start_p: Point, end_p: Point, type: Type):
        self.start_p = start_p
        self.end_p = end_p
        self.road_type = type
        self.length = 0

    def points(self):
        return [self.start_p, self.end_p]

    @abstractmethod
    def export(self):
        pass

    @abstractmethod
    def draw(self, surface, color=(0, 255, 0)):
        pass

    @abstractmethod
    def get_length(self):
        pass

    @abstractmethod
    def calculate_parameter_distance(self, distance):
        pass

    @abstractmethod
    def calculate_point(self, t):
        pass

    @abstractmethod
    def calculate_point_distance(self, distance):
        pass

    @abstractmethod
    def calculate_tangent(self, pos: Point):
        pass

    @abstractmethod
    def get_dir_vector(self, pos: Point):
        pass

    @abstractmethod
    def calculate_intersection_perp(self, segment, pos: Point):
        pass

    @abstractmethod
    def get_distance_to_point(self, pos):
        pass

    @abstractmethod
    def get_curvature_factor(self, pos):
        pass

