import string
chs = string.digits + string.ascii_uppercase
chs_len=len(chs)
def (start, chs):
    if start == 0:
        return ''
    chs_len = len(chs)
    ch = chs[start%chs_len]
    return ch + t(start//chs_len, chs)
def pretvorba(naslov, chs,number):

    number = (number+chs.index(naslov[0]))*chs_len
    naslov = naslov[1:]
    if naslov == "":
        return number / chs_len
#    import pdb
#    pdb.set_trace()
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
