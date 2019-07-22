import time

from CwController import CwController
from CwRestController import CwRestController

REPEATS = 1000
ON_TIME = 0.003
OFF_TIME = 0.02
EFFECT_NAME = "all"
# EFFECT_NAME = "wave_10_valves"
# EFFECT_NAME = "character_a_10_valves"

if __name__ == '__main__':
    controller = CwController(10)
    #restController = CwRestController()

    effect = []
    file = open("effects/" + EFFECT_NAME + ".txt", "r")
    for row in file:
        effect.append(row.split(" "))

    for index in range(0, REPEATS):
    #while True:
        for values in reversed(effect):
            for valve_index in range(len(controller.valves)):
                controller.valves[valve_index].is_on = False if values[valve_index] == '0' else True
            controller.flush()
            time.sleep(ON_TIME)

            for valve_index in range(len(controller.valves)):
                controller.valves[valve_index].is_on = False
            controller.flush()
            time.sleep(OFF_TIME)

    for valve_index in range(len(controller.valves)):
        controller.valves[valve_index].is_on = False
    controller.flush()
