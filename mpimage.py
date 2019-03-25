#!/usr/bin/python3
from PIL import Image
from multiprocessing import Pool
import sys
import math

PARALLEL=10

def colorfunc1(ix,iy):
    r=127+128*math.sin(ix*(math.pi/180))
    g=127+128*math.sin(iy*(math.pi/180))
    b=127+128*math.sin((ix+iy)*(math.pi/180))
    return (int(r),int(g),int(b))

def renderimg(width, height, offx, offy, rgbfunction):
    img = Image.new('RGB', (width, height), color = (0, 0, 0))
    pimg = img.load()
    for yy in range(height):
        for xx in range(width):
            pimg[xx,yy]=rgbfunction(xx+offx,yy+offy)
    return img

def mprenderbyfunc(mainwide, mainhigh, colorfunction,xoffset=0,yoffset=0):
    mainimg = Image.new('RGB', (mainwide, mainhigh), color = (255, 0, 255))

    splitx=1;
    splity=10;
    for spx in range(splitx):
        for spy in range(splity):
            suboffx=round((mainwide*spx)/splitx)
            suboffy=round((mainhigh*spy)/splity)
            suboffxplus1=round((mainwide*(spx+1))/splitx)
            suboffyplus1=round((mainhigh*(spy+1))/splity)
            subwide=suboffxplus1-suboffx
            subhigh=suboffyplus1-suboffy 
            subimage=renderimg(subwide,subhigh,suboffx+xoffset,suboffy+yoffset,colorfunction)
            mainimg.paste(subimage,(suboffx,suboffy))
    return mainimg

def main():
    mprenderbyfunc(600,600,colorfunc1).save("./test.png")

if __name__=="__main__":
    main()
