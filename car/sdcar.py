import random

from car.car import Car
import simulation.interface.highway_interface as hi


class SDCar(Car):

    def __init__(self, lane_num, car_id):
        Car.__init__(self, 0,  lane_num, car_id)
        self.target_lane = self.choose_autonomous_lane()

    def choose_autonomous_lane(self):
        autonomous_lanes = hi.get_autonomous_lanes()
        lane_selected = random.randint(0, len(autonomous_lanes)-1)
        return autonomous_lanes[lane_selected].lane_num

    def init_controller(self, min_following_distance, accel_smoothing, reaction_time, max_accel, comf_decel, max_speed):
        super().init_controller(20, 4.0, 0.1, 3.0, 1.3, 170)

    def select_next_lane(self):
        if self.lane_num > self.target_lane:
            return self.lane_num - 1
        elif self.target_lane > self.lane_num:
            return self.lane_num + 1

    def initiate_lane_change(self, new_lane_num):
        if self.lane_num == self.target_lane:
            return
        else:
            super().initiate_lane_change(new_lane_num)

    def update(self, delta_time, lead_car=None, lead_distance=0):
        if self.lane_num != self.target_lane and not self.changing_lanes:
            self.initiate_lane_change(self.select_next_lane())

        super().update(delta_time, lead_car, lead_distance)


