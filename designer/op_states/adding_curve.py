from designer.op_states.state import DesignerState
from ui.button_ident import ButtonIdent
import pygame
import designer.op_states.default_state as ds


class AddingCurve(DesignerState):

    def __init__(self, designer):
        DesignerState.__init__(self, designer)

        self.designer.title = "choose end point for curve"
        self.end_point_selected = False
        designer.highway.begin_adding_curve_segment()

        self.set_button_visibility()

    def handle_click(self, button_ident: ButtonIdent):
        pass

    def handle_mouse_press(self, button):
        pass

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONUP:
            if not self.end_point_selected:
                self.select_end_point_curve()
            else:
                self.complete_curve()

    def select_end_point_curve(self):
        self.designer.highway.select_curve_endpoint(pygame.mouse.get_pos())
        self.end_point_selected = True
        self.designer.title = "choose control point for curve"

    def complete_curve(self):
        self.designer.highway.complete_adding_curve_segment(pygame.mouse.get_pos())
        self.designer.designer_state_new = ds.DefaultState(self.designer)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(surface, (0, 0, 0), mouse_pos, 10)


