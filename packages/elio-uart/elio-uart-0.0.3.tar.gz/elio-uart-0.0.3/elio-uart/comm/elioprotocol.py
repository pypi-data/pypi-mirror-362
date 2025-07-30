# -*- coding:utf-8 -*-
import binascii

from elio.comm.protocol import Protocol
import struct

UDP = 0x30
CMD_EXECUTE = 0x4D


class ElioProtocol(Protocol):
    # __dc1 = None;
    # __dc2 = None;
    # __sv1 = None;
    # __sv2 = None;
    # __v3 = None;
    # __v5 = None;
    # __io1 = None;
    # __io2 = None;
    # __io3 = None;
    # __io4 = None;
    #
    # __ultra = None;
    # __line1 = None;
    # __line2 = None;

    def __init__(self):
        self.initialize()
        self.ultra = 0
        self.line1 = 0
        self.line2 = 0

    def initialize(self):
        self.dc1 = 0
        self.dc2 = 0
        self.sv1 = 0
        self.sv2 = 0
        self.v3 = 0
        self.v5 = 0
        self.io1 = 0
        self.io2 = 0
        self.io3 = 0
        self.io4 = 0

    def decideToUseSensor(self, ultra, line1, line2):
        self.ultra = ultra
        self.line1 = line1
        self.line2 = line2

        buffer = struct.pack('bbbbbbbbbbbbbbb', UDP, CMD_EXECUTE,
                             self.dc1,
                             self.dc2,
                             self.sv1,
                             self.sv2,
                             self.v3,
                             self.v5,
                             self.io1,
                             self.io2,
                             self.io3,
                             self.io4, self.ultra, self.line1, self.line2)

        self.write(buffer, 15)




        self.sendDeviceData()

    def connection_made(self, transport):
        self.transport = transport
        self.running = True

    def connection_lost(self, exc):
        self.transport = None

    def data_received(self, data, len):
        cmd = data[0]
        udp = data[1]

        self.DC1 = data[2]
        self.DC2 = data[3]

        self.SV1 = data[4]
        self.SV2 = data[5]

        self.V3 = data[6]
        self.V5 = data[7]

        self.IO1 = data[8]
        self.IO2 = data[9]
        self.IO3 = data[10]
        self.IO4 = data[11]

        self.sensor_mask = data[12];

        self.SONIC = (data[13] | data[14] << 8)
        # self.LINE1 = (data[14] | data[15] << 8) == 0 if 1 else 0
        # self.LINE2 = (data[16] | data[17] << 8) == 0 if 1 else 0
        self.LINE1 = (data[15] ) == 0 if 1 else 0
        self.LINE2 = (data[16] ) == 0 if 1 else 0
        print("dc1=", self.dc1, ", dc2=", self.dc2, ", sv1=", self.sv1, ", sv2=", self.sv2,
              ", io1=", self.io1, ", io2=", self.io2, ", io3=", self.io3, ", io4=", self.io4,
              ",sesnor_mask=",  self.sensor_mask, ", SONIC=", self.SONIC, ", LINE1=", self.LINE1, ", LINE2=", self.LINE2)

    def write(self, data, len):
        # print(binascii.hexlify(data))
        self.transport.packet.send_packet(data, len)

    def write_packet(self, data):
        # print(data)
        self.transport.write(data)

    def isDone(self):
        return self.running

    def initializeData(self):
        pass
        # init = bytearray([0x20, 0x50, 0x00, 0x00, 0x00])
        # p.write(init)

    def sendIO(self, which_io, value):
        print('sendIO')
        if (which_io == "3V"):
            self.v3 = value
        elif (which_io == "5V"):
            self.v5 = value
        elif (which_io == "IO1"):
            self.io1 = value
        elif (which_io == "IO2"):
            self.io2 = value
        elif (which_io == "IO3"):
            self.io3 = value
        elif (which_io == "IO4"):
            self.io4 = value

        self.sendDeviceData()

    def sendDC(self, dc1, dc2):
        print('sendDC')
        self.dc1 = dc1
        self.dc2 = dc2

        self.sendDeviceData()

    def sendServo(self, sv1, sv2):
        print('sendServo')
        self.sv1 = sv1
        self.sv2 = sv2
        self.sendDeviceData()

    def sendDeviceData_original(self):
        # buffer = bytearray(15)
        buffer = struct.pack('bbbbbbbbbbbbbbb', UDP, CMD_EXECUTE,
                             self.dc1,
                             self.dc2,
                             self.sv1,
                             self.sv2,
                             self.v3,
                             self.v5,
                             self.io1,
                             self.io2,
                             self.io3,
                             self.io4, self.ultra, self.line1, self.line2)

        self.write(buffer, 15)

    def sendDeviceData(self):
        # buffer = bytearray(15)
        buffer = struct.pack('bbbbbbbbbbbb',
                             CMD_EXECUTE,
                             10,
                             self.dc1,
                             self.dc2,
                             self.sv1,
                             self.sv2,
                             self.v3,
                             self.v5,
                             self.io1,
                             self.io2,
                             self.io3,
                             self.io4)

        self.write(buffer, 12)

        # buffer[0] = UDP
        # buffer[1] = CMD_EXECUTE
        #
        # buffer[2] = self.dc1
        # buffer[3] = self.dc2
        # buffer[4] = self.sv2
        # buffer[6] = self.sv1
        #         # buffer[5] = self.v3
        # buffer[7] = self.v5
        # buffer[8] = self.io1
        # buffer[9] = self.io2
        # buffer[10] = self.io3
        # buffer[11] = self.io4
        #
        # buffer[12] = self.ultra
        # buffer[13] = self.line1
        # buffer[14] = self.line2
        #
        # self.write(bytearray(buffer), 15)

    def sendTXRX(self):

        print('sendTXRX')
        buffer = bytearray(3)
        # buffer[0] = UDP
        buffer[0] = 0xf4#0xf5
        buffer[1] = 1
        buffer[2] = 1;
        self.write(bytearray(buffer), 3)
