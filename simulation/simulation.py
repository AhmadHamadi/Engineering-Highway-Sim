import tkinter.messagebox

import pygame
import simulation.interface.highway_interface as highway_interface
import simulation.policy.test_policy

from ui.button_ident import ButtonIdent
from ui.window import Window
from ui.button import Button

from road.highway import Highway

from tkinter import filedialog as fd
import simulation.policy.driving_policy as dp


class Simulation:

    def __init__(self):

        self.window = Window("Self-Driving #26 Highway Simulator")

        self.title = "HIGHWAY SIMULATOR"

        self.init_window()

        self.highway = None
        self.driving_policy: dp.DrivingPolicy = None

        self.time = 0.0
        self.time_step = 0.0

    def init_window(self):
        self.window.add_button(Button((10, 10), (90, 20), (255, 0, 0), "Load Highway", pygame.font.Font(None, 15),
                                      ButtonIdent.load_highway))
        self.window.set_rendering_callback(self.draw)
        self.window.set_button_click_callback(self.handle_button_press)
        self.window.set_update_callback(self.update)

    def draw_highway(self, draw_surface):
        if self.highway is not None:
            self.highway.draw_lanes(draw_surface)

    def load_highway(self):
        try:
            file_name = fd.askopenfilename()
            self.highway = Highway()
            self.highway.load_highway(file_name)
            highway_interface.highway = self.highway
            self.driving_policy = simulation.policy.test_policy.TestPolicy()
        except Exception as e:
            print(str(e))
            tkinter.messagebox.showerror(title='Road Simulator', message='Error loading highway from file!')
            self.highway = None

    def handle_button_press(self, button_ident):
        if button_ident == ButtonIdent.load_highway:
            self.load_highway()

    def set_time(self, time):
        self.time = time

    def run(self):
        self.window.run()

    def update(self, dt):
        if self.driving_policy:
            self.driving_policy.update(0.1666)

    def draw(self, draw_surface):
        self.draw_highway(draw_surface)

        if self.driving_policy:
            self.driving_policy.draw(draw_surface)
