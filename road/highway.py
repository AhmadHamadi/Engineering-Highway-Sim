import json

import pygame.draw

from road.lane import Lane
from road.ramp import Ramp
from geometry.Point import Point
from geometry.utils import Utils

from car.car import Car
from car.sdcar import SDCar


class Highway:

    def __init__(self, num_lanes=1, lane_width=50, origin_point=(50, 870)):
        self.num_lanes = num_lanes
        self.lane_width = lane_width
        self.lanes = []
        self.entry_ramps = []
        self.exit_ramps = []

        self.editing_mode = False
        self.origin_point = None

        self.editing_mode_curve = False
        self.temp_curve_end_point = None
        self.ramp_editing_mode = False

        for i in range(num_lanes):
            self.lanes.append(Lane(i))

        self.set_origin(origin_point)

    def set_origin(self, point):

        for i in range(len(self.lanes)):
            lane = self.lanes[i]
            lane_origin = Utils.translate_point_for_lane(Point.t2p(point), i, self.lane_width)
            lane.set_origin(lane_origin)

        self.origin_point = Point.t2p(point)

    def add_lane(self):
        self.num_lanes = self.num_lanes + 1

        prev_lane = self.lanes[-1]

        new_lane = prev_lane.create_translated_copy(self.lane_width, self.num_lanes - 1)

        self.lanes.append(new_lane)

    def remove_lane(self, lane_num):

        self.lanes = [lane for lane in self.lanes if lane.lane_num != lane_num]
        self.entry_ramps = [ramp for ramp in self.entry_ramps if ramp.attaching_lane != lane_num]

    def draw_origin(self, surface):
        pygame.draw.circle(surface, (0, 0, 0), self.origin_point, 10)

    def draw_temp_lane_ramp_editing_mode(self):
        entry_ramp = self.entry_ramps[-1]

        if self.editing_mode:
            Utils.create_temp_straight_segment(entry_ramp, self.lane_width, translate=False)
        elif self.editing_mode_curve and self.temp_curve_end_point is not None:
            Utils.create_temp_curved_segment(entry_ramp, self.lane_width, Point.t2p(self.temp_curve_end_point),
                                             translate=False)

    def draw_temp_lanes(self):

        for i in range(self.num_lanes):
            if self.editing_mode:
                Utils.create_temp_straight_segment(self.lanes[i], self.lane_width)
            elif self.editing_mode_curve and self.temp_curve_end_point is not None:
                Utils.create_temp_curved_segment(self.lanes[i], self.lane_width, Point.t2p(self.temp_curve_end_point))

    def draw_lanes(self, surface):

        if self.editing_mode_curve and self.temp_curve_end_point is not None:
            pygame.draw.circle(surface, (0, 0, 0), self.temp_curve_end_point, 10)
        elif self.editing_mode:
            pygame.draw.circle(surface, (0, 0, 0), pygame.mouse.get_pos(), 10)

        if self.ramp_editing_mode:
            self.draw_temp_lane_ramp_editing_mode()
        else:
            self.draw_temp_lanes()

        for i in range(self.num_lanes):
            self.lanes[i].draw_lane(surface)

        for i in range(len(self.entry_ramps)):
            self.entry_ramps[i].draw_lane(surface)

    def begin_adding_line_segment(self):
        self.editing_mode = True

    def begin_adding_curve_segment(self):
        self.editing_mode_curve = True

    def select_curve_endpoint(self, point):
        self.temp_curve_end_point = point

    def complete_curved_segment_lane(self, lane, point, translate=True):
        end_point = Utils.translate_point_for_lane(Point.t2p(self.temp_curve_end_point), lane.lane_num,
                                                   self.lane_width) if translate else Point.t2p(
            self.temp_curve_end_point)
        control_point = Utils.translate_point_for_lane(Point.t2p(point), lane.lane_num,
                                                       self.lane_width) if translate else Point.t2p(point)
        lane.complete_temp_segment_curve(end_point, control_point)

    def complete_adding_curve_segment_ramp(self, point):

        self.complete_curved_segment_lane(self.entry_ramps[-1], point, translate=False)

    def complete_adding_curve_segment(self, point):

        if self.ramp_editing_mode:
            self.complete_adding_curve_segment_ramp(point)
        else:
            for lane in self.lanes:
                self.complete_curved_segment_lane(lane, point)

        self.editing_mode_curve = False
        self.temp_curve_end_point = None

    def complete_line_segment_lane(self, lane, point, translate=True):
        lane_point = Utils.translate_point_for_lane(Point.t2p(point), lane.lane_num,
                                                    self.lane_width) if translate else point
        lane.complete_temp_segment_line(lane_point)

    def complete_adding_line_segment_ramp(self, point):

        self.complete_line_segment_lane(self.entry_ramps[-1], Point.t2p(point), translate=False)

    def complete_adding_line_segment(self):

        point = pygame.mouse.get_pos()

        if self.ramp_editing_mode:
            self.complete_adding_line_segment_ramp(point)
        else:
            for lane in self.lanes:
                self.complete_line_segment_lane(lane, point)

        self.editing_mode = False

    def does_highway_have_segments(self):
        for lane in self.lanes:
            if len(lane.segments) != 0:
                return True

        return False

    def get_lane_by_mouse_click(self):

        point = pygame.mouse.get_pos()
        p0 = Point.t2p(point)

        for lane in self.lanes:
            origin_lane = lane.origin_point
            if Utils.does_point_lie_in_circle(p0, origin_lane, 10):
                return lane

    def intersect_mouse_click_lane(self):

        point = pygame.mouse.get_pos()
        p0 = Point.t2p(point)

        for lane in self.lanes:
            p1 = lane.does_point_intersect_control_points(p0)
            if p1 is not None:
                return p1

        for ramp in self.entry_ramps:
            p1 = ramp.does_point_intersect_control_points(p0)
            if p1 is not None:
                return p1

    def on_ramp_editing_mode(self, point, lane):
        self.ramp_editing_mode = True
        entry_ramp = Ramp(len(self.entry_ramps), lane.lane_num)
        entry_ramp.set_origin(Point.t2p(point))
        self.entry_ramps.append(entry_ramp)

    def finish_ramp_editing(self):
        self.ramp_editing_mode = False

    def save_highway(self, file_name="highway_1.json"):
        highway_dict = {"num_lanes": self.num_lanes, "lane_width": self.lane_width,
                        "origin_point": self.origin_point.toString()}

        for lane in self.lanes:
            lane_dict = lane.export()
            highway_dict["lane_" + str(lane.lane_num)] = lane_dict

        highway_dict["num_ramps"] = len(self.entry_ramps)

        for ramp in self.entry_ramps:
            ramp_dict = ramp.export()
            highway_dict["onramp_" + str(ramp.lane_num)] = ramp_dict

        out_dict = {"highway": highway_dict, "_comment": "Self-driving #26!!!!"}

        with open(file_name, 'w') as outfile:
            json.dump(out_dict, outfile, indent=4)

    def load_highway(self, file_name):

        self.lanes = []

        file = open(file_name)

        data = json.load(file)

        highway_dict = data['highway']

        self.num_lanes = highway_dict['num_lanes']
        self.lane_width = highway_dict["lane_width"]
        self.origin_point = Point.string2point(highway_dict["origin_point"])

        for i in range(self.num_lanes):
            new_lane = Lane(i)
            new_lane.load(highway_dict["lane_" + str(i)])
            self.lanes.append(new_lane)

        for i in range(highway_dict["num_ramps"]):
            ramp_dict = highway_dict["onramp_" + str(i)]
            attaching_lane = ramp_dict["attaching_lane"]
            new_ramp = Ramp(i, attaching_lane)
            new_ramp.load(ramp_dict)
            self.entry_ramps.append(new_ramp)

        file.close()

    def add_car_to_lane(self, lane_num, car: Car):
        self.lanes[lane_num].add_car(car)

    def remove_car_from_lane(self, car):
        self.lanes[car.lane_num].cars.remove(car)
