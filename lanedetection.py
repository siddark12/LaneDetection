import cv2
import numpy as np
# import import_ipynb
import utlis1
 
curveList = []
avgVal=10
 
def getLaneCurve(img,display=2):
 
    imgCopy = img.copy()
    imgResult = img.copy()
    #### STEP 1
    imgThres = utlis1.thresholding(img)
 
    #### STEP 2
    hT, wT, c = img.shape
    points = utlis1.valTrackbars()
    imgWarp = utlis1.warpImg(imgThres,points,wT,hT)
    imgWarpPoints = utlis1.drawPoints(imgCopy,points)
 
    #### STEP 3
    middlePoint,imgHist = utlis1.getHistogram(imgWarp,display=True,minPer=0.5,region=3)
    curveAveragePoint, imgHist = utlis1.getHistogram(imgWarp, display=True, minPer=0.9)
    curveRaw = curveAveragePoint - middlePoint
 
    #### SETP 4
    curveList.append(curveRaw)
    if len(curveList)>avgVal:
        curveList.pop(0)
    curve = float(sum(curveList)/len(curveList))
 
    #### STEP 5
    if display != 0:
        imgInvWarp = utlis1.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (int(curve) * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (int(curve) * 3)), midY - 25), (wT // 2 + (int(curve) * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(int(curve) // 50), midY - 10),
                     (w * x + int(int(curve) // 50), midY + 10), (0, 0, 255), 2)
    if display == 2:
        imgStacked = utlis1.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                             [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Resutlt', imgResult)
 
    ### NORMALIZATION
    curve = curve/100
    if curve>1: curve ==1
    if curve<-1:curve == -1
 
    return curve
 
if __name__ == '__main__':
    cap = cv2.VideoCapture('video.avi')
#     cap = cv2.VideoCapture(2)
    cap.set(cv2.CAP_PROP_EXPOSURE,0)
    intialTrackBarVals = [102, 80, 20, 214 ]
    utlis1.initializeTrackbars(intialTrackBarVals)
    while True:
        success, img = cap.read()
        img = cv2.resize(img,(480,240))
        
        curve = getLaneCurve(img,display=2)
        print(curve)
        
        cv2.imshow('Vid',img)
        cv2.waitKey(1)