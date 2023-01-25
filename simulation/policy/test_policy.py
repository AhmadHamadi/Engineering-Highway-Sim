import pygame.font

import road.lane
from simulation.policy.driving_policy import DrivingPolicy
import simulation.interface.highway_interface as hi
from car.car import Car
from car.sdcar import SDCar
import car.car_manager as cm
import random

car_id_generated = 0

LOW_CONGESTION_FOLLOW = (60, 90)
HIGH_CONGESTION_FOLLOW = (100, 130)

FAST_GENERATION = (10.0, 15.0)
SPARSE_GENERATION = (15.0, 30.0)

RISK_FACTOR_DRIVER = (0.0, 0.01)


class CarSpawner:
    def __init__(self, lane_num: int, autonomous_lane=False):
        self.lane_num = lane_num
        self.timer = 0
        self.autonomous_lane = autonomous_lane
        self.next_car = self.get_next_car_time()

    def get_next_car_time(self):
        selected_tuple = FAST_GENERATION if not self.autonomous_lane else SPARSE_GENERATION
        return random.uniform(selected_tuple[0], selected_tuple[1])

    def generate_car(self, dt):
        global car_id_generated
        self.timer = self.timer + dt
        if self.timer > self.next_car:
            num_cars = hi.get_num_cars_lane(self.lane_num)

            if num_cars > 100:
                self.reset_timers()
                return

            new_car = None

            if self.autonomous_lane:
                new_car = SDCar(self.lane_num, car_id_generated)
            else:
                decision = random.choices([0, 1], [0.95, 0.05])

                if decision[0] == 0:
                    risk_factor = self.generate_number(RISK_FACTOR_DRIVER[0], RISK_FACTOR_DRIVER[1])
                    new_car = Car(risk_factor, self.lane_num, car_id_generated)
                elif decision[0] == 1:
                    new_car = SDCar(self.lane_num, car_id_generated)

            selected_tuple = HIGH_CONGESTION_FOLLOW

            reaction_time = self.generate_number(0.75, 2.0)
            min_follow = self.generate_number(selected_tuple[0], selected_tuple[1])
            max_accel = self.generate_number(2.07, 5.5)
            comf_decel = self.generate_number(0.2, 0.3)
            max_speed = self.generate_number(130, 190)

            new_car.init_controller(min_follow, 1.5, reaction_time, max_accel, comf_decel, max_speed)

            hi.highway.add_car_to_lane(self.lane_num, new_car)
            cm.cars.append(new_car)
            car_id_generated = car_id_generated + 1

            self.reset_timers()

    def reset_timers(self):
        self.next_car = self.get_next_car_time()
        self.timer = 0

    def generate_number(self, low, high):
        return random.uniform(low, high)


class TestPolicy(DrivingPolicy):

    def __init__(self):
        self.timer = 0
        self.timer_second = 0
        self.generate_second = True
        self.first_lane = 0
        self.generators = [CarSpawner(0, True), CarSpawner(1, True), CarSpawner(2)]
        self.select_autonomous_lane(0)
        self.select_autonomous_lane(1)

        if hi.get_num_lanes() > 3:
            self.generators.append(CarSpawner(3))

        self.init_lane_properties()
        self.total_timer = 0
        self.font = pygame.font.Font(None, 30)

    def select_autonomous_lane(self, lane_num):
        hi.highway.lanes[lane_num].lane_type = road.lane.LaneType.AUTONOMOUS_LANE

    def init_lane_properties(self):
        hi.highway.lanes[0].speed_limit = 180
        hi.highway.lanes[1].speed_limit = 170
        hi.highway.lanes[2].speed_limit = 130

        if hi.get_num_lanes() == 4:
            hi.highway.lanes[3].speed_limit = 120


    def remove_completed_cars(self):
        cars_to_remove = [car for car in cm.cars if car.reached_end]
        cm.cars = [car for car in cm.cars if car not in cars_to_remove]

        for car in cars_to_remove:
            hi.highway.remove_car_from_lane(car)

    def choose_new_lane(self, lane_num):
        if lane_num == 0:
            return 1
        elif lane_num == 1:
            return 2
        elif lane_num == 2:
            rand_decision = random.uniform(0, 1)
            return 3 if rand_decision > 0.5 and hi.get_num_lanes() > 3 else 1
        elif lane_num == 3:
            return 2

    def random_lane_change(self):
        num_cars = len(cm.cars) - 1

        if num_cars == -1:
            return

        chosen_car_i = random.randint(0, num_cars)
        chosen_car = cm.cars[chosen_car_i]
        chosen_car.initiate_lane_change(self.choose_new_lane(chosen_car.lane_num))

    def update(self, dt):
        self.timer = self.timer + dt
        self.total_timer = self.total_timer + dt

        for gen in self.generators:
            gen.generate_car(dt)

        self.remove_completed_cars()

        for car in cm.cars:
            lead_car, dist = cm.get_lead_car(car)
            car.update(dt, lead_car, dist)

        if self.timer > 15.0:
            self.random_lane_change()
            self.timer = 0.0

    def calc_traffic_flow(self):
        traffic_flow_accum = 0
        highway = hi.highway

        for lane in highway.lanes:
            traffic_flow_accum = traffic_flow_accum + lane.get_average_traffic_flow()

        return traffic_flow_accum / len(highway.lanes)

    def draw(self, draw_surface):
        t_flow = "Traffic Flow: " + str(round(self.calc_traffic_flow())) + " km/h"
        txt_flow = self.font.render(t_flow, True, (0, 0, 0))

        t_time = "Time: "+str(round(self.total_timer))
        txt_time = self.font.render(t_time, True, (0, 0, 0))

        t_incidents = "Risky Maneuvers: "+str(hi.risky_attempts)
        txt_incidents = self.font.render(t_incidents, True, (0, 0, 0))

        draw_surface.blit(txt_flow, (200, 70))
        draw_surface.blit(txt_time, (200, 100))
        draw_surface.blit(txt_incidents, (200, 130))
