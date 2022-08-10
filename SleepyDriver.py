import time

import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector

video = cv2.VideoCapture(0)
video.set(3, 1280)
video.set(4, 720)

detector = FaceMeshDetector(maxFaces=1)
i = 0
while True:
    success, img = video.read()
    img, faces = detector.findFaceMesh(img, draw=True)

    try:
        face = faces[0]
        # solKasUst 159 solKasAlt
        # sagKasUst 386 solKasAlt
        leftEye = face[145]
        rightEye = face[374]
        sagKasUst = face[386]
        solKasUst = face[159]
        ustDudak = face[13]
        altDudak = face[14]


        cv2.circle(img, leftEye, 5, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, sagKasUst, 5, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, solKasUst, 5, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, rightEye, 5, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, ustDudak, 5, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, altDudak, 5, (255, 0, 255), cv2.FILLED)

        cv2.line(img, leftEye, rightEye, (0, 200, 0), 3)
        cv2.line(img, leftEye, solKasUst, (0, 200, 0), 3)
        cv2.line(img, rightEye, sagKasUst, (0, 200, 0), 3)
        cv2.line(img, ustDudak, altDudak, (0, 200, 0), 3)
        w, _ = detector.findDistance(leftEye, rightEye)
        closeEyePX, _ = detector.findDistance(leftEye, solKasUst)
        yawnDistPX, _ = detector.findDistance(ustDudak, altDudak)
        W2 = 2
        W = 6.3
        d = 50
        f = 740
        d = (W * f) / w

        f2 = (closeEyePX * d) / W2
        f3 = (yawnDistPX * d) / W2
        print(f3)

        if f2 < 280 or f3 > 750:
            i += 1
           # print(i)
        else:
            i = 0

        cvzone.putTextRect(img, f'Distance: {int(d)} cm', (900, 100), scale=2)
        if d <= 35 or i > 5:
            cvzone.putTextRect(img, "You are sleeping.. PLEASE WAKE UP !", (300, 500), scale=2)


    except IndexError:
        cvzone.putTextRect(img, "You are sleeping.. PLEASE WAKE UP !", (300, 500), scale=2)

    cv2.imshow("Sleepy Driver Checker", img)
    cv2.waitKey(1)
