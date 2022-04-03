#!/usr/bin/env python3

# Christmas tree lights also with editing of light 3d positioning
# based on:
 
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

# How to use position: The position.py file contains the 3 arrays x, y, z, that
# is the 3d positions for each led in the christmas tree. Copy position1.py to position.py
# before starting ctree.py. This is done so that we minimize the damage if we owerwrite one of the
# files by mistake, took me 8 hours to create that file.

 



import sys
import time
from rpi_ws281x import *
import argparse
from position import *
from math import *
from random import *

# LED strip configuration:
LED_COUNT      = 249      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 250   # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_TYPE       = WS2811_STRIP_RGB
PI             = 3.14159265

theta = [0]*LED_COUNT
r = [0]*LED_COUNT

# create polar coordinates array

def norm(value):
    return value - 50
    
def cart2pol():
    deg = 0
    rad = 0
    for p in range(LED_COUNT):
        x = norm(xpos[p])
        y = norm(ypos[p])
        r[p] = int(sqrt(x**2 + y**2))
        rad = atan2(y,x)
        deg = rad/PI*180

        if deg < 0:
            deg += 360
        theta[p] = int(deg)



# reset strip to black
def pixelblack(strip):
    #print("pixelblack")
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
    #strip.show()

def read_single_keypress():
    """Waits for a single keypress on stdin.

    This is a silly function to call if you need to do it a lot because it has
    to store stdin's current setup, setup stdin for reading single keystrokes
    then read the single keystroke then revert stdin back after reading the
    keystroke.

    Returns a tuple of characters of the key that was pressed - on Linux, 
    pressing keys like up arrow results in a sequence of characters. Returns 
    ('\x03',) on KeyboardInterrupt which can happen when a signal gets
    handled.

    """
    import termios, fcntl, sys, os
    fd = sys.stdin.fileno()
    # save old state
    flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
    attrs_save = termios.tcgetattr(fd)
    # make raw - the way to do this comes from the termios(3) man page.
    attrs = list(attrs_save) # copy the stored version to update
    # iflag
    attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK
                  | termios.ISTRIP | termios.INLCR | termios. IGNCR
                  | termios.ICRNL | termios.IXON )
    # oflag
    attrs[1] &= ~termios.OPOST
    # cflag
    attrs[2] &= ~(termios.CSIZE | termios. PARENB)
    attrs[2] |= termios.CS8
    # lflag
    attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                  | termios.ISIG | termios.IEXTEN)
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    # turn off non-blocking
    fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
    # read a single keystroke
    ret = []
    try:
        ret.append(sys.stdin.read(1)) # returns a single character
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save | os.O_NONBLOCK)
        c = sys.stdin.read(1) # returns a single character
        while len(c) > 0:
            ret.append(c)
            c = sys.stdin.read(1)
    except KeyboardInterrupt:
        ret.append('\x03')
    finally:
        # restore old state
        termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
    return tuple(ret)


# set coordinates for each pixel
def setXYZ():
    for p in range(0,24):
        zpos[p] = 25
    for p in range(25,49):
        zpos[p] = 50
    for p in range(50,74):
        zpos[p] = 75
    for p in range(75,99):
        zpos[p] = 100
    for p in range(100,124):
        zpos[p] = 125
    for p in range(125,149):
        zpos[p] = 150
    for p in range(150,174):
        zpos[p] = 175
    for p in range(175,199):
        zpos[p] = 200
    for p in range(200,224):
        zpos[p] = 225
    for p in range(225,248):
        zpos[p] = 248

def vertikal(strip, height):
    color = Color(100, 100, 100)
    black = Color(0,0,0)
    
    for p in range(0,strip.numPixels()):
        if abs(zpos[p] - height) < 10:
            strip.setPixelColor(p, color)
        else:
            strip.setPixelColor(p, black)
    
    strip.show()
        
    
# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

# print edited pixel coordinates to file for later import
def printarray():
    filehandle = open("position1.py", "w")

    # now store the x position
    filehandle.write("xpos = [ ")
    x=0
    for i1 in range(15):
        for i2 in range(16):
            filehandle.write(str(xpos[x]))
            filehandle.write(", ")
            x=x+1

        filehandle.write("\n    ")
        
    for i2 in range(8):
        filehandle.write(str(xpos[x]))
        filehandle.write(", ")
        x=x+1

    filehandle.write(str(xpos[x]))
    filehandle.write("]\n\n")

    # and now the y position
    filehandle.write("ypos = [ ")
    x=0
    for i1 in range(15):
        for i2 in range(16):
            filehandle.write(str(ypos[x]))
            filehandle.write(", ")
            x=x+1

        filehandle.write("\n    ")
        
    for i2 in range(8):
        filehandle.write(str(ypos[x]))
        filehandle.write(", ")
        x=x+1

    filehandle.write(str(ypos[x]))
    filehandle.write("]\n\n")

    # and lastely the z position
    filehandle.write("zpos = [ ")
    x=0
    for i1 in range(15):
        for i2 in range(16):
            filehandle.write(str(zpos[x]))
            filehandle.write(", ")
            x=x+1

        filehandle.write("\n    ")
        
    for i2 in range(8):
        filehandle.write(str(zpos[x]))
        filehandle.write(", ")
        x=x+1

    filehandle.write(str(zpos[x]))
    filehandle.write("]\n\n")
        
    filehandle.close()

    # open the file and display what we have written
    filehandle = open("position1.py","r")
    
    print(filehandle.read())
    
    filehandle.close()
    

def xaxis(strip):
    for x in range(100):
        for p in range(LED_COUNT):
            if abs(xpos[p] - x) < 4:
                strip.setPixelColor(p, Color(100,100,100))
            else:
                strip.setPixelColor(p, Color(50,0,0))
        strip.show()

def yaxis(strip):
    for x in range(100):
        for p in range(LED_COUNT):
            if abs(ypos[p] - x) < 4:
                strip.setPixelColor(p, Color(100,100,100))
            else:
                strip.setPixelColor(p, Color(0,50,0))
        strip.show()
        
        
def zaxis(strip):
    for x in range(200):
        for p in range(LED_COUNT):
            if abs(zpos[p] - x) < 4:
                strip.setPixelColor(p, Color(100,100,100))
            else:
                strip.setPixelColor(p, Color(0,0,50))
        strip.show()

def showplane(strip,x,y,z):
    thickness = 4
    for p in range(LED_COUNT):
        if abs(xpos[p] - x) < thickness:
            xcolor = 100
        else:
            xcolor = 0
        if abs(ypos[p] - y) < thickness:
            ycolor = 100
        else:
            ycolor = 0
        if abs(zpos[p] - z) < thickness:
            zcolor = 100
        else:
            zcolor = 0
    
        strip.setPixelColor(p, Color(xcolor, ycolor, zcolor))
    
    strip.show()
    

# this is the main function for
# editing coordinates 
def editCoord(strip):
    xplane = 0
    yplane = 0
    zplane = 0
    plane = 0
    z = 0
    oldz = 0
    # clear the strip
    pixelblack(strip)
    
    try:

        while True:
            # for z in range(0,256):
            # light current pixel
            
            print("Pixel = " + str(z) + ": xpos = " + str(xpos[z]) + ", ypos = " + str(ypos[z]) + ", zpos = " + str(zpos[z]))
            
            # this will show an crosshair in x,y,and z
            # useful for fine adjustment of pixel position
            if plane==1:
                showplane(strip,xplane,yplane,zplane)
            
            strip.setPixelColor(oldz, Color(0,0,0))
            strip.setPixelColor(z, Color(100,100,100))
            strip.show()
            
            oldz = z
            
            #vertikal(strip, z)
            c = read_single_keypress()
            
            #print ("key = " + ''.join(c))
            
            
            t = ord(c[0])
            
            print (t)
            
            if c[0]=="+":
                z=z+1
                if z>248:
                    z=0
            if c[0]=="-":
                z=z-1
                if z<0:
                    z=248
            # change z axel value
            if c[0]=="a":
                zpos[z]=zpos[z]+1
                if zpos[z]>255:
                    zpos[z]=255
            if c[0]=="z":
                zpos[z]=zpos[z]-1
                if zpos[z]<0:
                    zpos[z]=0
            
            # change x axel value
            if c[0]=="s":
                xpos[z]=xpos[z]+1
                if xpos[z]>255:
                    xpos[z]=255
            if c[0]=="x":
                xpos[z]=xpos[z]-1
                if xpos[z]<0:
                    xpos[z]=0
            
            # change z axel value
            if c[0]=="y":
                ypos[z]=ypos[z]+1
                if ypos[z]>255:
                    ypos[z]=255
            if c[0]=="h":
                ypos[z]=ypos[z]-1
                if ypos[z]<0:
                    ypos[z]=0
            
            if c[0]=="c":
                print ("copy")
                if z>0:
                    xpos[z]=xpos[z-1]
                    ypos[z]=ypos[z-1]
                    zpos[z]=zpos[z-1]
            
            # ESC
            if ord(c[0])==27:
                print("Save to file position1.py")
                printarray()

            if c[0]=="u":
                xplane = xplane + 1
            if c[0]=="j":
                xplane = xplane - 1
                if xplane < 0:
                    xplane = 0

            if c[0]=="i":
                yplane = yplane + 1
            if c[0]=="k":
                yplane = yplane - 1
                if yplane < 0:
                    yplane = 0

            if c[0]=="o":
                zplane = zplane + 1
            if c[0]=="l":
                zplane = zplane - 1
                if zplane < 0:
                    zplane = 0

            if c[0]=="p":
                if plane == 0:
                    plane = 1
                else:
                    plane = 0

                
            # Ctrl-C
            if ord(c[0])==3:
                pixelblack(strip)
                break
                    
            if c[0]=="q":
                pixelblack(strip)
                break

   
            
            # print ('Color wipe animations.')
            # colorWipe(strip, Color(255, 0, 0))  # Red wipe
            # colorWipe(strip, Color(0, 255, 0))  # Blue wipe
            # colorWipe(strip, Color(0, 0, 255))  # Green wipe
            # print ('Theater chase animations.')
            # theaterChase(strip, Color(127, 127, 127))  # White theater chase
            # theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            # theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            # print ('Rainbow animations.')
            # rainbow(strip)
            # rainbowCycle(strip)
            # theaterChaseRainbow(strip)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
    
# Main program logic follows:

    
def printPolar():
    r1 = LED_COUNT // 16
    r2 = LED_COUNT - r1*16
    print (r1)
    print(r2)
    #exit(0)
    sys.stdout.write("r = [ ")
    for i1 in range(r1):
        for i2 in range(16):
            p = i1*16 + i2
            sys.stdout.write(str(r[p]))
            sys.stdout.write(", ")
        print("")

    for i2 in range(r2-1):
        p = r1*16 + i2
        sys.stdout.write(str(r[p]))
        sys.stdout.write(", ")

    p = LED_COUNT - 1
    sys.stdout.write(str(r[p]))
    print(" ]")
    print("")
    
    sys.stdout.write("theta = [ ")
    for i1 in range(r1):
        for i2 in range(16):
            p = i1*16 + i2
            sys.stdout.write(str(theta[p]))
            sys.stdout.write(", ")
        print("")

    for i2 in range(r2-1):
        p = r1*16 + i2
        sys.stdout.write(str(theta[p]))
        sys.stdout.write(", ")

    p = LED_COUNT - 1
    sys.stdout.write(str(theta[p]))
    print(" ]")
    print("")

def degDist(d1,d2):
    
    d3 = d1-d2
    if d3 < 0:
        d3 += 360
    return d3
    
def fade(strip):
    c = 0
    r = 0
    g = 0
    b = 0
    #return (white << 24) | (red << 16)| (green << 8) | blue
    for p in range (LED_COUNT):
        c = strip.getPixelColor(p)
        r = abs(((c >> 16) & 255) - 1)
        g = abs(((c >> 8) & 255) - 1)
        b = abs((c & 255) - 1)
        strip.setPixelColor(p, Color(r, g, b))

def spiral(strip, light):
    #light = Color(100,100, 100)
    
    for alfa in range(360):
        for p in range(LED_COUNT):
            if degDist(alfa, theta[p]) < 2:
                strip.setPixelColor(p, light)
        if (alfa%3) == 0:
            fade(strip)
        strip.show()

def ddist(p, i):
    dx = abs(xpos[p] - xpos[i])
    dy = abs(ypos[p] - ypos[i])
    dz = abs(zpos[p] - zpos[i])
    return int(sqrt(dx**2 + dy**2 + dz**2))
 
        
def randNova(strip):    
    pixelblack(strip)

    
    p = randint(0,248)
    nova(strip, p)
        
def nova(strip, p):
    pp = [256] * 249
    
    for i in range(249):
        pp[i] = ddist(p,i)
        
    strip.setPixelColor(p, Color(250,250,250))
    strip.show()
    
    for i in range(100):
        for p1 in range(249):
            if (i - pp[p1]) == 0:
                b=99 - i
                strip.setPixelColor(p1, Color(b,50,50))
        fade(strip)
        fade(strip)

        strip.show()
        
    for i in range(0,100):
        fade(strip)
        strip.show()

def findCloserPixel(p, target):
    delta = [300] * 249
    index = 0
    closest = target
    
    # first find all closer pixels
    for i in range(249):
        if ddist(p, target) > ddist(i, target):
            delta[index] = i
            index += 1
    print("i=" + str( index))
    # cannot find a closer pixel, p is the closest, return the target
    if index == 0:
        return target
        
    # now find the closest to current pixel p
    for i in range(index):
        if ddist(delta[i], p) < ddist(closest, p):
            closest = delta[i]
    
    return closest
            
def walk(strip):
    print("walk")
    
    p = randint(0,248)
    t = randint(0,248)
    
    strip.setPixelColor(p, Color(0,50,50))
    strip.setPixelColor(t, Color(100,100,100))
    strip.show()
    time.sleep(800/1000.0)
    
    
    while True:
        print("P=" + str(p) + ", t=" + str(t))
        if p == t:
            time.sleep(1)
            nova(strip,p)
            break
        p = findCloserPixel(p,t)
        strip.setPixelColor(p, Color(50,50,0))
        strip.show()
        time.sleep(150/1000.0)
        
def testBrightness(strip):
    
    strip.setBrightness(255)

    for p in range(249):
        #strip.setBrightness(p*20)
        strip.setPixelColor(p, Color(0,0,p))
    strip.show()
    time.sleep(3)
    
    for i in range(256):
        strip.setBrightness(255 - i)
        #fade(strip)
        strip.show()
        time.sleep(20/1000.0)
    
    
def main(strip):


    # initiate polar coordinates from cartesian
    cart2pol()
    
    while True:
        #randNova(strip)
        #walk(strip)
        testBrightness(strip)

#    while True:
#        spiral(strip, Color(100,0,0))
#        spiral(strip, Color(0,100,0))
#        spiral(strip, Color(0,0,100))

    
    #setXYZ()

    #printarray()
    #exit(0)
    #editCoord(strip)




if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_TYPE)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    
    try:
        main(strip)
    except KeyboardInterrupt:
        pixelblack(strip)
        strip.show()


