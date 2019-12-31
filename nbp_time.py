from datetime import datetime
from threading import Thread
import time
import serial
from collections import deque
import json

import string
import csv
import timeit

stevilovozlisc = 0
SLIP_END = 0xC0  # declared in hexa Frame End
serial_port = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
SLIP_ESC = 0xDB  # Frame Escape
SLIP_ESC_END = 0xDC  # transposed Frame End
SLIP_ESC_ESC = 0xDD
readBufferQueue = deque([])
chs = string.digits + string.ascii_uppercase
bytedate=[]
byteArray2 = [
                    255,
                    255,
                    255,
                    255,
                    240,
                    13,
                    241,
                    38, 16, 14, 19, 93,
                    0,
                    0,
                    0,
                    0,
                    240,
                    13,
                    241,
                    38,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    47,
                    47,
                    47,
                    47,
                    ord('>'),ord('!'),]
byteArray1=[240, 13, 241, 38, 16, 14, 19, 93, 80, 34, 19, 93, 144, 0, 16, 60, 176, 10, 16, 60, 80, 101, 106, 107, 96, 106, 106, 107, 80, 58, 71, 74, 96, 63, 71, 74, 96, 161, 13, 52, 128, 171, 13, 52]

#0, 206, 16, 1
byteArray = [
                    255,
                    255,
                    255,
                    255,

                ]

byteArray_ost = [
                 0,
                 0,
                 0,
                 0,
                 240,
                 13,
                 241,
                 38,

                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 47,
                 47,
                 47,
                 47,
ord('>'),ord('!')]
byteArray=byteArray+byteArray1+byteArray_ost
def read(timebyte):
    print timebyte
    writeToSerialPort(timebyte)
    while True:
        time.sleep(0.0000001)
        data = serial_port.read()
        print ord(data)
        if ord(data) == ord('!'):
            print ord(data)
            return

def do_time( bytedate):
    """
    This function measure
    :param bytedate:
    :return:
    """
    t = timeit.Timer("read("+str(bytedate)+")")

    time = t.timeit(1)
    return time
def writeToSerialPort( byteArray):
    """
     This function accept a byte array and write it to the serial port
    :param serialFD: opened serial port file descriptor
    :param byteArray: accepted a byte array
    :return:
    """

    encodedSLIPBytes = encodeToSLIP(byteArray)

    byteString = ''.join(
        chr(b) for b in encodedSLIPBytes
    )  # convert byte list to a string

    serial_port.write(byteString)

def encodeToSLIP( byteList):
    """This function takes a byte list, encode it in SLIP protocol and return the encoded byte list
    :param byteList: bytelist
    :return: tempSLIPBuffer: SLIP encoded byte
    """

    tempSLIPBuffer = []
    tempSLIPBuffer.append(SLIP_END)
    for i in byteList:
        if i == SLIP_END:
            tempSLIPBuffer.append(SLIP_ESC_END)
        elif i == SLIP_ESC:
            tempSLIPBuffer.append(SLIP_ESC_ESC)
        else:
            tempSLIPBuffer.append(i)
    tempSLIPBuffer.append(SLIP_END)
    return tempSLIPBuffer


import __builtin__
__builtin__.__dict__.update(locals())

while True:
    t=do_time(byteArray2)
    time.sleep(0.0002)
    with open('S53FE.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(str(t))
    print(t)
