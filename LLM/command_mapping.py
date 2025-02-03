COMMAND_MAPPING = {
    "takeoff": lambda drone, param: drone.takeoff(),
    "land": lambda drone, param: drone.land(),
    "move_up": lambda drone, param: drone.move_up(param),
    "move_down": lambda drone, param: drone.move_down(param),
    "move_left": lambda drone, param: drone.move_left(param),
    "move_right": lambda drone, param: drone.move_right(param),
    "move_forward": lambda drone, param: drone.move_forward(param),
    "move_back": lambda drone, param: drone.move_back(param),
    "rotate_clockwise": lambda drone, param: drone.rotate_clockwise(param),
    "rotate_counter_clockwise": lambda drone, param: drone.rotate_counter_clockwise(param),
    "flip_left": lambda drone, param: drone.flip_left(),
    "flip_right": lambda drone, param: drone.flip_right(),
    "flip_forward": lambda drone, param: drone.flip_forward(),
    "flip_back": lambda drone, param: drone.flip_back(),
    # In case you want to support complex moves such as RC control:
    "send_rc_control": lambda drone, params: drone.send_rc_control(*params),
}