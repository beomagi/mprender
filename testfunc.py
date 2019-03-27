from PIL import Image
import mpimage

def simpfunc(xv,yv):
    r=xv%255
    g=yv%255
    b=(xv*yv)%255
    return (int(r),int(g),int(b))

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



mpimage.mprenderbyfunc(800,600,simpfunc,procs=2,perprocsplit=4).save("functest.png")
