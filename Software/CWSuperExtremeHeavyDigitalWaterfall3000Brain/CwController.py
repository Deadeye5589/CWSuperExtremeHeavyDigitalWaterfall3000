import binascii
import math
import struct

from CwSerial import CwSerial
from CwValve import CwValve


class CwController():

    def __init__(self, valve_count):
        self.valves = []
        self.init_valves(valve_count)
        self.serial = CwSerial()
        self.valve_count = valve_count
        self.valve_stripes = int(math.ceil(float(self.valve_count)/8))
        self.high_byte_valve_stripe, self.low_byte_valve_stripe = struct.unpack('>BB', struct.pack('>H', self.valve_stripes))

    def init_valves(self, valve_count):
        for x in range(valve_count):
            bytes = []
            for y in range(int(math.ceil(valve_count / 8.0))):
                bytes.append(0)

            bytes[int((math.ceil(valve_count / 8.0)) - (x / 8) - 1)] = 1 << x % 8
            self.valves.append(CwValve(bytearray(bytes)))

    def flush(self):
        self.send_start()
        self.send_valve_count()
        self.send_data()

    def send_data(self):
        bytes_to_send = bytearray(self.valve_stripes)

        for valve in self.valves:
            for valve_stripe in range(self.valve_stripes):
                if valve.is_on:
                    bytes_to_send[valve_stripe] |= valve.address[valve_stripe]
                else:
                    bytes_to_send[valve_stripe] &= ~valve.address[valve_stripe]

        self.serial.write(bytes_to_send)

    def send_start(self):
        self.serial.write('S')

    def send_valve_count(self):
        self.serial.write(str(unichr(self.high_byte_valve_stripe)))
        self.serial.write(str(unichr(self.low_byte_valve_stripe)))
