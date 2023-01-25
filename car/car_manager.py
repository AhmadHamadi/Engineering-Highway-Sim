from typing import List

from geometry.utils import Utils
import globalprops
import simulation.interface.highway_interface as hi

cars = []


def cars_in_radius(car, radius_km: float):
    circle_origin = car.pos
    radius_sim = radius_km / globalprops.KM_PER_UNIT
    cars_found = []

    for car_other in cars:
        car_pos = car_other.pos
        if Utils.does_point_lie_in_circle(car_pos, circle_origin, radius_sim):
            cars_found.append(car_other)

    return cars_found


def get_distance_between_cars(car, other_car):
    lane = hi.get_lane_by_id(car.lane_num)
    segment_num_car = car.segment_num

    if segment_num_car == other_car.segment_num:
        return other_car.distance_on_segment - car.distance_on_segment
    elif segment_num_car < other_car.segment_num:
        # car is ahead of us
        dist_car = car.distance_on_segment
        distance_remaining_car = lane.segments[car.segment_num].get_length() - dist_car
        distance_between_segments = 0

        for i in range(car.segment_num + 1, other_car.segment_num):
            distance_between_segments = distance_between_segments + lane.segments[i].get_length()

        return distance_remaining_car + distance_between_segments + other_car.distance_on_segment
    else:
        return get_distance_between_cars(other_car, car)  # just switch cars around (car is behind other_car)


def get_lead_car(car):
    lane_num = car.lane_num
    segment_num = car.segment_num

    closest_car = None
    closest_dist = float("inf")

    for other_car in cars:
        if other_car.lane_num == lane_num and other_car.segment_num >= segment_num and other_car != car:
            distance = get_distance_between_cars(car, other_car)

            if closest_dist > distance > 0:
                closest_car = other_car
                closest_dist = distance

    return closest_car, closest_dist
