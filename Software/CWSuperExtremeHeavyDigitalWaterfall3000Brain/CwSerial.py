from serial import Serial
import platform


class CwSerial():

    def __init__(self):
        # self.serial_port = None
        if platform.system() == 'Linux':
            self.serial_port = Serial('/dev/ttyUSB0', 115200)
        else:
            self.serial_port = Serial('COM4', 115200)

    def write(self, data):
        self.serial_port.write(data)

#        bytes_read = self.serial_port.read()
#        while bytes_read != '\r':
#            print(bytes_read)
#            bytes_read = self.serial_port.read()

    def close(self):
        self.serial_port.close()
