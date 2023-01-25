import designer.op_states.choosing_origin as co
import designer.op_states.adding_line as al
import designer.op_states.adding_curve as ac
import designer.op_states.editing_lanes as el
import designer.op_states.adding_entry as ae
from designer.op_states.state import DesignerState
from ui.button_ident import ButtonIdent
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox


class DefaultState(DesignerState):

    def __init__(self, designer):
        DesignerState.__init__(self, designer)
        self.show_buttons = [ButtonIdent.add_lane, ButtonIdent.select_origin,
                             ButtonIdent.add_straight_seg, ButtonIdent.add_curve_seg]

        if designer.highway.does_highway_have_segments():
            self.show_buttons.append(ButtonIdent.edit_segs)
            self.show_buttons.append(ButtonIdent.add_entry_ramp)
            self.show_buttons.append(ButtonIdent.save_highway)

        self.set_button_visibility()

    def handle_click(self, button_ident: ButtonIdent):
        if button_ident == ButtonIdent.add_lane:
            self.designer.highway.add_lane()
        elif button_ident == ButtonIdent.select_origin:
            self.designer.designer_state_new = co.ChoosingOrigin(self.designer)

        elif button_ident == ButtonIdent.add_straight_seg:
            self.designer.designer_state_new = al.AddingLine(self.designer)
        elif button_ident == ButtonIdent.add_curve_seg:
            self.designer.designer_state_new = ac.AddingCurve(self.designer)
        elif button_ident == ButtonIdent.edit_segs:
            self.designer.designer_state_new = el.EditingLanes(self.designer)
        elif button_ident == ButtonIdent.add_entry_ramp:
            self.designer.designer_state_new = ae.AddingEntryRamp(self.designer)
        elif button_ident == ButtonIdent.save_highway:
            self.export_highway()

    def export_highway(self):

        try:
            files = [('JSON', '*.json')]

            file = asksaveasfile(filetypes=files, defaultextension=files)
            self.designer.highway.save_highway(file.name)
        except:
            messagebox.showerror(title='Road Designer', message='Error saving highway to file!')


    def handle_mouse_press(self, button):
        pass

    def handle_event(self, event):
        pass

    def draw(self, surface):
        pass
