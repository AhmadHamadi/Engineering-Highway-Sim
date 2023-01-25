from road.straight import StraightRoad
from road.curved import CurvedRoad
from road.type import Type
import pygame
from geometry.Point import Point
from geometry.utils import Utils
from road.lane import Lane


class Ramp(Lane):

    def __init__(self, lane_num, attaching_lane):
        Lane.__init__(self, lane_num)
        self.lane_txt = pygame.font.Font(None, 15).render("Ramp " + str(self.lane_num), True, (0, 0, 0))
        self.attaching_lane = attaching_lane

    def export(self):
        lane_dict = super().export()
        lane_dict["attaching_lane"] = self.attaching_lane

        return lane_dict




