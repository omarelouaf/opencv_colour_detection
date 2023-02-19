import cv2
import numpy as np

framewidth = 360
frameheight = 360

cap = cv2.VideoCapture(0)
cap.set(3, framewidth)
cap.set(4, frameheight)
x1 = -0.5
x2 = -0.5

def empty(a):
    pass
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
cv2.createTrackbar("Threshold1", "Parameters", 150, 255, empty)
cv2.createTrackbar("Threshold2", "Parameters", 255, 255, empty)

def getContours1(img, imgContour1):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>2000:
            cv2.drawContours(imgContour1,contours,-1, (255,0,255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)

            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour1, (x,y), (x+w,y+h),(0, 255, 0), 5)

            cv2.putText(imgContour1, "Couleur bleu", (x, y-20), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 255, 0), 2)
            global x1
            # x1 = 0
            x1 = x
            # print('x1 = ', x1)
            return

def getContours2(img, imgContour2):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>2000:
            cv2.drawContours(imgContour2,contours,-1, (255,0,255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)

            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour2, (x,y), (x+w,y+h),(0, 255, 0), 5)

            cv2.putText(imgContour2, "Couleur rouge", (x, y-20), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 255, 0), 2)
            global x2
            # x2 = 0
            x2 = x
            # print('x2 = ', x2)
            return x2
while True:
    success, img = cap.read()

 #Détection de la couleur bleu
    h_min1 = 65
    h_max1 = 100
    s_min1 = 100
    s_max1 = 154
    v_min1 = 80
    v_max1 = 255
 #Détection de la couleur rouge
    h_min2 = 0
    h_max2 = 26
    s_min2 = 204
    s_max2 = 255
    v_min2 = 81
    v_max2 = 255

    lower1 = np.array([h_min1, s_min1, v_min1])
    upper1 = np.array([h_max1, s_max1, v_max1])

    lower2 = np.array([h_min2, s_min2, v_min2])
    upper2 = np.array([h_max2, s_max2, v_max2])

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(hsv, lower1, upper1)
    mask2 = cv2.inRange(hsv, lower2, upper2)

    result1 = cv2.bitwise_and(img, img, mask=mask1)
    result2 = cv2.bitwise_and(img, img, mask=mask2)

    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")

    imgCanny1 = cv2.Canny(result1, 1, 8)
    imgCanny2 = cv2.Canny(result2, 1, 8)

    kernel = np.ones((5,5))
    imgDil1 = cv2.dilate(imgCanny1, kernel, iterations=1)
    imgDil2 = cv2.dilate(imgCanny2, kernel, iterations=1)

    imgContour1 = img.copy()
    imgContour2 = img.copy()

    getContours2(imgDil2, imgContour2)
    getContours1(imgDil1, imgContour1)

    cv2.imshow('frame1', imgContour2)
    cv2.imshow('frame2', imgContour1)

    if x2 <= x1:
        x3 = 1
    else:
        x3 = 0
    A = [x1, x2, x3]
    print(A)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllwindows()

####################################################################################