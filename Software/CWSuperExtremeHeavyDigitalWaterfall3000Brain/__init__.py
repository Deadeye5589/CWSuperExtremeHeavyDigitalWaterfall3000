import math
import time
from Queue import Queue
from threading import Thread

from CwController import CwController
from CwRestController import CwRestController
from Settings import Settings


def send_on_time(controller):
    for valve_index in range(len(controller.valves)):
        controller.valves[valve_index].is_on = False if values[valve_index] == '0' else True
    controller.flush()
    time.sleep(Settings.on_time)


def send_off_time(controller):
    for valve_index in range(len(controller.valves)):
        controller.valves[valve_index].is_on = False
    controller.flush()
    time.sleep(Settings.off_time)


def send_on_time_ascending(controller, line):
    for valve_index in range(len(controller.valves)):
        controller.valves[valve_index].is_on = False if values[valve_index] == '0' else True
    controller.flush()

    on_time = math.sqrt((Settings.height / line * 2 / 9.81))

    print on_time

    time.sleep(on_time)


def wait_for_response(queue):
    while not queue.get():
        continue


if __name__ == '__main__':
    queue = Queue()
    controller = CwController(8, queue)
    restController = CwRestController()

    server_thread = Thread(target=restController.run)
    server_thread.start()

    effect = []
    file = open("effects/" + Settings.effect_name + ".txt", "r")
    for row in file:
        effect.append(row.split(" "))

    for index in range(0, Settings.repeats):
        line_in_effect = 1
        #        on_time = ON_TIME_DIFF * 100
        for values in reversed(effect):
            wait_for_response(queue)
            send_on_time(controller)
            # send_on_time_ascending(controller, line_in_effect)

            wait_for_response(queue)
            send_off_time(controller)

            line_in_effect += 1

        time.sleep(Settings.off_time_pause)

    for valve_index in range(len(controller.valves)):
        controller.valves[valve_index].is_on = False
    controller.flush()
