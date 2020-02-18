import tensorflow as tf
import tflearn
from tflearn.layers.conv import conv_2d,max_pool_2d
from tflearn.layers.core import input_data,dropout,fully_connected
from tflearn.layers.estimator import regression
import numpy as np
from PIL import Image
import cv2
import imutils
from playsound import playsound

#model
tf.reset_default_graph()
convnet=input_data(shape=[None,170,60,1],name='input')

convnet=conv_2d(convnet,32,2,activation='relu')
convnet=max_pool_2d(convnet,2)

convnet=conv_2d(convnet,64,2,activation='relu')
convnet=max_pool_2d(convnet,2)

convnet=conv_2d(convnet,128,2,activation='relu')
convnet=max_pool_2d(convnet,2)

convnet=conv_2d(convnet,256,2,activation='relu')
convnet=max_pool_2d(convnet,2)

convnet=conv_2d(convnet,256,2,activation='relu')
convnet=max_pool_2d(convnet,2)

convnet=conv_2d(convnet,128,2,activation='relu')
convnet=max_pool_2d(convnet,2)

convnet=conv_2d(convnet,64,2,activation='relu')
convnet=max_pool_2d(convnet,2)

convnet=fully_connected(convnet,600,activation='relu')

convnet=dropout(convnet,0.75)
convnet=fully_connected(convnet,12,activation='softmax')

convnet=regression(convnet,optimizer='adam',learning_rate=0.001,loss='categorical_crossentropy',name='regression')

model=tflearn.DNN(convnet,tensorboard_verbose=0)
model.load("Trainer/RohModel.tfl")	


#resizing
def resize(imageName):
    basewidth = 100
    img = Image.open(imageName)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(imageName)
	
#capture and predict
cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
plane_image=False
avg={} #calculate the mode of predicted class
double_digit=False
digits=0 #no of digits persent in double_digit number
while True:
	_,frame=cap.read()
	frame=cv2.flip(frame, 1)
	frame1=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	img=cv2.GaussianBlur(frame1,(5,5),0)
	roi2 = img[10:400,250:630]
	cv2.rectangle(frame,(630,10),(250,400),(255,0,0),2)
	
	cv2.imshow('f',frame)
	k=cv2.waitKey(30)
	
	
	if(k==ord('q')): #to quit
		break
	elif(plane_image==False and k==ord('s')): #to capture plane_image
		cv2.imwrite('take'+str(0)+'.png',roi2)
		plane_image=True
		roi1=roi2
	elif(plane_image==True):
		diff=cv2.absdiff(roi1, roi2)
		_,thresh1=cv2.threshold(diff,25,255,cv2.THRESH_BINARY)
		fingers, _ = cv2.findContours(thresh1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		cv2.imshow('f1',thresh1)
		#print("length fingers=",len(fingers),avg)
		if(len(fingers)>0):
			type=False
			
			cv2.imwrite('temp.png',thresh1)
			resize('temp.png')
			
			image = cv2.imread('temp.png')
			gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			prediction = model.predict([gray_image.reshape(170, 60, 1)])
			PredictedClass,confidence=np.argmax(prediction), (np.amax(prediction) / (prediction[0][0] + prediction[0][1] + prediction[0][2]))
			#print(int(PredictedClass)+1,confidence*100)
			
			if(int(PredictedClass) in avg.keys()):
				avg[int(PredictedClass)]+=1
			else:
				avg[int(PredictedClass)]=1
				
		
		elif(len(avg)!=0):
			
			maxi=-99999
			for i in avg.keys():
				if(avg[i]>maxi):
					ind=i
					maxi=avg[i]
			
			if(double_digit==True and (ind==10 or ind==11)):
				double_digit=False
				digits=0
				playsound("beep_sound.wav")
			elif(ind==10):
				print(" ",end="")
			elif(ind==11):
				double_digit=True
			elif(double_digit==True and digits==0):
				if(ind<=2):
					number=str(ind)
					digits+=1
				else:
					double_digit=False
					digits=0
					playsound("beep_sound.wav")
			elif(double_digit==True and digits==1):
				number+=str(ind)
				ind=int(number)
				double_digit=False
				digits=0
				if(ind<=26):
					print(chr(64+ind),end="")
				else:
					playsound("beep_sound.wav")
			else:
				print(chr(64+ind),end="")
				
			avg={}
	
cap.release()

