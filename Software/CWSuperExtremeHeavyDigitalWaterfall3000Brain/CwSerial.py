from serial import Serial


class CwSerial():

    def __init__(self):
        # self.serial_port = None
        self.serial_port = Serial('/dev/ttyUSB0', 115200)

    def write(self, bytes):
        self.serial_port.write(bytes)

    def close(self):
        self.serial_port.close()
