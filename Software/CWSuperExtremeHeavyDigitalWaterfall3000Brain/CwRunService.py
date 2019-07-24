import Queue
import math
import os
import time
from datetime import datetime

from CwController import CwController
from CwEffect import CwEffect


class CwRunService:

    def __init__(self, queue, valve_count):
        self.queue = queue
        self.cw_controller = CwController(valve_count)

    def update_effect(self, current_effect, effect):
        if effect.on_time is not None:
            current_effect.on_time = effect.on_time
        if effect.height is not None:
            current_effect.height = effect.height
        if effect.pixel_height is not None:
            current_effect.pixel_height = effect.pixel_height
        if effect.off_time is not None:
            current_effect.off_time = effect.off_time
        if effect.sequence is not None:
            current_effect.sequence = effect.sequence
        if effect.effect_name is not None:
            current_effect.effect_name = effect.effect_name
        if effect.off_time_pause is not None:
            current_effect.off_time_pause = effect.off_time_pause
        return current_effect

    def run(self):
        current_effect = CwEffect()
        while True:
            try:
                effect = self.queue.get(block=False)
            except Queue.Empty:
                effect = None
            if effect is not None:
                current_effect = self.update_effect(current_effect, effect)

            if current_effect is not None:
                if current_effect.effect_name == "text":
                    if current_effect.sequence is None:
                        current_effect.sequence = "Hello world!"
                    self.write_sequence(current_effect)
                    time.sleep(current_effect.off_time_pause)
                if current_effect.effect_name == "clock":
                    current_effect.sequence = datetime.now().strftime('%H:%M')
                    self.write_sequence(current_effect)
                    time.sleep(current_effect.off_time_pause)
                else:
                    self.send_effect(self.load_file(current_effect.effect_name), current_effect)

    def map_character_to_file(self, character):
        if character == '@':
            return "at"
        if character == ':':
            return "colon"
        if character == ';':
            return "semicolon"
        if character == '!':
            return "bang"
        if character == '?':
            return "questionmark"
        if character == ',':
            return "comma"
        if character == ' ':
            return "space"
        return character

    def write_sequence(self, effect):
        for character in list(effect.sequence.upper()):
            print character
            filename = self.map_character_to_file(character)
            self.send_effect(self.load_file(filename), effect)

    def send_effect(self, rows, effect):
        for row in reversed(rows):
            # wait_for_response(queue)
            self.send_on_time(row, effect)

            # wait_for_response(queue)
            self.send_off_time(effect)

        time.sleep(effect.off_time_pause)

    def wait_for_response(self, queue):
        while not queue.get():
            continue

    def send_on_time(self, row, effect):
        for valve_index in range(len(self.cw_controller.valves)):
            self.cw_controller.valves[valve_index].is_on = False if row[valve_index] == '0' else True
        self.cw_controller.flush()
        # time.sleep(effect.on_time)

        timing_valves = 0.01

        on_time = math.sqrt(2 * effect.height / 9.81) - math.sqrt(
            2 * (effect.height - effect.pixel_height) / 9.81) + timing_valves
        print on_time
        time.sleep(on_time)

    def send_off_time(self, effect):
        for valve_index in range(len(self.cw_controller.valves)):
            self.cw_controller.valves[valve_index].is_on = False
        self.cw_controller.flush()
        time.sleep(effect.off_time)

    def turn_off_all_valves(self):
        for valve_index in range(len(self.cw_controller.valves)):
            self.cw_controller.valves[valve_index].is_on = False
        self.cw_controller.flush()

    def load_file(self, effect_name):
        rows = []

        file_name = 'effects/' + effect_name + '.txt'
        if os.path.isfile(file_name):
            effect_file = open(file_name, "r")
            for row in effect_file:
                rows.append(row.split(" "))

        return rows
