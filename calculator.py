import pandas
import math
from IPython.display import display
from PIL import Image
import os
from  scipy.stats import linregress

def bw(img):
    gray = img.convert('L')
    return gray.point(lambda x: 0 if x<128 else 1, '1')

def interesting(image):
    #true if any data is 0, i.e. black
    return 0 in set(image.getdata())

def interesting_box_count(image, length):
    width,height=image.size
    
    interesting_count=0
    box_count=0
    for x in range(int(width/length)):
        for y in range(int(height/length)):
            C=(x*length,y*length,length*(x+1),length*(y+1))

            chopped = image.crop(C)
            box_count+=1
            if (interesting(chopped)):
                interesting_count+=1        
      
    assert box_count
    assert interesting_count
    return interesting_count

def getcounts(image):
    length=min(image.size)
    while(length>5):
        interesting = interesting_box_count(image,length)
        yield math.log(1.0/length), math.log(interesting)
        length=int(length/2)
        
def counts(image):
    return pandas.DataFrame(getcounts(image),columns=["x","y"])

def dimension(image):
    frame=counts(image)
    return linregress(frame.x,frame.y)

def analyse(image):
    c=counts(image)
    print("Fractal Dimension:",linregress(c.x,c.y).slope)
