from abc import ABC
from abc import abstractmethod


class DrivingPolicy(ABC):

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, draw_surface):
        pass
