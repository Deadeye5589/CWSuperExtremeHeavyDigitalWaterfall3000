import time

from serial import Serial

if __name__ == '__main__':
    serial_port = Serial('/dev/ttyUSB0', 115200)
    print(serial_port.name)

    for left in range(256):
        for right in range(256):
            serial_port.write(bytearray([left, right]))
            time.sleep(0.0125)

    serial_port.close()
