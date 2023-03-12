import cv2
import numpy as np
#webcam access
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 100)

Colors=[#[66,100,0,123,255,255],#blue
        [107,128,72,179,255,255],]#red

myColorsValues=[#[255,51,51],
                [0,0,255]]
myPoints=[] #x,y,colorid
def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>500:
        #cv2.drawContours(imgResult, cnt, -1, (0, 255, 255), 3)
            peri=cv2.arcLength(cnt,True)
            points=cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h=cv2.boundingRect(points)
    return x+w//2,y #passing the top edge center



def findColor(img,Colors):
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    new_points=[]
    count=0
    for color in Colors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),2,myColorsValues[count],cv2.FILLED)# creating a circle there
        if x!=0 and y!=0:
            new_points.append([x,y,count])
        count+=1
    return new_points

def drawonCanvas(myPoints,myColorsValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 15, myColorsValues[point[2]], cv2.FILLED)



while True:
    success, img= cap.read()
    imgResult=img.copy()
    points=findColor(img,Colors)
    if len(points)!=0:
        for p in points:
            myPoints.append(p)
    if len(myPoints)!=0:
        drawonCanvas(myPoints,myColorsValues)

    cv2.imshow("Result",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break