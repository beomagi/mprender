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
    return(int(vr),int(vg),int(vb))



def renderimg(width, height, offx, offy, rgbfunction,aqueue):
    print("starting subrender..."+str((width, height, offx, offy, rgbfunction)))
    img = Image.new('RGB', (width, height), color = (0, 0, 0))
    pimg = img.load()
    for yy in range(height):
        for xx in range(width):
            pimg[xx,yy]=rgbfunction(xx+offx,yy+offy)
    print("finished subrender..."+str((width, height, offx, offy, rgbfunction)))
    aqueue.put(img)
    return img

def mprenderbyfunc(mainwide, mainhigh, colorfunction,xoffset=0,yoffset=0,procs=2):
    mainimg = Image.new('RGB', (mainwide, mainhigh), color = (255, 0, 255))

    queuelist=[]
    processlist=[]

    splitx=1;
    splity=procs;
    for spx in range(splitx):
        for spy in range(splity):
            suboffx=round((mainwide*spx)/splitx)
            suboffy=round((mainhigh*spy)/splity)
            suboffxplus1=round((mainwide*(spx+1))/splitx)
            suboffyplus1=round((mainhigh*(spy+1))/splity)
            subwide=suboffxplus1-suboffx
            subhigh=suboffyplus1-suboffy
            childq=smp.Queue()
            iprocess=smp.Process(target=renderimg,args=(subwide,subhigh,suboffx+xoffset,suboffy+yoffset,colorfunction,childq,))
            queuelist.append((suboffx, suboffy, childq))
            processlist.append(iprocess)
    a=0
    for eachprocess in processlist:
        a+=1
        print("starting process "+str(a))
        eachprocess.start()
    
    complete=0
    while complete==0:
        complete=1
        for  prcs in processlist:
            if (prcs.is_alive==True):
                prcs.join(timeout=0)
                print("process "+str(prcs.pid)+"  "+str(prcs.is_alive()))
                complete=0
        time.sleep(0.01)
    
    for eachq in queuelist:
        sx,sy,cldq=eachq
        subimage=cldq.get()
        mainimg.paste(subimage,(sx,sy))

    return mainimg

def main():
    mprenderbyfunc(600,600,colorfunc2).save("./test.png")

if __name__=="__main__":
    main()
