import string
import pdb
import numpy as np
chs = string.digits + string.ascii_uppercase
chs_len=len(chs)
def convert36ToAscii(start, chs):
    """Convert decimal address to ascci address

    :param start: NBP adress in decimal reverse:Big Endian Byte Order: The most significant byte (the "big end") of the data is placed at the byte with the lowest address
    :param chs:tsring of all digits and ascii upper
    :return:NBP adress in ASCII
    """

    if start == 0:
        return ''
    chs_len = len(chs)
    ch = chs[start%chs_len]
    return ch + convert36ToAscii(start//chs_len, chs)
def convertAsciiTo36(naslov, chs,number):
    """convert ascci NBP adress to decimal NBP address

    :param naslov: NBP address ASCII reverse: Big Endian Byte Order: The most significant byte (the "big end") of the data is placed at the byte with the lowest address
    :param chs: string of all digits and ascii upper
    :param number:
    :return: NBP in decimal
    """
    number = (number+chs.index(naslov[0]))*chs_len
    naslov = naslov[1:]
    if naslov == "":
        return number / chs_len
#    import pdb
 #   pdb.set_trace()
    return convertAsciiTo36(naslov,chs, number)
def convertDecBin(num):
    """

    :param num  NBP adress in dec:
    :return: NBP in binary
    """

    return
def convertBinDec(num):
    """convert binary NBP adress to decimal NBP address

    :param num:
    :return:
    """

    return

def convertOctDec(num):
    """ convert octal NBP address to dec NBP address

    :param num: 4x octal NBP adrdress [13,13,14,12], 32 bit, 4 x8 bit
    :return : decimal NBP address
    """
    if len(num)!=4:
        print num
        return 0
    return np.sum(np.array([1,256,256*256,256*256*256])*np.array(num))




def convertNumber32Bit(stevilo, delitelj):
    """ convert dec NBP to 32 bit number: 4 x 8bit in dec

    :param stevilo: decimal NBP
    :param delitelj: 256*256*256
    :param naslov: NBP in 32 bit: 4x 8bit, array
    :return:

    Example
    convertNumber32bit(653331952,256*256*256)
    """
    deljenec=stevilo / delitelj
    ostanek = stevilo % delitelj
    try:
        naslov
    except NameError:
        naslov = []

    naslov.append(deljenec)
    #print
    #pdb.set_trace()
    if ostanek <= 256:
        naslov.append(ostanek)

        return naslov
    #print(naslov)
    #pdb.settrace()

    return naslov+convertNumber32Bit(ostanek,delitelj/256)

#r=convertDecAscii(653331952, chs)
#print(r)
#r=convertDecAscii(64716160330,chs)
#naslov="S50PTP"
#naslov=naslov[::-1]
s1=convertAsciiTo36("ASZ65S",chs,0)
#s1=convertAsciiTo36("S56ZSA",chs,0)
#s2=convertAsciiTo36(naslov,chs,0)
#print(r)
print(s1)
#print(s)
#print(s2)
#print(convertDecAscii(1561529872,chs))
#a=convertNumber32Bit(653331952,256*256*256)
#print(a[::-1])
#a=convertOctDec([ 240,13,241,38])
#print(a)
