import platform

from serial import Serial


class CwSerial:

    def __init__(self):
        if platform.system() == 'Linux':
            port = '/dev/ttyUSB0'
        else:
            port = 'COM4'

        self.serial_port = Serial(port, 115200)

    def write(self, data):
        self.serial_port.write(data)

    def close(self):
        self.serial_port.close()
