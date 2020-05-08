import cv2
import pickle
import pytesseract
from  matplotlib import pyplot
frame=cv2.VideoCapture( "/home/nbp/Pictures/radar_anim.gif")
frame=cv2.VideoCapture( "/home/nbp/Pictures/radar_anim.gif")
gif=cv2.VideoCapture( "/home/nbp/Pictures/radar_anim.gif")
img = cv2.imread("nbp.png")

frame=gif.read()
frame=gif.read()
frame=gif.read()
cv2.imwrite("tadeja5.png", frame[1])
start=(330,280)
stop=(330,390)
color = (0, 255, 0)
thickness = 9
image = cv2.line(img, start, stop, color, thickness)
start=(330,280)
stop=(330,390)
color = (0, 255, 0)
thickness = 9
start=(210,350)
stop=(370,350)
color = (0, 255, 0)
img = cv2.imread("tadeja2.png")
#img = cv2.imread("bitcoin.jpeg")
thickness = 9
#image = cv2.line(frame[1], start, stop, color, 2)
window_name = 'Image'
#cv2.imshow('tadeja4.png', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
#print(frame)
startY = 25
endY = 40
#startY = 7
#endY = 24
startX = 8
endX =150
text = pytesseract.image_to_string(img)
roi = img[startY:endY, startX:endX]
config = ("-l eng --oem 1 --psm 7")
text = pytesseract.image_to_string(roi, config=config)
text=text+"tadeja"
print(text)
print(img[366,266])


def bresenham_line(x0, y0, x1, y1):
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    switched = False
    if x0 > x1:
        switched = True
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    if y0 < y1:
        ystep = 1
    else:
        ystep = -1

    deltax = x1 - x0
    deltay = abs(y1 - y0)
    error = -deltax / 2
    y = y0

    line = []
    for x in range(x0, x1 + 1):
        if steep:
            line.append((y,x))
        else:
            line.append((x,y))

        error = error + deltay
        if error > 0:
            y = y + ystep
            error = error - deltax
    if switched:
        line.reverse()
    return line

