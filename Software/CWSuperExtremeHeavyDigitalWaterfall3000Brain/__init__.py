import time
from Queue import Queue

from CwController import CwController
from CwRestController import CwRestController

REPEATS = 1000
ON_TIME = 0.001
OFF_TIME = 0.05
ON_TIME_DIFF = 0.01
OFF_TIME_PAUSE = 1.0
# ON_TIME = 0.020
# OFF_TIME = 1.000
EFFECT_NAME = "three"


# EFFECT_NAME = "wave_10_valves"
# EFFECT_NAME = "character_a_10_valves"

def send_on_time(controller):
    for valve_index in range(len(controller.valves)):
        controller.valves[valve_index].is_on = False if values[valve_index] == '0' else True
    controller.flush()
    time.sleep(ON_TIME)


def send_off_time(controller):
    for valve_index in range(len(controller.valves)):
        controller.valves[valve_index].is_on = False
    controller.flush()
    time.sleep(OFF_TIME)


def send_on_time_ascending(controller, line):
    for valve_index in range(len(controller.valves)):
        controller.valves[valve_index].is_on = False
    controller.flush()

    ontime = ON_TIME * (ON_TIME_DIFF * line)
    print ontime

    time.sleep(ontime)


def wait_for_response(queue):
    while not queue.get():
        continue


if __name__ == '__main__':
    queue = Queue()
    controller = CwController(8, queue)
    # restController = CwRestController()

    effect = []
    file = open("effects/" + EFFECT_NAME + ".txt", "r")
    for row in file:
        effect.append(row.split(" "))

    for index in range(0, REPEATS):
        line_in_effect = 0
        for values in reversed(effect):
            wait_for_response(queue)
            # send_on_time(controller)
            send_on_time_ascending(controller, line_in_effect)

            wait_for_response(queue)
            send_off_time(controller)

            line_in_effect += 1

        time.sleep(OFF_TIME_PAUSE)

    for valve_index in range(len(controller.valves)):
        controller.valves[valve_index].is_on = False
    controller.flush()
