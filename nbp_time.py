datetime import datetime
from threading import Thread
import time
import serial
from collections import deque
import json
import datetime
import string
import csv
import timeit

stevilovozlisc = 0
SLIP_END = 0xC0  # declared in hexa Frame End
serial_port = serial.Serial(port='/dev/ttyUSB1', baudrate=115200, timeout=1)
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
# do ptp-JA
byteArrayPTP = [
                    255,
                    255,
                    255,
                    255,
                    240,
                    13,
                    241,
                    38, 16, 14, 19, 93]
bytearryPTdoFE = [176, 10, 16, 60]+[96, 106, 106, 107]+[128, 73, 71, 74]+[128, 171, 13, 52]
bytearrayMuci =   [ 0,
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
pot = byteArrayPTP + byteArrayPTP + bytearrayMuci

byteArray=byteArray+byteArray1+byteArray_ost
def read(timebyte):
    print timebyte
    while True:
        writeToSerialPort(timebyte)
        start_time = time.time()
        while True:
            if ((time.time()-start_time)>9):
                break

            time.sleep(0.0000001)

            data = serial_port.read()
            #print ord(data)
            if len(data) ==  0:
                break
            if ord(data) == ord('>'):
                data = serial_port.read()
                if len(data)==0:
                    break
                if ord(data)==ord('!'):
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
    t=do_time(pot)
    time.sleep(1)
    with open('S53FE.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        #t={'cas:'+''+str(t)+'','datum:'+'+str(datetime.datetime.now())+'''}
        t=[str(t)]+[str(datetime.datetime.now())]
        print(t)
        writer.writerow(t)
    print(t)
