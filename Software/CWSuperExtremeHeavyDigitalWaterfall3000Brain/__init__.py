import atexit
import math
import time
from Queue import Queue
from datetime import datetime
from threading import Thread

from CwController import CwController
from CwRestController import CwRestController
from Settings import Settings


def send_on_time(row):
    for valve_index in range(len(cw_controller.valves)):
        cw_controller.valves[valve_index].is_on = False if row[valve_index] == '0' else True
    cw_controller.flush()
    time.sleep(Settings.on_time)


def send_off_time():
    for valve_index in range(len(cw_controller.valves)):
        cw_controller.valves[valve_index].is_on = False
    cw_controller.flush()
    time.sleep(Settings.off_time)


def send_on_time_ascending(row, line):
    for valve_index in range(len(cw_controller.valves)):
        cw_controller.valves[valve_index].is_on = False if row[valve_index] == '0' else True
    cw_controller.flush()

    on_time = math.sqrt((Settings.height / line * 2 / 9.81))

    print on_time

    time.sleep(on_time)


def wait_for_response(queue):
    while not queue.get():
        continue


def send_effect(effect):
    for row in reversed(effect):
        # wait_for_response(queue)
        send_on_time(row)
        # send_on_time_ascending(controller, line_in_effect)

        # wait_for_response(queue)
        send_off_time()

    time.sleep(Settings.off_time_pause)


def write_sequence(sequence):
    for character in list(sequence):
        effect_name = 'colon' if character == ':' else character
        effect = Settings.load_effect(effect_name)
        send_effect(effect)


def turn_off_all_valves():
    for valve_index in range(len(cw_controller.valves)):
        cw_controller.valves[valve_index].is_on = False
    cw_controller.flush()


if __name__ == '__main__':
    queue = Queue()
    cw_controller = CwController(8, queue)

    atexit.register(turn_off_all_valves)

    rest_controller = CwRestController()

    server_thread = Thread(target=rest_controller.run)
    server_thread.start()

    Settings.load_effect(Settings.effect_name)

    for index in range(0, Settings.repeats):
        if Settings.effect_name == "clock":
            time_to_send = datetime.now().strftime('%H:%M')
            write_sequence(time_to_send)

            time.sleep(Settings.off_time_pause)
        else:
            send_effect(Settings.load_effect(Settings.effect_name))
