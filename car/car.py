import random

import globalprops
import simulation.interface.highway_interface as highway_interface
from geometry.Point import Point
from road.road import Road
import pygame
from road.type import Type
from car.car_controller import VehicleController
import car.car_manager as cm


class Car:

    font_txt = None

    def __init__(self, risk_factor, lane_num, car_id=0):

        # distance, position and orientation data

        self.lane_num = lane_num
        self.speed = 100
        self.pos: Point = self.get_starting_pos()
        self.segment_num = 0
        self.current_segment: Road = self.get_segment()
        self.distance_on_segment = 0
        self.reached_end = False
        self.distance_total = 0
        self.debug_changed_lane = False

        # identification and control data
        self.car_id = car_id
        self.str_car_id = str(car_id)
        self.lead_car = None
        self.slowing_curve = False
        self.controller: VehicleController = None

        # lane change data
        self.changing_lanes = False
        self.blindspot_circle_radius = 0
        self.lane_change_timeout = 0
        self.new_lane_num = 0

        # heuristic data
        self.risk_factor = risk_factor

        # optimization
        self.prev_str = None
        self.prev_str_surface = None

        if Car.font_txt is None:
            Car.font_txt = pygame.font.Font(None, 15)

    def init_controller(self, min_following_distance, accel_smoothing, reaction_time, max_accel, comf_decel, max_speed):
        max_speed = max_speed / 3.6
        self.controller = VehicleController(min_following_distance, accel_smoothing, reaction_time, max_accel,
                                            comf_decel, max_speed, self.speed / 3.6)

    def get_starting_pos(self):
        lane = self.get_lane()
        return lane.origin_point

    def get_segment(self):
        lane = self.get_lane()
        return lane.segments[self.segment_num]

    def initiate_lane_change(self, new_lane_num):
        self.changing_lanes = True
        self.new_lane_num = new_lane_num
        self.lane_change_timeout = 0

    def perform_lane_change(self, dt):

        self.lane_change_timeout = self.lane_change_timeout + dt

        if self.lane_change_timeout > 30.0:
            self.changing_lanes = False
            return

        new_lane_num = self.new_lane_num
        new_lane = highway_interface.get_lane_by_id(new_lane_num)
        prev_lane = self.get_lane()
        new_segment_pos = new_lane.get_position_on_lane(self.get_segment(), self.pos)

        if new_segment_pos[0] is None:
            return  # abort lane change, not possible

        # perform blind-spot check

        ignore_check = random.choices([0, 1], [1-self.risk_factor, self.risk_factor])

        if ignore_check[0] == 0:
            self.blindspot_circle_radius = new_segment_pos[0].distance_to(self.pos) * globalprops.KM_PER_UNIT
            self.blindspot_circle_radius = self.blindspot_circle_radius + 0.035

            cars_in_search_radius = cm.cars_in_radius(self, self.blindspot_circle_radius)

            for car in cars_in_search_radius:
                if car.lane_num == new_lane_num:
                    return
        else:
            print("CHECK IGNORED", self.car_id)
            highway_interface.risky_attempts = highway_interface.risky_attempts + 1

        self.pos = new_segment_pos[0]
        self.lane_num = new_lane_num
        self.segment_num = new_segment_pos[1]
        self.distance_on_segment = new_segment_pos[2]
        self.current_segment = self.get_segment()
        self.debug_changed_lane = True
        prev_lane.cars.remove(self)
        new_lane.cars.append(self)

        self.changing_lanes = False
        self.lane_change_timeout = 0

    def adjust_following_distance(self):
        pass

    def adjust_reaction_time(self):
        pass

    def adjust_risk_factor(self):
        pass

    def get_next_segment(self):
        self.segment_num = self.segment_num + 1
        self.current_segment = self.get_segment()

    def get_lane(self):
        return highway_interface.get_lane_by_id(self.lane_num)

    def calculate_curve_slowdown(self):
        if self.current_segment.road_type == Type.curved:
            speed_adjustment = (1 - self.current_segment.get_curvature_factor(self.pos)) * 15
            if speed_adjustment < 0:
                speed_adjustment = 0
            self.slowing_curve = False if speed_adjustment < 2 else True
            return speed_adjustment
        else:
            self.slowing_curve = False
            return 0

    def update(self, delta_time, lead_car=None, lead_distance=0):

        self.lead_car = lead_car

        if self.debug_changed_lane:
            # print("Break")
            self.debug_changed_lane = False

        speed_adj = self.calculate_curve_slowdown()
        self.controller.max_speed = (self.get_lane().speed_limit - speed_adj) / 3.6
        self.controller.update_motion(delta_time, lead_car, lead_distance)
        accel = self.controller.current_accel
        self.speed = self.controller.get_speed()

        time_second = delta_time
        speed_ms = self.speed / 3.6

        distance_travelled = (time_second * speed_ms) + (0.5 * accel * delta_time * delta_time)
        distance_travelled = 0 if distance_travelled < 0 else distance_travelled
        distance_travelled_km = distance_travelled / 1000.0
        self.distance_on_segment = self.distance_on_segment + distance_travelled_km
        self.distance_total = self.distance_total + distance_travelled_km

        if self.distance_on_segment > self.current_segment.get_length():
            remaining_distance = self.distance_on_segment - self.current_segment.get_length()

            if self.segment_num == (len(self.get_lane().segments) - 1):
                self.reached_end = True
                return

            self.get_next_segment()
            self.distance_on_segment = remaining_distance
            self.pos = self.current_segment.calculate_point_distance(self.distance_on_segment)
        else:
            self.pos = self.current_segment.calculate_point_distance(self.distance_on_segment)

        if self.changing_lanes:
            self.perform_lane_change(delta_time)

    def draw(self, draw_surface):
        draw_color = (206, 0, 252)

        if self.slowing_curve:
            draw_color = (255, 0, 0)

        pygame.draw.circle(draw_surface, draw_color, self.pos.get_tuple(), 10)

        txt = self.str_car_id + "/" + str(self.lead_car.car_id) if self.lead_car is not None else self.str_car_id
        txt = txt + "/" + str(round(self.speed))

        if not txt == self.prev_str:
            self.prev_str_surface = Car.font_txt.render(txt, True, (0, 0, 0))

        draw_surface.blit(self.prev_str_surface, (self.pos.x, self.pos.y))

        if self.changing_lanes:
            pygame.draw.circle(draw_surface, (255, 15, 20), self.pos.get_tuple(),
                               self.blindspot_circle_radius / globalprops.KM_PER_UNIT, 2)
