# -*- coding:utf-8 -*-
import time
import serial
# eliochannel 관련 모듈 임포트
from elio_uart.comm.eliochannel import eliochannel
from elio_uart.comm.elioprotocol import ElioProtocol
from elio_uart.comm.packet_t import packet_t

if __name__ == "__main__":

    PORT = '/dev/tty.wchusbserial14410'

    ser = serial.serial_for_url(PORT, baudrate=115200, timeout=1)

    with eliochannel(ser, ElioProtocol, packet_t) as p:

        p.decideToUseSensor("ON", "OFF", "OFF");

        while p.isDone():
            p.sendDC(-90, 90)
            time.sleep(1)
            p.sendDC(0, 0)
            time.sleep(1)

            p.sendServo(30, 0)
            time.sleep(1)

            p.sendServo(0, 0)
            time.sleep(1)

            p.sendIO("IO3", 100)
            time.sleep(1)

            p.sendIO("IO3", 0)
            time.sleep(1)
