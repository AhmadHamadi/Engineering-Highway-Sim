import road.lane

highway = None
risky_attempts = 0


def get_num_lanes():
    return highway.num_lanes


def get_lane_by_id(lane_id):
    return highway.lanes[lane_id]


def get_autonomous_lanes():
    lanes = []

    for lane in highway.lanes:
        if lane.lane_type == road.lane.LaneType.AUTONOMOUS_LANE:
            lanes.append(lane)

    return lanes


def get_num_cars_lane(lane_id):
    return len(highway.lanes[lane_id].cars)


def get_lane_length(lane_id):
    return highway.lanes[lane_id].get_length()


def lane_has_ramp(lane_id):
    for ramp in highway.entry_ramps:
        if ramp.attaching_lane == lane_id:
            return True

    return False
