#!/usr/bin/env python3
from PIL import Image
import mpimage
import math

def juliafunc(ix,iy):
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


def mandelfunc(ix,iy):
    zoom=78225
    xoff=-0.78940
    yoff=-0.163055
    tx=xoff+ix/(zoom*200)
    ty=yoff+iy/(zoom*200)
    xtmp=ytmp=xtmp2=iters=0
    maxiters=10000
    while ((iters<maxiters) and (xtmp*xtmp+ytmp*ytmp < 4)):
        xtmp2=xtmp*xtmp-ytmp*ytmp+tx
        ytmp=2*xtmp*ytmp+ty
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




mpimage.mprenderbyfunc(800,600,juliafunc,xoffset=-400,yoffset=-300,procs=2,perprocsplit=4).save("functest.png")
#mpimage.mprenderbyfunc(800,600,mandelfunc,xoffset=-400,yoffset=-300,procs=2,perprocsplit=4).save("functest.png")
