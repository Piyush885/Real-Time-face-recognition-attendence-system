# from lib2to3.pytree import WildcardPattern
# import cv2
# import numpy as np
# import face_recognition
# import os

# path = 'Training_images'

# images = [] # used to store all images from Training_images folder
# classNames = [] # Used to store only names. like if elon.jpg then it will store elon only
# mylist = os.listdir(path) # list all folders images from given path
# for cl in mylist:
#     curImag = cv2.imread(f'{path}/{cl}')
#     images.append(curImag)
#     classNames.append(os.path.splitext(cl)[0])
# print(classNames)  

# # In this section we will find the encodings of all images.
# def findencodings(images):
#     encodinglist=[]
#     for img in images:
#         img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encodinglist.append(encode)
#     return encodinglist
# encodingListKnown = findencodings(images)

# # Now opening webcam to take test images
# cap = cv2.VideoCapture(0)
# # To get each frame one by one we use while loop
# while True:
#     sucess , img = cap.read() # this will give our image
#     # for real time working we will reduce the size of image this will speed the process.
#     imgS = cv2.resize(img,(0,0),None,0.25,0.25)
#     # converting bgr to rgb
#     imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    
#     # finding face location and face encodings
#     faceLoc = face_recognition.face_locations(imgS)
#     encode = face_recognition.face_encodings(imgS,faceLoc)
    
#     for encoding, faceloc in zip(faceLoc,encode):
#         matches = face_recognition.compare_faces(encodingListKnown,encoding)
#         face_Dis = face_recognition.face_distance(encodingListKnown,encoding)
#         print(face_Dis)
import cv2
import numpy as np
import face_recognition
import os
import time
from datetime import datetime

# from PIL import ImageGrab

path = 'Training_images'
images = []
classNames = []
myList = os.listdir(path)
# print(myList)
print("Running Please wait!!!!")
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
# print(classNames)


def findEncodings(images):
    encodeList = []


    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

nameList = []
def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()


        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime("%d/%m/%Y %H:%M:%S")
                f.writelines(f'\n{name},{dtString}')
                

#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr

encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
# img = captureScreen()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
# print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
# print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
            # print(f'{name} your attendence has been taken please move out of camera!!!!!')
            

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)             