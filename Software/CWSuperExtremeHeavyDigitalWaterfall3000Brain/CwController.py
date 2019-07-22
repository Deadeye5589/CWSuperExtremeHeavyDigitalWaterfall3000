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

    def init_valves(self, valve_count):
        for x in range(valve_count):
            bytes = []
            for y in range(int(math.ceil(valve_count / 8.0))):
                bytes.append(0)

            bytes[int((math.ceil(valve_count / 8.0)) - (x / 8) - 1)] = 1 << x % 8
            self.valves.append(CwValve(bytearray(bytes)))

    def flush(self):
        # send S to start
        self.serial.write('S')

        # send valve count (divided by 8)
        valve_stripes = int(math.ceil(float(self.valve_count)/8))
        high_byte, low_byte = struct.unpack('>BB', struct.pack('>H', valve_stripes))
        self.serial.write(str(unichr(high_byte)))
        self.serial.write(str(unichr(low_byte)))

        bytes_to_send = bytearray([0, 0])
        for valve in self.valves:
            if valve.is_on:
                bytes_to_send[0] |= valve.address[0]
                #bytes_to_send[1] |= valve.address[1]
            else:
                bytes_to_send[0] &= ~valve.address[0]
                #bytes_to_send[1] &= ~valve.address[1]

        self.serial.write(bytes_to_send)
