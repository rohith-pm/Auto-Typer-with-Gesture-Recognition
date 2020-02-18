import cv2

cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)

f=0
n=0
while True:
	rep,frame=cap.read()
	frame=cv2.flip(frame, 1)
	frame1=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	img=cv2.GaussianBlur(frame1,(5,5),0)
	roi2 = img[10:400,250:630]
	cv2.rectangle(frame,(630,10),(250,400),(255,0,0),2)
	
	cv2.imshow('f',frame)
	k=cv2.waitKey(30)
	
	if(k==ord('q')):
		break
	elif(f==0 and k==ord('s')):
		cv2.imwrite('take'+str(0)+'.png',roi2)
		n+=1
		f=1
		roi1=roi2
		print(roi1)
		print("taken")
	elif(f==1 and k==ord('s')):
		diff=cv2.absdiff(roi1, roi2)
		_,thresh1=cv2.threshold(diff,25,255,cv2.THRESH_BINARY)
		(cnts, _) = cv2.findContours(thresh1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		print(len(cnts))
		cv2.imshow('f1',thresh1)
		
		cv2.imwrite('nine'+str(n)+'.png',thresh1)
		n+=1
		print("taken")
		
cap.release()
