#!/usr/bin/env python3
from PIL import Image
import multiprocessing as smp
import sys
import math
import time


def colorfunc1(ix,iy):
    r=127+128*math.sin(ix*(math.pi/180))
    g=127+128*math.sin(iy*(math.pi/180))
    b=127+128*math.sin((ix+iy)*(math.pi/180))
    return (int(r),int(g),int(b))

def colorfunc2(ix,iy):
    rx,ry=(30,30)
    gx,gy=(60,30)
    bx,by=(45,53)
    mx=ix%90
    my=iy%90
    dr=0.1+math.sqrt((rx-mx)*(rx-mx)+(ry-my)*(ry-my))
    dg=0.1+math.sqrt((gx-mx)*(gx-mx)+(gy-my)*(gy-my))
    db=0.1+math.sqrt((bx-mx)*(bx-mx)+(by-my)*(by-my))
    
    vr=255
    vg=1/dg*dr*255
    vb=1/db*dr*255
    if vg > 255:
        vr=(255/vg)*vr
        vb=(255/vg)*vb
        vg=255
    if vb > 255:
        vr=(255/vb)*vr
        vg=(255/vb)*vg
        vb=255
    mul=(1+4050)/(1+((mx-45)*(mx-45)+(my-45)*(my-45)))
    vr=(mul*dr)
    vg=(mul*dg)
    vb=(mul*db)

    return(int(vr),int(vg),int(vb))



#def renderimg(width, height, offx, offy, rgbfunction):
def renderimg(params):
    width, height, offx, offy, rgbfunction = params
    print("starting subrender..."+str((width, height, offx, offy, rgbfunction.__name__)))
    img = Image.new('RGB', (width, height), color = (0, 0, 0))
    pimg = img.load()
    for yy in range(height):
        for xx in range(width):
            pimg[xx,yy]=rgbfunction(xx+offx,yy+offy)
    print("finished subrender..."+str((width, height, offx, offy, rgbfunction.__name__)))
    return((offx,offy,img))

def mprenderbyfunc(mainwide, mainhigh, colorfunction,xoffset=0,yoffset=0,procs=2,perprocsplit=10):
    """
    create an image, dimensions mainwide x mainhigh
    colorfunction takes values x,y and returns r,g,b
    xoffset,yoffset are added to x,y coordinates in the image to align the function
    procs is the number of processes that will be loaded (default 2)
    perprocsplit is used to divide the image more. Different x,y can have different loads
      by splitting the image further we are less likely to stick one core with a lot of
      processing and another with little to do.
    """
    mainimg = Image.new('RGB', (mainwide, mainhigh), color = (255, 0, 255))

    processargs=[]
    splitx=1;
    splity=procs*perprocsplit;
    for spx in range(splitx):
        for spy in range(splity):
            suboffx=round((mainwide*spx)/splitx)
            suboffy=round((mainhigh*spy)/splity)
            suboffxplus1=round((mainwide*(spx+1))/splitx)
            suboffyplus1=round((mainhigh*(spy+1))/splity)
            subwide=suboffxplus1-suboffx
            subhigh=suboffyplus1-suboffy
            childq=smp.SimpleQueue()
            processargs.append((subwide,subhigh,suboffx+xoffset,suboffy+yoffset,colorfunction))
    renderpool=smp.Pool(procs)
    imgreturn=renderpool.map(renderimg,processargs)

    for eachentry in imgreturn:
        sx,sy,img=eachentry
        mainimg.paste(img,(sx-xoffset,sy-yoffset))

    return mainimg

def main():
    proccount=2
    procsplit=2
    if "-p" in sys.argv:
        proccount=int(sys.argv[sys.argv.index("-p")+1])
    if "-s" in sys.argv:
        procsplit=int(sys.argv[sys.argv.index("-s")+1])
    mprenderbyfunc(600,600,colorfunc2,procs=proccount,perprocsplit=procsplit).save("./test.png")

if __name__ == '__main__':
    main()
