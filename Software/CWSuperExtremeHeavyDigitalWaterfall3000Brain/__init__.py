import time

from CwController import CwController

if __name__ == '__main__':
    controller = CwController(32)

    time.sleep(2)
    controller.valves[1].is_on = True
    controller.valves[2].is_on = True
    controller.valves[3].is_on = True
    controller.flush()
    time.sleep(2)
    controller.valves[1].is_on = False
    controller.valves[3].is_on = False
    controller.flush()
    time.sleep(2)
    controller.valves[2].is_on = False
    controller.flush()
