from math import sqrt
from geometry.Point import Point
import globalprops


class Line:
    def __init__(self, x, y, x1, y1):
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1
        self.dir_vector = Point(x1 - x, y1 - y)
        self.length_units = sqrt((self.x1 - self.x) ** 2 + (self.y1 - self.y) ** 2)
        self.length = self.length_units * globalprops.KM_PER_UNIT

    def get_length(self):
        return self.length

    def get_length_units(self):
        return self.length_units

    def get_perpendicular(self):
        return self.get_perpendicular_point(Point(self.x, self.y))

    def get_param_for_point(self, point):
        dist_to_point = Point(self.x, self.y).distance_to(point)
        param_positive = dist_to_point / self.get_length_units()
        param_neg = -param_positive
        p_pos = self.get_point(param_positive)

        if p_pos.distance_to(point) < 0.004:
            return param_positive
        else:
            return param_neg

    def get_point(self, t):
        return Point(self.x + t * self.dir_vector.x, self.y + t * self.dir_vector.y)

    def get_perpendicular_point(self, point: Point):
        new_dir_vector = Point(self.dir_vector.y, -self.dir_vector.x)
        end_point = Point(point.x + new_dir_vector.x, point.y + new_dir_vector.y)
        perp_line = Line(point.x, point.y, end_point.x, end_point.y)
        return perp_line

    def get_intersection(self, line):

        intx = self.find_intersection(self.x, self.y, self.x1, self.y1,
                                      line.x, line.y, line.x1, line.y1)

        return intx

    @staticmethod
    def find_intersection(x1, y1, x2, y2, x3, y3, x4, y4):

        first_term = x1 * y2 - y1 * x2
        second_term = x3 * y4 - y3 * x4
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        px = (first_term * (x3 - x4) - (x1 - x2) * second_term) / denom
        py = (first_term * (y3 - y4) - (y1 - y2) * second_term) / denom
        return Point(px, py)

    def is_point_on_line(self, point: Point):
        dist_ap = sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)
        dist_pb = sqrt((self.x1 - point.x) ** 2 + (self.y1 - point.y) ** 2)

        dist_ab = self.get_length_units()

        return ((dist_ap + dist_pb) - dist_ab) < 0.0000000005

    def get_point_for_distance(self, distance):
        t = distance / self.get_length()
        return Point(self.x + self.dir_vector.x * t, self.y + self.dir_vector.y * t)
