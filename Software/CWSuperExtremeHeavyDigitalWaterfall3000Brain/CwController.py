from CwValve import CwValve


class CwController():

    def __init__(self, valve_count):
        self.valves = []
        self.init_valves(valve_count)
        # self.serial = CwSerial()

    def init_valves(self, valve_count):
        for x in range(valve_count):
            bytes = []
            for y in range(int(valve_count / 8)):
                bytes.append(0)

            bytes[int((valve_count - x - 1) / 8)] = 1 << x % 8
            self.valves.append(CwValve(bytearray(bytes)))

    def flush(self):
        bytes_to_send = bytearray([0, 0])
        for valve in self.valves:
            if valve.is_on:
                bytes_to_send[0] |= valve.address[0]
                bytes_to_send[1] |= valve.address[1]
            else:
                bytes_to_send[0] &= ~valve.address[0]
                bytes_to_send[1] &= ~valve.address[1]

        # self.serial.write(bytes_to_send)
