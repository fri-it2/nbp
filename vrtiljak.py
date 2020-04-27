##### Potovanje po galaksiji z vrtiljakom KR5600 - S53MV 18.02.2019 #####

#izvajanje potrebuje najmanj python-2.7.12 in pyserial-2.7.win32_py3k
import time, math, serial	#uporabljene funkcije

port='COM3'	#ime zaporednega vmesnika
pomlad=0.275	#poenostavljeno pomladisce za Julijanski koledar (del kroga)
elmin=5.0	#minimalna varna elevacija vrtiljaka

casracun=18	#interval racunanja (sekunde)
stracun=86400/casracun	#stevec racunov omejen na 24h!

sirina=45.948	#zemljepisna sirina opazovalca v stopinjah (+sever)
dolzina=13.634	#zemljepisna dolzina opazovalca v stopinjah (+vzhod)

cs=math.cos(math.radians(sirina))	#smerni vektorji opazovalca ovzhod, osever in ogor
ss=math.sin(math.radians(sirina))
cd=math.cos(math.radians(dolzina))
sd=math.sin(math.radians(dolzina))
ovzhod=[-sd,cd,0]
osever=[-ss*cd,-ss*sd,cs]
ogor=[cs*cd,cs*sd,ss]

def skalar(a,b):		#skalarni produkt dveh vektorjev
	return (a[0]*b[0])+(a[1]*b[1])+(a[2]*b[2])

def azel(s,ov,os,og):		#izracunaj azimut in elevacijo za opazovalca
	az=math.degrees(math.atan2(skalar(s,ov),skalar(s,os)))	#azimut
	if az<0:
		az=az+360
	el=math.degrees(math.asin(skalar(s,og)))		#elevacija
	return az,el

def pw(s):			#izpis na zaslon in v izhodni zapis brez nove vrste
	print s,
	iz.write(s+' ')

def pwn(s):			#izpis na zaslon in v izhodni zapis z novo vrsto
	print s
	iz.write(s+'\r\n')

def datumura(t):		#izpisi trenutni datum in uro
	leto=t[0]
	mesec=t[1]
	dan=t[2]
	pw(str(leto)+'-'+str(mesec)+'-'+str(dan))	#izpisi datum
	ura=t[3]
	minuta=t[4]
	sekunda=t[5]
	pw(str(ura)+':'+str(minuta)+':'+str(sekunda))	#izpisi uro

def smerneba(ra,dec,t):		#izracunja smerni vektor neba ob dani uri in datumu
	ddan=(((t[5]/60.0)+t[4])/60.0+t[3])/24.0	#decimalni del dneva
	pleto=t[0]-int((t[0]/4)*4)			#dan v stiriletju
	sdan=t[2]
	dmesec=[31,28,31,30,31,30,31,31,30,31,30,31]	#dodaj stevilo dni v mesecih
	n=1	
	while n<t[1]:
		sdan=sdan+dmesec[n-1]
		if pleto==0:				#popravek za prestopno leto
			if n==2:
				sdan=sdan+1
		n=n+1
	dleto=[366,365,365,365]				#dodaj stevilo dni v letih
	n=0
	while n<pleto:
		sdan=sdan+dleto[n]
		n=n+1
	zdolzina=(ddan*(1+(1/365.25)))+(sdan/365.25)	#izracunaj Julijansko zemljepisno dolzino
	zdolzina=zdolzina+pomlad			#dodaj zacetni polozaj pomladisca
	zdolzina=(1+int(zdolzina)-zdolzina)*360.0	#rezultat v stopinje (+vzhod)
	zdolzina=zdolzina+ra				#izracunaj smerni vektor neba
	cr=math.cos(math.radians(zdolzina))
	sr=math.sin(math.radians(zdolzina))
	cd=math.cos(math.radians(dec))
	sd=math.sin(math.radians(dec))
	return [cd*cr,cd*sr,sd]

def gllvrd(glon,glat):				#galakticne koordinate v rektascenzijo,deklinacijo
	glon=glon-32.9				#galakticna dolzina dviznega vozla galaksije 32.9
	glon=math.radians(glon)			#pretvorba v radiane
	glat=math.radians(glat)
	x=math.cos(glon)*math.cos(glat)		#pretvorba v kartezicne koordinate
	y=math.sin(glon)*math.cos(glat)
	z=math.sin(glat)
	nagib=math.radians(62.8)		#nagib ravnine galaksije 62.8
	yy=y*math.cos(nagib)-z*math.sin(nagib)
	z=y*math.sin(nagib)+z*math.cos(nagib)
	ra=math.degrees(math.atan2(yy,x))	#pretvorba v krogelne koordinate
	dec=math.degrees(math.asin(z))
	ra=ra+282.9				#rektascenzija dviznega vozla galaksije 282.9
	if ra>360:				#omeji obmocje rektascenzije 0...360
		ra=ra-360
	return ra,dec

#odpri comport port, 9600bps, 8bit, brez paritete
comport=serial.Serial(port,9600,timeout=0.1)

def konstante():	#postavi casovne konstante KR5600
	comport.write('S'+chr(8))	#dusenje AZ
	comport.write('T'+chr(8))	#dusenje EL
	comport.write('U'+chr(22))	#vztrajnost AZ
	comport.write('V'+chr(22))	#vztrajnost EL

#konstante pretvorbe podatkov vrtiljaka (obvezno cela stevila)
el0=16
el90=130
azm180=14
az180=248

def vrtiljak(el0,el90,azm180,az180):	#azimut in elevacija vrtiljaka KR5600
	s=comport.read(999)		#izprazni vmesnik comporta
	ss='Vrtiljak '
	comport.write('P')	#vprasaj za parametre vrtiljaka KR5600
	s=comport.read(99)
	if len(s)<>20:		#napaka pri prenosu podatkov?
		ss=ss+'ni podatka!!!'
	else:
		ss=ss+str(ord(s[3]))+'/'+str(ord(s[4]))		#polozaj rotatorja
		sa=(ord(s[3])-azm180)*360.0/(az180-azm180)-180	#preracunaj azimut
		if sa<0:
			sa=sa+360
		se=(ord(s[4])-el0)*90.0/(el90-el0)		#preracunaj elevacijo
		ss=ss+str(' AZ=%5.1f'%(sa))+str('/EL=%4.1f'%(se))	#azimut/elevacijo
	return ss	#izhodni string

def polozaj(el0,el90,azm180,az180,azimut,elevacija,elmin):	#postavi polozaj KR5600
	sa=azimut					#pretvorba obmocja azimuta
	if sa>180:
		sa=sa-360
	sa=sa+180
	sa=int((sa/360.0)*(az180-azm180)+azm180+0.5)	#preracunavanje azimuta
	if sa<azm180:
		sa=azm180
	if sa>az180:
		sa=az180
	se=int((elevacija/90.0)*(el90-el0)+el0+0.5)	#preracunavanje elevacije
	if se<el0:
		se=el0
	if se>el90:
		se=el90
	if elevacija>=elmin:				#postavi veljaven polozaj
		comport.write('Q'+chr(sa))
		comport.write('R'+chr(se))

t=time.ctime()			#ime izhodnega zapisa
f=t[20:24]+t[4:7]+t[8:10]+t[11:13]+t[14:16]+t[17:19]+'.txt'
iz=open(f,'w')			#odpri izhodni zapis

pwn('*** Potovanje po galaksiji z vrtiljakom KR5600 ***')
t=time.gmtime()			#precitaj datum in uro realnega casa racunalnika (UTC)
datumura(t)			#izpisi trenutni datum in uro
print vrtiljak(el0,el90,azm180,az180)	#izpisi azimut in elevacijo vrtiljaka KR5600

glon=input('Vstavi zacetno galakticno dolzino: ')
glat=input('Vstavi zacetno galakticno sirino: ')
klon=input('Vstavi korak galakticne dolzine: ')
klat=input('Vstavi korak galakticne sirine: ')

pwn('*** Nastavitve za korak '+str(casracun)+' sekund ***')
pwn('Zacetna galakticna dolzina '+str(glon))
pwn('Zacetna galakticna sirina '+str(glat))
pwn('Korak galakticne dolzine '+str(klon))
pwn('Korak galakticne sirine '+str(klat))

while stracun>0:			#zanka racunanja
	t=time.gmtime()			#precitaj datum in uro realnega casa racunalnika (UTC)
	datumura(t)			#izpisi trenutni datum in uro

	pw(str('GLON=%5.1f'%(glon))+str('/GLAT=%4.1f'%(glat)))

	ra,dec=gllvrd(glon,glat)	#galakticne koordinate v rektascenzijo,deklinacijo
	pwn(str('RA=%5.1f'%(ra))+str('/DEC=%4.1f'%(dec)))

	smer=smerneba(ra,dec,t)		#izracunja smerni vektor neba ob dani uri in datumu
	azimut,elevacija=azel(smer,ovzhod,osever,ogor)	#izracunaj azimut in elevacijo za opazovalca
	pw(str('AZ=%5.1f'%(azimut))+str('/EL=%4.1f'%(elevacija)))

	konstante()	#postavi casovne konstante KR5600
	polozaj(el0,el90,azm180,az180,azimut,elevacija,elmin)	#postavi polozaj KR5600
	pwn(vrtiljak(el0,el90,azm180,az180))	#izpisi azimut in elevacijo vrtiljaka KR5600

	stracun=stracun-1		#zakljucek zanke racunanja
	time.sleep(casracun)		#cakanje do naslednjega racuna
	glon=glon+klon			#povecaj glon in glat za korak
	glat=glat+klat

iz.close()		#zapri izhodni zapis

#konec programa
