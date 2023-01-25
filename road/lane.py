import math
from enum import Enum

from road.straight import StraightRoad
from road.curved import CurvedRoad
from road.road import Road
from road.type import Type
import pygame
from geometry.Point import Point
from geometry.utils import Utils

from car.car import Car
from car.sdcar import SDCar
from typing import List


class LaneType(Enum):
    AUTONOMOUS_LANE = 0,
    NORMAL_LANE = 1


class Lane:

    def __init__(self, lane_num):
        self.segments: List[Road] = []
        self.lane_num = lane_num
        self.origin_point: Point = None
        self.lane_txt = pygame.font.Font(None, 15).render("Lane " + str(self.lane_num), True, (0, 0, 0))
        self.temp_segment = None
        self.cars = []
        self.speed_limit = 0
        self.lane_type = LaneType.NORMAL_LANE

    def set_origin(self, point: Point):
        self.origin_point = point

    def create_new_straight_road(self, end_point: Point):

        if len(self.segments) == 0:
            return StraightRoad(self.origin_point, end_point)
        else:
            final_point = self.segments[-1].end_p
            return StraightRoad(final_point, end_point)

    def create_new_curved_road(self, end_point: Point, control_point: Point):
        if len(self.segments) == 0:
            return CurvedRoad(self.origin_point, control_point, end_point)
        else:
            final_point = self.segments[-1].end_p
            return CurvedRoad(final_point, control_point, end_point)

    def temp_segment_curve(self, end_point: Point, control_point: Point):
        self.temp_segment = self.create_new_curved_road(end_point, control_point)

    def complete_temp_segment_curve(self, end_point: Point, control_point: Point):
        new_segment = self.create_new_curved_road(end_point, control_point)
        self.segments.append(new_segment)
        self.temp_segment = None

    def temp_segment_line(self, end_point: Point):
        self.temp_segment = self.create_new_straight_road(end_point)

    def complete_temp_segment_line(self, end_point: Point):
        new_segment = self.create_new_straight_road(end_point)
        self.segments.append(new_segment)
        self.temp_segment = None

    def get_last_segment(self):
        if not len(self.segments) == 0:
            return self.segments[-1]

    def create_translated_copy(self, dx, lane_num):
        lane = Lane(lane_num)

        new_segments = []
        for segment in self.segments:
            if segment.road_type == Type.straight:
                new_segment = Utils.translate_line_segment(segment, 0, dx)

            else:
                new_segment = Utils.translate_curved_segment(segment, 0, dx)

            if not len(new_segments) == 0:
                last_segment = new_segments[-1]
                new_segment.start_p = last_segment.end_p

            new_segments.append(new_segment)

        lane.origin_point = Utils.translate_point_vertical(self.origin_point, dx)
        lane.segments = new_segments

        return lane

    def does_point_intersect_control_points(self, p0: Point):

        if len(self.segments) == 0:
            return False

        for segment in self.segments:
            for p1 in segment.points():

                if Utils.does_point_lie_in_circle(p0, p1, 10):
                    return p1

    def draw_lane(self, surface):

        if self.origin_point is not None:
            pygame.draw.circle(surface, (0, 0, 0), self.origin_point.get_tuple(), 10.0)
            surface.blit(self.lane_txt, (self.origin_point.x - 10, self.origin_point.y + 12))

        for segment in self.segments:
            if self.lane_type == LaneType.AUTONOMOUS_LANE:
                segment.draw(surface, (233, 142, 98))
            else:
                segment.draw(surface)

        if self.temp_segment is not None:
            self.temp_segment.draw(surface)

        for car in self.cars:
            car.draw(surface)

    def export(self):
        lane_dict = {"segment_num": len(self.segments), "origin_point": self.origin_point.toString()}
        segments_dict = {}
        for i in range(len(self.segments)):
            segments_dict["segment_" + str(i)] = self.segments[i].export()

        lane_dict["segments"] = segments_dict

        return lane_dict

    def load(self, lane_dict):

        origin_point = Point.string2point(lane_dict["origin_point"])
        self.set_origin(origin_point)

        segments_dict = lane_dict["segments"]

        for i in range(lane_dict["segment_num"]):
            segment_info = segments_dict["segment_" + str(i)].split(",")

            if segment_info[0] == "STRAIGHT":
                self.complete_temp_segment_line(Point.list2point(segment_info[3:5]))
            elif segment_info[0] == "CURVED":
                self.complete_temp_segment_curve(Point.list2point(segment_info[5:7]),
                                                 Point.list2point(segment_info[3:5]))

    def add_car(self, car: Car):
        self.cars.append(car)

    def set_speed_limit(self, speed_limit):
        self.speed_limit = speed_limit

    def set_lane_type(self, lane_type: LaneType):
        self.lane_type = lane_type

    def calculate_length(self):
        calculated_distance = 0
        for segment in self.segments:
            calculated_distance = calculated_distance + segment.get_length()

    def get_pos_segment_distance(self, distance):
        calculated_distance = 0
        index = 0
        for segment in self.segments:
            calculated_distance = calculated_distance + segment.get_length()
            if calculated_distance >= distance:
                remain_distance = calculated_distance - distance

                if index == 0:
                    remain_distance = distance

                return segment.calculate_point_distance(remain_distance), index, remain_distance

            index = index + 1

    def get_position_on_lane(self, segment, current_pos):

        closest_distance = 1000000
        closest_point = None
        closest_segment = None
        closest_index = 10000000

        index = 0

        for lane_segment in self.segments:
            intx_point = lane_segment.calculate_intersection_perp(segment, current_pos)

            if intx_point is None:
                index = index + 1
                continue

            dist = intx_point.distance_to(current_pos)

            if dist < closest_distance:
                closest_point = intx_point
                closest_distance = dist
                closest_segment = lane_segment
                closest_index = index

            index = index + 1

        if closest_segment is None:
            return None, -1, -1

        return closest_point, closest_index, closest_segment.get_distance_to_point(closest_point)

    def get_average_traffic_flow(self):

        if len(self.cars) == 0:
            return 0

        traffic_flow_accum = 0
        for car in self.cars:
            traffic_flow_accum = traffic_flow_accum + car.speed

        return traffic_flow_accum / len(self.cars)
