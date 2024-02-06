# VisionCoin app


import numpy as np
import cv2
import os
import datetime
import math

waitkey_time=1
url='http://192.168.1.234:4747/video' #DroidCam Ip camera address
matched=False
p=0
n=0
d=0
q=0
total=0
res1=None
res4=None


#sift keypoints and descriptors for five and ten rupees coins
sift=cv2.SIFT_create(contrastThreshold=0.01, edgeThreshold=100)

penny=cv2.imread("newfive8.png")
#cv2.imshow("penny", penny)
#cv2.waitKey(0)
penny=cv2.cvtColor(penny, cv2.COLOR_BGR2GRAY)
kp1, des1=sift.detectAndCompute(penny,None)

quarter=cv2.imread("ten8.png")
#cv2.imshow("quarter", quarter)
#cv2.waitKey(0)
quarter=cv2.cvtColor(quarter, cv2.COLOR_BGR2GRAY)
kp4, des4=sift.detectAndCompute(quarter,None)



#starting video capture from IP camera
cap = cv2.VideoCapture(url)
if not cap.isOpened():
        print("Cannot open IP camera /n Trying laptop camera...")
        #starting video capture from laptop webcam
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
                print("Cannot open laptop camera")
                exit()
        print("Using laptop camera") 



#looping over the video capture from webcam
while True:
        
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
 
        
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred=cv2.GaussianBlur(gray, (5,5), 2, 2)
        #canny=cv2.Canny(blurred, 180, 60)
        #cv2.imshow("canny", canny)
        #cv2.waitKey(waitkey_time)
        #finding coins on table as hough circles
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, 10,
                               param1=180, param2=60,
                               minRadius=70, maxRadius=90) #70, 90
        
        coin_dict={5:0, 10:0}        

        if circles is not None:
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                        center = (int(i[0]), int(i[1]))
                        radius=int(i[2])
                        cv2.circle(frame, center, radius, (255,0,0), 3)
                        #print("center: ", center)
                        #print("radius: ", radius)
                        if center[1]-radius>0 and center[1]+radius<frame.shape[1] and center[0]-radius>0 and center[0]+radius<frame.shape[0]:
                                crop=gray[max(center[1]-radius,0):min(center[1]+radius,frame.shape[0]), max(center[0]-radius,0):min(center[0]+radius,frame.shape[1])]
                                cropl=crop[:,:int(crop.shape[1]/2)]
                                cropu=crop[10:int(crop.shape[0]/3),:]
                                #print("frame shape: ",frame.shape)
                                #print("crop shape: ",crop.shape)
                        else: crop=None
                        if crop is not None:
                                kpl, desl=sift.detectAndCompute(cropl,None)
                                kpu, desu=sift.detectAndCompute(cropu,None)
                                if desl is not None and desl.shape[0]>1 and desu is not None and desu.shape[0]>1:
                                        FLANN_INDEX_KDTREE = 1
                                        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
                                        search_params = dict(checks=100)
                                        flann = cv2.FlannBasedMatcher(index_params,search_params)
                                        
                                        matches1 = flann.knnMatch(des1,desl,k=2)
                                        matchesMask1 = [[0,0] for i1 in range(len(matches1))]
                                        good_matches1=[]
                                        for j,(m,n1) in enumerate(matches1):
                                                if m.distance < 0.8*n1.distance:
                                                        matchesMask1[j]=[1,0]
                                                        good_matches1.append(m)
                                        draw_params = dict(matchColor = (0,255,0),
                                                        singlePointColor = (0,0,255),
                                                        matchesMask = matchesMask1,
                                                        flags = cv2.DrawMatchesFlags_DEFAULT)
                                        #res1 = cv2.drawMatchesKnn(penny,kp1,cropl,kpl,matches1,None,**draw_params)
                                        

                                        matches4 = flann.knnMatch(des4,desu,k=2)
                                        matchesMask4 = [[0,0] for i1 in range(len(matches4))]
                                        good_matches4=[]
                                        for j,(m,n1) in enumerate(matches4):
                                                if m.distance < 0.8*n1.distance:
                                                        matchesMask4[j]=[1,0]
                                                        good_matches4.append(m)
                                        draw_params = dict(matchColor = (0,255,0),
                                                        singlePointColor = (0,0,255),
                                                        matchesMask = matchesMask4,
                                                        flags = cv2.DrawMatchesFlags_DEFAULT)
                                        #res4 = cv2.drawMatchesKnn(quarter,kp4,cropu,kpu,matches4,None,**draw_params)
                                        
                                        if len(good_matches1)<len(good_matches4):
                                                coin_dict[10]+=1                    
                                        else: #len(good_matches4)<len(good_matches1):
                                                coin_dict[5]+=1
                                        #else: pass
        

        ten=coin_dict[10]
        five=coin_dict[5]
        total=(5*five)+(10*ten)

        cv2.putText(frame, 'Five: '+str(five), (10,30), 0, 0.6, (255,255,0), 2)
        cv2.putText(frame, 'Ten: '+str(ten), (10,50), 0, 0.6, (255,255,0), 2)
        cv2.putText(frame, 'Total value: '+str(total), (10,70), 0, 0.6, (255,255,0), 2)

       
        #app screen displaying video capture (displaying frame every 25ms)
        cv2.imshow('frame', frame)
        k=cv2.waitKey(waitkey_time)
        
        #if res1 is not None:
        #        cv2.imshow("penny", res1)
        #        k=cv2.waitKey(waitkey_time)

        #if res4 is not None:
        #        cv2.imshow("quarter", res4)
        #        k=cv2.waitKey(waitkey_time)


        #feature:  press "Esc" for closing app
        if k==27:
                cap.release()
                cv2.destroyAllWindows()


