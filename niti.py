
import datetime
from threading import Thread
import time
import serial
from collections import deque
import json
import nbp_pretvorba
import string
import csv
keys = []
nodes = {}

SLIP_END = 0xC0  # declared in hexa Frame End
zacetek_vozlisca = 0
SLIP_ESC = 0xDB  # Frame Escape
SLIP_ESC_END = 0xDC  # transposed Frame End
SLIP_ESC_ESC = 0xDD
readBufferQueue = deque([])
chs = string.digits + string.ascii_uppercase
f = open("logging", "a")
f.write("logging")
class Odgovor(Thread):
    def __init__(self, delay, serial_port):
        Thread.__init__(self)
        self.delay = delay
        self.serial_port = serial_port
        self.zacetek_vozlisca = 0
        self.time = 0
    def run(self):
        f.write("Zacetek odgovor \n")
        f.write(str(datetime.datetime.now())+"\n")
        #print(readBufferQueue)

        while True:
            data = self.serial_port.read()

            readBufferQueue.append(data)
            self.zacetek_vozlisca =+1

            #print(readBufferQueue)
            if ( self.zacetek_vozlisca!= 1 or  self.zacetek_vozlisca!= 0) and data == 'xc0':
                f.write("Konec  odgovor\n")
                f.write(str(datetime.datetime.now())+"\n")
                print("eno vozlisce")
                time.sleep(self.delay)

                self.zacetek_vozlisca = 0

                print("eno vozlisce")


            # print(data)



class Vprasanje(Thread):
    # franspose Frame Escape

    def __init__(self, delay, serial_port,stevilovozlisc,keys,nodes,string_nodes):
        Thread.__init__(self)
        self.delay = delay
        self.serial_port = serial_port
        self.stevilovozlisc =  stevilovozlisc
        self.keys = keys
        self.nodes = nodes
        self.string_nodes = string_nodes

    def run(self):
        #print(byteArray)
        f.write("Zacetek vprasanje \n")
        f.write(str(datetime.datetime.now())+"n")
        while True:
            if self.stevilovozlisc == 0:

                byteArray = [
                    255,
                    255,
                    255,
                    255,
                    240,
                    13,
                    241,
                    38, 16, 14, 19, 93,
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

            else:
                byteArray = [
                    255,
                    255,
                    255,
                    255,

                ]
                f.write(str(keys)+"\n")
                key_node = self.keys[0]
                f.write(str(key_node)+"")
                self.keys.remove(self.keys[0])
                byteArray=byteArray+self.nodes[str(key_node)]["path"]
                byteArray_ost= [255,
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
                self.nodes.pop(str(key_node))
                byteArray = byteArray + byteArray_ost


            f.write(str(byteArray)+"\n")
            self.writeToSerialPort(byteArray)
            f.write("Kaj smo zapisali" +"\n")
            f.write(str(byteArray)+"\n")
            f.write("Kaj smo prebrali"+"\n")
            f.write(str(readBufferQueue))
            print(str(datetime.datetime.now()))


            i=0
            while (True):
                i=+1
                f.write("Vprasanje"+str(i)+"\n")
                f.write(str(datetime.datetime.now())+"\n")
                try:
                #{"vozlisce1":{"id":1,"source":[255,28,25,16],"destinationation":[34,15,18],"live_time":[255,255,255,255], "signal":100, "noise":99,"path":[[255,8,9,20],[244,8,9]]}}
                    char = ord(readBufferQueue.popleft())
                    vozlisce='{"'+str(self.stevilovozlisc)+'":{"lifetime":'
                    livetime=[]
                    #izracun zivljenkse dobe
                    if char == 192 and len(readBufferQueue) == 1:
                        print(json.dumps(nodes))



                        break
                    if char==192:
                        for i in range(1,5):
                            num = ord(readBufferQueue.popleft() )
                            if num == 192:
                                num = ord(readBufferQueue.popleft())
                            livetime.append(num)

                        vozlisce += str(livetime)+","
                        receiver=[]
                        # izracun poti do vozlisca
                        for i in range(1,5):
                            receiver.append(ord(readBufferQueue.popleft()))
                        vozlisce += '"receiver":' + str(receiver) + ","
                        for i in range(1,5):
                            readBufferQueue.popleft()

                        path=[]
                        while True:
                            string=ord(readBufferQueue.popleft())
                            string1=ord(readBufferQueue.popleft())
                            string2=ord(readBufferQueue.popleft())
                            string3=ord(readBufferQueue.popleft())
                            if string == 0 and string1 == 0 and string2 == 0 and string3 == 0:
                                break
                            path.append(string)
                            path.append(string1)
                            path.append(string2)
                            path.append(string3)
                        vozlisce += '"path":' + str(path) + ","

                        #y=json.loads(vozlisce)
                        #nodes.update(y)


                        sosed_oct = path[-8:-4]
                        node_oct = path[-4::]
                        neightbour = nbp_pretvorba.convert36ToAscii(nbp_pretvorba.convertOctDec(sosed_oct),chs)
                        node = nbp_pretvorba.convert36ToAscii(nbp_pretvorba.convertOctDec(node_oct),chs)
                        cvs_node=[]
                        cvs_node.append(neightbour)
                        cvs_node.append(node)
                        print('sosed:{first} vozlisce: {last} pot:{pot}'.format(first=neightbour, last=node ,pot=path))



                        vozlisce += '"sosed":"' + neightbour + '",' + '"vozlisce":"' +node + '"}}'
                        if neightbour[0] != 'S' or node[0] != 'S':
                            with open('napaka29.csv', 'a') as csvFile:
                                writer = csv.writer(csvFile)
                                writer.writerow(cvs_node)
                            continue
                        print(self.string_nodes)
                        if self.string_nodes.find(node) != -1:
                            continue
                        with open('node29.csv', 'a') as csvFile:
                            writer = csv.writer(csvFile)
                            writer.writerow(cvs_node)
                        y = json.loads(vozlisce)
                        self.nodes.update(y)
                        self.keys.append(self.stevilovozlisc)
                        self.stevilovozlisc +=1
                        if self.string_nodes.find(neightbour) != -1:
                            continue
                        self.string_nodes += neightbour + " "

                        f.write(self.string_nodes)

                        #print(self.nodes)
                    #print(char)
                    #izracun poti do vozlisca
                    f.write("Vprasanje" + str(i)+"\n")
                    f.write(str(datetime.datetime.now())+"\n")
                except IndexError or NameError:
                    break

            readBufferQueue.clear()
            f.write("Vprasanje Konec:")
            f.write(str(datetime.datetime.now())+"\n")
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
        port='/dev/ttyUSB0',
        baudrate=115200,
        bytesize=8,
        parity='N',
        stopbits=1,
        xonxoff=False,
        rtscts=False,
    )

    vprasanje = Vprasanje(3, serial_port,0,[],{},"")
    odgovor = Odgovor(0.04, serial_port)
    vprasanje.start()
    odgovor.start()


if __
import datetime
from threading import Thread
import time
import serial
from collections import deque
import json
import nbp_pretvorba
import string
import csv
keys = []
nodes = {}

SLIP_END = 0xC0  # declared in hexa Frame End
zacetek_vozlisca = 0
SLIP_ESC = 0xDB  # Frame Escape
SLIP_ESC_END = 0xDC  # transposed Frame End
SLIP_ESC_ESC = 0xDD
readBufferQueue = deque([])
chs = string.digits + string.ascii_uppercase
f = open("logging", "a")
f.write("logging")
class Odgovor(Thread):
    def __init__(self, delay, serial_port):
        Thread.__init__(self)
        self.delay = delay
        self.serial_port = serial_port
        self.zacetek_vozlisca = 0
        self.time = 0
    def run(self):
        f.write("Zacetek odgovor \n")
        f.write(str(datetime.datetime.now())+"\n")
        #print(readBufferQueue)

        while True:
            data = self.serial_port.read()

            readBufferQueue.append(data)
            self.zacetek_vozlisca =+1

            #print(readBufferQueue)
            if ( self.zacetek_vozlisca!= 1 or  self.zacetek_vozlisca!= 0) and data == 'xc0':
                f.write("Konec  odgovor\n")
                f.write(str(datetime.datetime.now())+"\n")
                print("eno vozlisce")
                time.sleep(self.delay)

                self.zacetek_vozlisca = 0

                print("eno vozlisce")


            # print(data)



class Vprasanje(Thread):
    # franspose Frame Escape

    def __init__(self, delay, serial_port,stevilovozlisc,keys,nodes,string_nodes):
        Thread.__init__(self)
        self.delay = delay
        self.serial_port = serial_port
        self.stevilovozlisc =  stevilovozlisc
        self.keys = keys
        self.nodes = nodes
        self.string_nodes = string_nodes

    def run(self):
        #print(byteArray)
        f.write("Zacetek vprasanje \n")
        f.write(str(datetime.datetime.now())+"n")
        while True:
            if self.stevilovozlisc == 0:

                byteArray = [
                    255,
                    255,
                    255,
                    255,
                    240,
                    13,
                    241,
                    38, 16, 14, 19, 93,
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

            else:
                byteArray = [
                    255,
                    255,
                    255,
                    255,

                ]
                f.write(str(keys)+"\n")
                key_node = self.keys[0]
                f.write(str(key_node)+"")
                self.keys.remove(self.keys[0])
                byteArray=byteArray+self.nodes[str(key_node)]["path"]
                byteArray_ost= [255,
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
                self.nodes.pop(str(key_node))
                byteArray = byteArray + byteArray_ost


            f.write(str(byteArray)+"\n")
            self.writeToSerialPort(byteArray)
            f.write("Kaj smo zapisali" +"\n")
            f.write(str(byteArray)+"\n")
            f.write("Kaj smo prebrali"+"\n")
            f.write(str(readBufferQueue))
            print(str(datetime.datetime.now()))


            i=0
            while (True):
                i=+1
                f.write("Vprasanje"+str(i)+"\n")
                f.write(str(datetime.datetime.now())+"\n")
                try:
                #{"vozlisce1":{"id":1,"source":[255,28,25,16],"destinationation":[34,15,18],"live_time":[255,255,255,255], "signal":100, "noise":99,"path":[[255,8,9,20],[244,8,9]]}}
                    char = ord(readBufferQueue.popleft())
                    vozlisce='{"'+str(self.stevilovozlisc)+'":{"lifetime":'
                    livetime=[]
                    #izracun zivljenkse dobe
                    if char == 192 and len(readBufferQueue) == 1:
                        print(json.dumps(nodes))



                        break
                    if char==192:
                        for i in range(1,5):
                            num = ord(readBufferQueue.popleft() )
                            if num == 192:
                                num = ord(readBufferQueue.popleft())
                            livetime.append(num)

                        vozlisce += str(livetime)+","
                        receiver=[]
                        # izracun poti do vozlisca
                        for i in range(1,5):
                            receiver.append(ord(readBufferQueue.popleft()))
                        vozlisce += '"receiver":' + str(receiver) + ","
                        for i in range(1,5):
                            readBufferQueue.popleft()

                        path=[]
                        while True:
                            string=ord(readBufferQueue.popleft())
                            string1=ord(readBufferQueue.popleft())
                            string2=ord(readBufferQueue.popleft())
                            string3=ord(readBufferQueue.popleft())
                            if string == 0 and string1 == 0 and string2 == 0 and string3 == 0:
                                break
                            path.append(string)
                            path.append(string1)
                            path.append(string2)
                            path.append(string3)
                        vozlisce += '"path":' + str(path) + ","

                        #y=json.loads(vozlisce)
                        #nodes.update(y)


                        sosed_oct = path[-8:-4]
                        node_oct = path[-4::]
                        neightbour = nbp_pretvorba.convert36ToAscii(nbp_pretvorba.convertOctDec(sosed_oct),chs)
                        node = nbp_pretvorba.convert36ToAscii(nbp_pretvorba.convertOctDec(node_oct),chs)
                        cvs_node=[]
                        cvs_node.append(neightbour)
                        cvs_node.append(node)
                        print('sosed:{first} vozlisce: {last} pot:{pot}'.format(first=neightbour, last=node ,pot=path))



                        vozlisce += '"sosed":"' + neightbour + '",' + '"vozlisce":"' +node + '"}}'
                        if neightbour[0] != 'S' or node[0] != 'S':
                            with open('napaka29.csv', 'a') as csvFile:
                                writer = csv.writer(csvFile)
                                writer.writerow(cvs_node)
                            continue
                        print(self.string_nodes)
                        if self.string_nodes.find(node) != -1:
                            continue
                        with open('node29.csv', 'a') as csvFile:
                            writer = csv.writer(csvFile)
                            writer.writerow(cvs_node)
                        y = json.loads(vozlisce)
                        self.nodes.update(y)
                        self.keys.append(self.stevilovozlisc)
                        self.stevilovozlisc +=1
                        if self.string_nodes.find(neightbour) != -1:
                            continue
                        self.string_nodes += neightbour + " "

                        f.write(self.string_nodes)

                        #print(self.nodes)
                    #print(char)
                    #izracun poti do vozlisca
                    f.write("Vprasanje" + str(i)+"\n")
                    f.write(str(datetime.datetime.now())+"\n")
                except IndexError or NameError:
                    break

            readBufferQueue.clear()
            f.write("Vprasanje Konec:")
            f.write(str(datetime.datetime.now())+"\n")
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
        port='/dev/ttyUSB0',
        baudrate=115200,
        bytesize=8,
        parity='N',
        stopbits=1,
        xonxoff=False,
        rtscts=False,
    )

    vprasanje = Vprasanje(3, serial_port,0,[],{},"")
    odgovor = Odgovor(0.04, serial_port)
    vprasanje.start()
    odgovor.start()


if __name__ == '__main__':
    main()name__ == '__main__':
    main()
