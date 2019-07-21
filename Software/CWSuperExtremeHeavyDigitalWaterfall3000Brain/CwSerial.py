from serial import Serial
import platform


class CwSerial():

    def __init__(self):
        # self.serial_port = None
        if platform.system() == 'Linux':
            self.serial_port = Serial('/dev/ttyUSB0', 115200)
        else:
            self.serial_port = Serial('COM3', 115200)

    def write(self, bytes):
        self.serial_port.write(bytes)

    def close(self):
        self.serial_port.close()
