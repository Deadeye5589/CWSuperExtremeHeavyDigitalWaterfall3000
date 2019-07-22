import os


class Settings():
    height = 1.0
    repeats = 100000
    on_time = 0.03
    #    on_time = 0.001
    off_time = 0.0
    on_time_diff = 0.01
    off_time_pause = 1.0
    effect_name = "three"
    available_effects = []


for r, d, files in os.walk("."):
    for name in files:
        if name.endswith('.txt'):
            Settings.available_effects.append(name[:-4])
