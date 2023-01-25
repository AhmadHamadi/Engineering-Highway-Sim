from enum import Enum


class ButtonIdent(Enum):
    select_origin = 1,
    add_lane = 2,
    add_straight_seg = 3,
    add_curve_seg = 4,
    edit_segs = 5,
    add_entry_ramp = 6,
    remove_lane = 7,
    complete_editing = 8,
    complete_entry_ramp = 9,
    save_highway = 10,
    load_highway = 11

