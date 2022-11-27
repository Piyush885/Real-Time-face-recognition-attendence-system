from django.shortcuts import render
import pyttsx3
converter = pyttsx3.init()
converter.setProperty('volume', 0.7)
# Create your views here.
from urllib import request
from django.http import HttpResponse
from django.shortcuts import render,HttpResponse,redirect
from .models import Register,Manager
import cv2
import numpy as np
import face_recognition
import os
import time
from datetime import datetime
encodeList = []
nameList = []
# Create your views here.
def login(request):
    return render(request,"login.html")
def validate(request):
    if request.method == 'POST':
        password = request.POST.get("password")
        print(password)
        a = Manager.objects.all()
        for i in a:
            print("orignal password is ",i.password)
            if i.password == password:
                return render(request,"index.html")
        return redirect("/",{"message":"Wrong password"})   
                
# def index(request):
#     return render(request,"index.html")
def start(request):
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
        # encodeList = []


        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    
    def markAttendance(name):
        # code for save in database---
        
        
        
        # code for saving to csv file
        with open('Attendance.csv', 'r+') as f:
            myDataList = f.readlines()


            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
                if name not in nameList:
                    now = datetime.now()
                    dtString = now.strftime("%d/%m/%Y %H:%M:%S")
                    f.writelines(f'\n{name},{dtString}')
                    studentno = name[0:7]
                    name1  = name[7:]
                    name1 = name1.replace('_','')
                    register = Register(name = name1 ,studentno = studentno,time =str(dtString))
                    register.save()
                    converter.say(f"{name} Your Attendence has been taken")
                    converter.runAndWait()

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
    return HttpResponse("working!!")
def stop(request):
    return redirect("/")
def showdata(request):
    data = Register.objects.all()
    return render(request,"data.html",{"message" :data})