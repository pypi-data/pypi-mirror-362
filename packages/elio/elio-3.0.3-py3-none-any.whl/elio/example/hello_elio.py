# -*- coding:utf-8 -*-

import time

import serial

from elio.comm.eliochannel import eliochannel
from elio.comm.elioprotocol import ElioProtocol
from elio.comm.packet_t import packet_t


if __name__ == "__main__":

    PORT = '/dev/tty.usbmodem4ABD0733AB9D2'
    ser = serial.serial_for_url(PORT, baudrate=115200, timeout=1)

    with eliochannel(ser, ElioProtocol, packet_t) as p:

        p.decideToUseSensor(1, 0, 0)
        while p.isDone():
            p.sendDC(-90, 0)
            time.sleep(1)
            p.sendDC(0, 0)
            time.sleep(1)

            p.sendServo(50, 0)
            time.sleep(1)
            p.sendServo(0, 0)
            time.sleep(1)

            p.sendIO("IO4", 100)
            time.sleep(1)
            # p.sendIO("IO4", 0)
            time.sleep(1)
