import os


class Settings():
    available_effects = ["clock"]

    # effect = []





for r, d, files in os.walk("."):
    for name in files:
        if name.endswith('.txt'):
            Settings.available_effects.append(name[:-4])
