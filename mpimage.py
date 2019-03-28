#!/usr/bin/env python3
from PIL import Image
import multiprocessing as smp
import sys
import math
import time


def colorfunc3(ix,iy):
    zoom=1
    xoff=0
    yoff=0
    tx=xoff+ix/(zoom*200)
    ty=yoff+iy/(zoom*200)
    xtmp2=iters=0
    xtmp=tx
    ytmp=ty
    maxiters=1000
    while ((iters<maxiters) and (xtmp*xtmp+ytmp*ytmp < 4)):
        xtmp2=xtmp*xtmp-ytmp*ytmp-0.32
        ytmp=2*xtmp*ytmp+0.6575
        xtmp=xtmp2
        iters+=1;
    log2=math.log(2)
    if (iters<maxiters): #smoother transitions
        zn=math.sqrt(xtmp*xtmp+ytmp*ytmp)
        zl=math.log(math.log(zn)/log2)/log2
        iters+=1-zl
    if iters==maxiters: #inerbulb shading
        dlg=xtmp*xtmp+ytmp*ytmp
        if dlg>0:
            iters=math.log((1/(xtmp*xtmp+ytmp*ytmp)))/(log2);
    cycle=(maxiters)/(3.14159265359*100);
    cr=128+127*math.sin(0.00+iters/(cycle*1.5000))
    cg=128+127*math.sin(1.57+iters/(cycle*1.6000))
    cb=128+127*math.sin(3.14+iters/(cycle*1.5666))
    return(int(cr),int(cg),int(cb))




#def renderimg(width, height, offx, offy, rgbfunction):
def renderimg(params):
    width, height, offx, offy, rgbfunction = params
    print("starting subrender..."+str((width, height, offx, offy, rgbfunction.__name__)))
    inittime=time.time()
    img = Image.new('RGB', (width, height), color = (0, 0, 0))
    pimg = img.load()
    for yy in range(height):
        for xx in range(width):
            pimg[xx,yy]=rgbfunction(float(xx+offx),float(yy+offy))
    endtime=time.time()
    print("finished subrender..."+str((width, height, offx, offy, rgbfunction.__name__))+"  "+str(endtime-inittime)+"s")
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
            processargs.append((int(subwide),int(subhigh),int(suboffx+xoffset),int(suboffy+yoffset),colorfunction))
    renderpool=smp.Pool(procs)
    imgreturn=renderpool.map(renderimg,processargs)

    for eachentry in imgreturn:
        sx,sy,img=eachentry
        mainimg.paste(img,(sx-xoffset,sy-yoffset))

    return mainimg

def main():
    proccount=2
    procsplit=5
    if "-p" in sys.argv:
        proccount=int(sys.argv[sys.argv.index("-p")+1])
    if "-s" in sys.argv:
        procsplit=int(sys.argv[sys.argv.index("-s")+1])
    mprenderbyfunc(800,600,colorfunc3,xoffset=-400,yoffset=-300,procs=proccount,perprocsplit=procsplit).save("./test.png")

if __name__ == '__main__':
    main()
