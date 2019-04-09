import time

from CwController import CwController

REPEATS = 1000
ON_TIME = 0.003
OFF_TIME = 0.02
EFFECT_NAME = "all"
# EFFECT_NAME = "wave_10_valves"
# EFFECT_NAME = "character_a_10_valves"

if __name__ == '__main__':
    controller = CwController(10)

    effect = []
    file = open("effects/" + EFFECT_NAME + ".txt", "r")
    for row in file:
        effect.append(row.split(" "))

    for index in range(0, REPEATS):
        for values in reversed(effect):
            controller.valves[0].is_on = False if values[0] == '0' else True
            controller.valves[1].is_on = False if values[1] == '0' else True
            controller.valves[2].is_on = False if values[2] == '0' else True
            controller.valves[3].is_on = False if values[3] == '0' else True
            controller.valves[4].is_on = False if values[4] == '0' else True
            controller.valves[5].is_on = False if values[5] == '0' else True
            controller.valves[6].is_on = False if values[6] == '0' else True
            controller.valves[7].is_on = False if values[7] == '0' else True
            controller.valves[8].is_on = False if values[8] == '0' else True
            controller.valves[9].is_on = False if values[9] == '0' else True
            controller.flush()
            time.sleep(ON_TIME)

            controller.valves[0].is_on = False
            controller.valves[1].is_on = False
            controller.valves[2].is_on = False
            controller.valves[3].is_on = False
            controller.valves[4].is_on = False
            controller.valves[5].is_on = False
            controller.valves[6].is_on = False
            controller.valves[7].is_on = False
            controller.valves[8].is_on = False
            controller.valves[9].is_on = False
            controller.flush()
            time.sleep(OFF_TIME)

    controller.valves[0].is_on = False
    controller.valves[1].is_on = False
    controller.valves[2].is_on = False
    controller.valves[3].is_on = False
    controller.valves[4].is_on = False
    controller.valves[5].is_on = False
    controller.valves[6].is_on = False
    controller.valves[7].is_on = False
    controller.valves[8].is_on = False
    controller.valves[9].is_on = False
    controller.flush()