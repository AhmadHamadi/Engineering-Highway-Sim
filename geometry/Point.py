import math

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_tuple(self):
        return self.x, self.y

    def distance_to(self, point):
        return math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    def toString(self):
        return str(self.x) + "," + str(self.y)

    def add(self, point):
        return Point(self.x + point.x, self.y + point.y)

    def multiply(self, k):
        return Point(self.x * k, self.y * k)

    def subtract(self, point):
        return self.add(point.multiply(-1))

    @staticmethod
    def t2p(tup):
        return Point(tup[0], tup[1])

    @staticmethod
    def string2point(string: str):
        list_int = string.split(',')
        return Point(int(list_int[0]), int(list_int[1]))

    @staticmethod
    def list2point(list_point):
        return Point(int(list_point[0]), int(list_point[1]))