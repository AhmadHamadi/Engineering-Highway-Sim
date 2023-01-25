from designer.op_states.state import DesignerState
import designer.op_states.adding_line as al
import designer.op_states.adding_curve as ac
from ui.button_ident import ButtonIdent
import pygame
from geometry.Point import Point
import designer.op_states.default_state as ds


class AddingEntryRamp(DesignerState):

    def __init__(self, designer):
        DesignerState.__init__(self, designer)
        self.show_buttons = [ButtonIdent.complete_entry_ramp]
        self.set_button_visibility()

        designer.title = "select lane for entry ramp"

        self.selected_lane = None
        self.selected_origin_point = False

        self.sub_state = None

    def handle_click(self, button_ident: ButtonIdent):
        if button_ident == ButtonIdent.add_straight_seg:
            self.sub_state = al.AddingLine(self.designer)
            self.designer.title = "add line segment to ramp"

        elif button_ident == ButtonIdent.add_curve_seg:
            self.sub_state = ac.AddingCurve(self.designer)

        elif button_ident == ButtonIdent.complete_entry_ramp:
            self.designer.highway.finish_ramp_editing()
            self.designer.designer_state_new = ds.DefaultState(self.designer)

    def handle_mouse_press(self, button):
        pass

    def handle_event(self, event):

        if self.sub_state is not None:
            self.sub_state.handle_event(event)
            self.handle_substate_completion()

        if event.type == pygame.MOUSEBUTTONUP:
            if self.selected_lane is None:
                self.selected_lane = self.designer.highway.get_lane_by_mouse_click()
            elif not self.selected_origin_point:
                self.select_origin_point()

    def select_origin_point(self):
        self.designer.highway.on_ramp_editing_mode(pygame.mouse.get_pos(), self.selected_lane)
        self.selected_origin_point = True
        self.show_buttons = [ButtonIdent.add_straight_seg, ButtonIdent.add_curve_seg,
                             ButtonIdent.complete_entry_ramp]
        self.set_button_visibility()

    def handle_substate_completion(self):
        if self.designer.designer_state_new is not None:
            self.designer.designer_state_new = None
            self.set_button_visibility()
            self.sub_state = None
            self.designer.title = "add segments to ramp"

    def draw(self, surface):
        if (self.selected_lane is not None) and (not self.selected_origin_point):
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.circle(surface, (0, 0, 0), mouse_pos, 10)


