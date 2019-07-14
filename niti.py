
from threading import Thread
import time
import serial
from collections import deque


SLIP_END = 0xC0  # declared in hexa Frame End

SLIP_ESC = 0xDB  # Frame Escape
SLIP_ESC_END = 0xDC  # transposed Frame End
SLIP_ESC_ESC = 0xDD
readBufferQueue = deque([])


class Odgovor(Thread):
    def __init__(self, delay, serial_port):
        Thread.__init__(self)
        self.delay = delay
        self.serial_port = serial_port

    def run(self):
        print(readBufferQueue)
        i = 0
        while True:
            data = self.serial_port.read()

            readBufferQueue.append(data)

            print(readBufferQueue)
            if i != 1 or i != 0 and data == 'xc0':
                time.sleep(self.delay)

            # print(data)


class Vprasanje(Thread):
    # franspose Frame Escape

    def __init__(self, delay, serial_port):
        Thread.__init__(self)
        self.delay = delay
        self.serial_port = serial_port

    def run(self):

        while True:
            byteArray = [
                255,
                255,
                255,
                255,
                240,
                13,
                241,
                38,16,14,19,93,
                255,
                255,
                255,
                255,
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
                ord('?'),
                13,
            ]

            self.writeToSerialPort(byteArray)

            print(byteArray)
            readBufferQueue.clear()

            time.sleep(self.delay)

    def writeToSerialPort(self, byteArray):
        """
         This function accept a byte array and write it to the serial port
        :param serialFD: opened serial port file descriptor
        :param byteArray: accepted a byte array
        :return:
        """
        encodedSLIPBytes = self.encodeToSLIP(byteArray)

        byteString = ''.join(
            chr(b) for b in encodedSLIPBytes
        )  # convert byte list to a string

        self.serial_port.write(byteString)

    def encodeToSLIP(self, byteList):
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


def main():
    serial_port = serial.Serial(
        port='/dev/ttyUSB1',
        baudrate=9600,
        bytesize=8,
        parity='N',
        stopbits=1,
        xonxoff=False,
        rtscts=False,
    )
    vprasanje = Vprasanje(600, serial_port)
    odgovor = Odgovor(0.4, serial_port)
    vprasanje.start()
    odgovor.start()


if __name__ == '__main__':
    main()
