import numpy as np
from PIL import Image
def resize(imageName):
    basewidth = 100
    img = Image.open(imageName)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(imageName)
    img=np.array(img)
    
	
	
for i in range(1,1001):
	resize("three"+str(i)+".png")