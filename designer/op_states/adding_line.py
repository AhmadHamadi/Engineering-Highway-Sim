from designer.op_states.state import DesignerState
from ui.button_ident import ButtonIdent
import pygame
import designer.op_states.default_state as ds


class AddingLine(DesignerState):

    def __init__(self, designer):
        DesignerState.__init__(self, designer)
        self.set_button_visibility()
        self.designer.title = "Add line segment to highway"
        self.designer.highway.begin_adding_line_segment()

    def handle_click(self, button_ident: ButtonIdent):
        pass

    def handle_mouse_press(self, button):
        pass

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.designer.highway.complete_adding_line_segment()
            self.designer.designer_state_new = ds.DefaultState(self.designer)

    def draw(self, surface):
        pass
