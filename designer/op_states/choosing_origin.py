from designer.op_states.state import DesignerState
from ui.button_ident import ButtonIdent
import pygame
import designer.op_states.default_state as ds


class ChoosingOrigin (DesignerState):

    def __init__(self, designer):
        DesignerState.__init__(self, designer)
        designer.title = "choose origin point for highway"
        self.set_button_visibility()

    def handle_click(self, button_ident: ButtonIdent):
        pass

    def handle_mouse_press(self, button):
        pass

    def handle_event(self, event):
        print(event)
        if event.type == pygame.MOUSEBUTTONUP:
            self.designer.highway.set_origin(pygame.mouse.get_pos())
            self.designer.designer_state_new = ds.DefaultState(self.designer)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(surface, (0, 0, 0), mouse_pos, 10)



