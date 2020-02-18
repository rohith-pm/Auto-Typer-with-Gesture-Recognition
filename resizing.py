from PIL import Image
import numpy as np
def resize(imageName):
    basewidth = 100
    img = Image.open(imageName)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(imageName)
	img=np.array(img)
	print(img.shape)
	
for i in range(1,101):
	resize("three"+str(i)+".png")