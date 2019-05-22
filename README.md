# mprender
python based multiprocessing renderer

usage:
from PIL import Image
import mpimage

imagevariable=mpimage.mprenderbyfunc(width,height,rgbfunction,procs=procnumber,perprocsplit=furthersplit)

rgbfunction is a function you define taking 2 variables for x,y and returning (r,g,b).
procnumber is the number of processes that will run
The number of jobs created = procnumber*furthersplit. This is useful for when functions take longer for specific values of x,y.

e.g.
mpimage.mprenderbyfunc(800,600,simpfunc,procs=2,perprocsplit=4).save("functest.png")

see textfunc.py as an example
