from serial import Serial
import platform
import threading


class CwSerial():

    def __init__(self):
        # self.serial_port = None
        if platform.system() == 'Linux':
            port = '/dev/ttyUSB0'
        else:
            port = 'COM4'

        self.serial_port = Serial(port, 115200)
#        thread = threading.Thread(target=self.read, args=(self.serial_port,))
#        thread.start()

    def write(self, data):
        self.serial_port.write(data)

    def read(self, ser):
       bytes_read = ser.read()
       while True:
           print(bytes_read)
           bytes_read = ser.read()

    def close(self):
        self.serial_port.close()
