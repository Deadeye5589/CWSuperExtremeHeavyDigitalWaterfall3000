import os
import string


class Settings():
    height = 1.0
    repeats = 100000
    on_time = 0.03
    #    on_time = 0.001
    off_time = 0.0
    on_time_diff = 0.01
    off_time_pause = 1.0
    effect_name = "three"
    available_effects = ["clock"]

    # effect = []

    @staticmethod
    def to_json():
        return '{"off_time": ' + str(
            Settings.off_time) + ',' + '"on_time": ' + str(
            Settings.on_time) + ',' + '"effect_name": "' + Settings.effect_name + '"}'

    @staticmethod
    def available_effects_to_json():
        return '["' + string.join(Settings.available_effects, '","') + '"]'

    @staticmethod
    def load_effect(effect_name):
        Settings.effect_name = effect_name
        effect = []

        if effect_name in Settings.available_effects and effect_name != "clock":
            effect_file = open("effects/" + effect_name + ".txt", "r")
            for row in effect_file:
                effect.append(row.split(" "))

        return effect


for r, d, files in os.walk("."):
    for name in files:
        if name.endswith('.txt'):
            Settings.available_effects.append(name[:-4])
