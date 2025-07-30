# -*- coding:utf-8 -*-
import time
import serial

if __name__ == "__main__":

    PORT = '/dev/tty.wchusbserial14410'

    ser = serial.serial_for_url(PORT, baudrate=115200, timeout=1)

    with eliochannel(ser, ElioProtocol, packet_t) as p:

        # p.decideToUseSensor(1, 1, 1)
        p.sendTXRX();


        while p.isDone():
            p.sendTXRX();
            # p.sendDC(-90, 90)
            # time.sleep(1)
            # p.sendDC(0, 0)
            # time.sleep(1)
            # p.sendServo(0, 0)
            # time.sleep(1)

            # for i in range(-90, 91):
            #     p.sendServo(i, 0);
            #     time.sleep(0.01);
            #     print('->: ',i);

            for i in range(90, -90, -10):
                p.sendServo(i, 0);
                time.sleep(0.05)
                print('<-: ',i);


            # p.sendServo(0, 0)
            # time.sleep(1)


            # p.sendIO("IO3", 100)
            # time.sleep(1)
            # p.sendIO("IO3", 0)
            # time.sleep(1)
