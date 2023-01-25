import globalprops
from designer.op_states.state import DesignerState
from ui.button_ident import ButtonIdent
import pygame
from geometry.Point import Point
import designer.op_states.default_state as ds


class EditingLanes(DesignerState):

    def __init__(self, designer):
        DesignerState.__init__(self, designer)
        self.show_buttons = [ButtonIdent.complete_editing]
        self.set_button_visibility()

        designer.title = "click and drag points to edit segments"

        self.selected_point: Point = None

        globalprops.EDITING_MODE = True

    def handle_click(self, button_ident: ButtonIdent):
        if button_ident == ButtonIdent.complete_editing:
            globalprops.EDITING_MODE = False
            self.designer.designer_state_new = ds.DefaultState(self.designer)

    def handle_mouse_press(self, button):
        pass

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.selected_point = self.designer.highway.intersect_mouse_click_lane()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.selected_point = None
        elif event.type == pygame.MOUSEMOTION:
            self.update_selected_point()

    def update_selected_point(self):
        if self.selected_point is not None:
            mouse_pos = pygame.mouse.get_pos()
            self.selected_point.x = mouse_pos[0]
            self.selected_point.y = mouse_pos[1]

    def draw(self, surface):
        pass
