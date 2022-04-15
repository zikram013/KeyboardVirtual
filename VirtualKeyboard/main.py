import cv2
import cvzone
import mediapipe
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Captura el video
cap.set(3, 1280)  # Resolucion
cap.set(4, 720)  # Resolucion

detector = HandDetector(detectionCon=1)

keyboard_keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                 ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Ñ", ";"],
                 ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

final_text = ""
keyboard = Controller()


def draw(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1],
                                                   button.size[0],button.size[0]), 20 ,rt=0)
        cv2.rectangle(img, button.pos, (int(x + w), int(y + h)), (255, 144, 30), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
    return img




def transparent_layout(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1],
                                                   button.size[0],button.size[0]), 20 ,rt=0)
        cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
                                   (255, 144, 30), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

    out = img.copy()
    alpaha = 0.5
    mask = imgNew.astype(bool)
    print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpaha, imgNew, 1-alpaha, 0)[mask]
    return out


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.text = text
        self.size = size


buttonList = []
for h in range(len(keyboard_keys)):
    for x, key in enumerate(keyboard_keys[h]):
        buttonList.append(Button([100 * x + 25, 100 * h + 50], key))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxIngo = detector.findPosition(img)
    img = draw(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 255), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.QT_FONT_BLACK, 4, (0, 0, 0), 4)
                l, _, _ = detector.findDistance(8, 12, img,False)
                print(l)

                if l<25:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.QT_FONT_BLACK, 4, (0, 0, 0), 4)
                    final_text += button.text
                    sleep(0.20)
    cv2.rectangle(img,(25,350), (700,450), (255, 255, 255), cv2.FILLED)
    cv2.putText(img,final_text, (60,425), cv2.QT_FONT_BLACK, 4, (0, 0, 0), 4)
    cv2.imshow("output",img)
    cv2.waitKey(1)