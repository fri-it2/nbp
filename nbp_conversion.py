import string
chs = string.digits + string.ascii_uppercase
chs_len=len(chs)
def t(start, chs):
    """Convert decimal address to ascci address

    :param start: NBP adress in decimal:Big Endian Byte Order: The most significant byte (the "big end") of the data is placed at the byte with the lowest address
    :param chs:tsring of all digits and ascii upper
    :return:NBP adress in ASCII
    """

    if start == 0:
        return ''
    chs_len = len(chs)
    ch = chs[start%chs_len]
    return ch + t(start//chs_len, chs)
def pretvorba(naslov, chs,number):
    """convert ascci NBP adress to decimal NBP adress

    :param naslov: NBP address ASCII: Big Endian Byte Order: The most significant byte (the "big end") of the data is placed at the byte with the lowest address
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
    return pretvorba(naslov,chs, number)

r=t(653331952, chs)
print(r)
r=t(64716160330,chs)
naslov="S50PTP"
naslov=naslov[::-1]
s=pretvorba("ASZ65S",chs,0)
s1=pretvorba("S56ZSA",chs,0)
s2=pretvorba(naslov,chs,0)
print(r)
print(s1)
print(s)
print(s2)
print(t(1561529872,chs))
