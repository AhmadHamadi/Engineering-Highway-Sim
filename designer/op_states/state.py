from abc import ABC, abstractmethod
from typing import List

from ui.button_ident import ButtonIdent


class DesignerState(ABC):

    def __init__(self, designer):
        self.designer = designer
        self.show_buttons: List[ButtonIdent] = []

    @abstractmethod
    def handle_click(self, button_ident: ButtonIdent):
        pass

    @abstractmethod
    def handle_mouse_press(self, button):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

    def set_button_visibility(self):
        start_y = 10
        button_drawn = 0
        for button in self.designer.window.buttons:
            if button.ident in self.show_buttons:
                button.is_visible = True
                button.update_coords(button.x, start_y + (button_drawn * 30))
                button_drawn = button_drawn + 1
            else:
                button.is_visible = False

    @abstractmethod
    def draw(self, surface):
        pass
