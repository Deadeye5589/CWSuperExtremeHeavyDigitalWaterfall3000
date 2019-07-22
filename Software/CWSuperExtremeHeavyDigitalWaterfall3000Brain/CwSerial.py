import platform
import threading

from serial import Serial


def read(serial_port, queue):
    while True:
        bytes_read = serial_port.read()
        if bytes_read == 'F':
            queue.put(True)


class CwSerial:

    def __init__(self, queue):
        if platform.system() == 'Linux':
            port = '/dev/ttyUSB0'
        else:
            port = 'COM4'

        self.serial_port = Serial(port, 115200)
        queue.put(True)
        thread = threading.Thread(target=read, args=(self.serial_port, queue,))
        thread.start()

    def write(self, data):
        self.serial_port.write(data)

    def close(self):
        self.serial_port.close()
