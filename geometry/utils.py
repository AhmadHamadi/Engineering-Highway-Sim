import pygame.mouse

from geometry.Point import Point
import math

from road.straight import StraightRoad
from road.curved import CurvedRoad


class Utils:

    @staticmethod
    def does_point_lie_in_circle(point: Point, circle_center: Point, circle_radius):
        sqx = (point.x - circle_center.x) ** 2
        sqy = (point.y - circle_center.y) ** 2

        return math.sqrt(sqx + sqy) < circle_radius

    @staticmethod
    def translate_point_horizontal(point: Point, dx):
        origin_x = point.x + dx
        return Point(origin_x, point.y)

    @staticmethod
    def translate_point_vertical(point: Point, dy):
        origin_y = point.y + dy
        return Point(point.x, origin_y)
    
    @staticmethod 
    def translate_point(point: Point, dx, dy):
        new_x = point.x + dx
        new_y = point.y + dy
        return Point(new_x, new_y)

    @staticmethod
    def translate_line_segment(segment: StraightRoad, dx=0, dy=0):
        new_start = Utils.translate_point(segment.start_p, dx, dy)
        new_end = Utils.translate_point(segment.end_p, dx, dy)

        return StraightRoad(new_start, new_end)

    @staticmethod
    def translate_curved_segment(segment: CurvedRoad, dx=0, dy=0):
        new_start = Utils.translate_point(segment.start_p, dx, dy)
        new_end = Utils.translate_point(segment.end_p, dx, dy)
        new_control = Utils.translate_point(segment.control_point, dx, dy)

        return CurvedRoad(new_start, new_control, new_end)

    @staticmethod
    def create_temp_straight_segment(lane, lane_width, translate=True):
        mouse_pos = Point.t2p(pygame.mouse.get_pos())
        end_point = Utils.translate_point_for_lane(mouse_pos, lane.lane_num, lane_width) if translate else mouse_pos
        lane.temp_segment_line(end_point)

    @staticmethod
    def create_temp_curved_segment(lane, lane_width, end_point: Point, translate=True):
        mouse_pos = Point.t2p(pygame.mouse.get_pos())
        end_point_lane = Utils.translate_point_for_lane(end_point, lane.lane_num, lane_width) if translate else end_point
        control_point_lane = Utils.translate_point_for_lane(mouse_pos, lane.lane_num, lane_width) if translate else mouse_pos
        lane.temp_segment_curve(end_point_lane, control_point_lane)

    @staticmethod
    def translate_point_for_lane(point: Point, lane_num, lane_width):
        lane_origin_y = point.y + (lane_width * lane_num)
        return Point(point.x, lane_origin_y)

    @staticmethod
    def dist_points(p0: Point, p1: Point):
        return math.sqrt((p1.x - p0.x)**2 + (p1.y - p0.y)**2)
