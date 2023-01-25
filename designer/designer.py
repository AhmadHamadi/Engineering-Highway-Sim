import pygame

from ui.button_ident import ButtonIdent
from ui.button import Button
from ui.window import Window
from ui.window import get_mouse_clicked

from road.highway import Highway
from designer.op_states.default_state import DefaultState


# main designer class which acts as a context for our state objects
class Designer:

    def __init__(self):

        self.window = Window("Road Designer Self-driving #26")

        # initial title
        self.title = "ROAD DESIGNER"

        self.init_window()

        # create our highway
        self.highway = Highway()

        # create default state
        self.designer_state = DefaultState(self)

        # this is used to check if we have to transition to another state set by self.designer_state
        self.designer_state_new = None

    # initialize menu buttons. Locations provided here are somewhat irrelevant since they are refreshed with new states.
    def init_window(self):
        self.window.add_button(Button((10, 10), (70, 20), (255, 0, 0), "Add Lane", pygame.font.Font(None, 15),
                                   ButtonIdent.add_lane))
        self.window.add_button(Button((10, 40), (90, 20), (255, 0, 0), "Remove Lane", pygame.font.Font(None, 15),
                                   ButtonIdent.remove_lane))

        self.window.add_button(Button((10, 70), (120, 20), (255, 0, 0), "Choose Origin Point", pygame.font.Font(None, 15),
                                   ButtonIdent.select_origin))

        self.window.add_button(Button((10, 100), (120, 20), (255, 0, 0), "Add Straight Segment",
                                   pygame.font.Font(None, 15), ButtonIdent.add_straight_seg))

        self.window.add_button(Button((10, 130), (120, 20), (255, 0, 0), "Add Curved Segment",
                                   pygame.font.Font(None, 15), ButtonIdent.add_curve_seg))

        self.window.add_button(Button((10, 160), (120, 20), (255, 0, 0), "Edit segments", pygame.font.Font(None, 15),
                                   ButtonIdent.edit_segs))

        self.window.add_button(Button((10, 190), (120, 20), (255, 0, 0), "Finish Editing", pygame.font.Font(None, 15),
                                   ButtonIdent.complete_editing))

        self.window.add_button(Button((10, 220), (120, 20), (255, 0, 0), "Add On Ramp", pygame.font.Font(None, 15),
                                   ButtonIdent.add_entry_ramp))

        self.window.add_button(Button((10, 250), (120, 20), (255, 0, 0), "Complete On Ramp", pygame.font.Font(None, 15),
                                   ButtonIdent.complete_entry_ramp))

        self.window.add_button(Button((10, 250), (120, 20), (255, 0, 0), "Save Highway", pygame.font.Font(None, 15),
                                   ButtonIdent.save_highway))

        self.window.set_button_click_callback(self.handle_button_click)
        self.window.set_mouse_button_click_callback(self.handle_mouse_click)
        self.window.set_rendering_callback(self.draw)
        self.window.set_event_handling_callback(self.handle_event)

    def draw_highway(self, draw_surface):
        self.highway.draw_lanes(draw_surface)

    def handle_button_click(self, button_ident):
        self.designer_state.handle_click(button_ident)
        self.handle_state_transition()

    def handle_mouse_click(self):
        self.designer_state.handle_mouse_press(0)
        self.handle_state_transition()

    def handle_event(self, event):
        self.designer_state.handle_event(event)
        self.handle_state_transition()

    def handle_state_transition(self):
        if self.designer_state_new is not None:  # update to new state requested by current state
            self.designer_state = self.designer_state_new
            self.designer_state_new = None

    def run(self):
        self.window.run()

    def draw(self, draw_surface):

        self.draw_highway(draw_surface)
        self.designer_state.draw(draw_surface)

