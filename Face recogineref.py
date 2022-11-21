import numpy as np
import pymysql
import face_recognition
import cv2
import os
from datetime import datetime
path='data'
images=[]
classNames =[]
myList=os.listdir(path)
#print(myList)
for cl in myList:
 curImg=cv2.imread(f'{path}/{cl}')
 images.append(curImg)
 classNames.append(os.path.splitext(cl)[0])
#print(classNames)
def findEncodings(images):
 encodeList=[]
 for img in images:
 img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
 encode=face_recognition.face_encodings(img)[0]
 encodeList.append(encode)
 return encodeList
def markAttendence(name):

 conn=pymysql.connect(
 host='localhost',
 user='root',
 password='@Sai553@',
 db='db',
CMRTC 14
 )
 cur=conn.cursor()
 now=datetime.now()
 checkUsername = cur.execute('SELECT name FROM attendence WHERE name=%s',name)
 if checkUsername == 0:
 cur.execute("insert into attendence(name,entry) values(%s,%s)",(name,now))
 else:
 cur.execute('update attendence set entry=%s where name=%s',(now,name))
 conn.commit()
 #for r in cur:
 # print(r)
 '''with open('attendence1.csv','r+') as f:
 myDataList=f.readlines()
 nameList=[]
 for line in myDataList:
 entry=line.split(',')
 nameList.append(entry[0])
 if name not in nameList:
 now=datetime.now()
 dtstring=now.strftime('%H:%M:%S')

 f.writelines(f'\n{name},{dtstring}')
 '''

encodeListKnown = findEncodings(images)
#print("its working on it")
cap=cv2.VideoCapture(0)
while True:
 success,img=cap.read()
 #print("jgjjhg")
 imgS=cv2.resize(img,(0,0),None,0.25,0.25)
 imgS=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
 facesCurrFrame=face_recognition.face_locations(imgS)
 encodesCurrFrames=face_recognition.face_encodings(imgS,facesCurrFrame)
CMRTC 15
 #print(encodesCurrFrames)
 for encodeFaces,faceLoc in zip(encodesCurrFrames,facesCurrFrame):
 matches=face_recognition.compare_faces(encodeListKnown,encodeFaces)
 #print(matches)
 faceDis=face_recognition.face_distance(encodeListKnown,encodeFaces)
 #print(faceDis)
 matchIndex=-1;
 '''if faceDis.any() < 0.80000000:
 matchIndex=np.argmin(faceDis)
 print(faceDis)'''
 for val in faceDis:
 if val < 0.4000000:
 matchIndex=np.argmin(faceDis)
 #print(faceDis)
 break

 #print(matchIndex)
 if matchIndex!=-1 and matches[matchIndex]:
 name=classNames[matchIndex].upper()
 #(faceDis)
 y1,x2,y2,x1=faceLoc
 cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
 cv2.rectangle(img,(x1,y2-10),(x2,y2),(0,255,0),cv2.FILLED)
 cv2.putText(img,name,(x1+6,y2-
6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
 #print('gggggg')
 markAttendence(name)
 else:
 name='Not Found'
 #print(faceDis)
 y1,x2,y2,x1=faceLoc
 cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
 cv2.rectangle(img,(x1,y2-10),(x2,y2),(0,255,0),cv2.FILLED)
CMRTC 16
 cv2.putText(img,name,(x1+6,y2-
6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
 cv2.imshow('webcam',img)
 cv2.waitKey(1)