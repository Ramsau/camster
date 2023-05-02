import cv2 as cv
from Xlib import display
import pyautogui
import settings as _
import requests

clickLoc = (0, 0)
lightOn = False

def vidLoop(background):
    cap = cv.VideoCapture(0)
    while True:
        processNewFrame(cap, background)

        if cv.waitKey(1) & 0xFF == ord('y'):
            cv.destroyAllWindows()
            break

    cap.release()


def rectContains(leftTop, rightBottom,pt):
    logic = leftTop[0] < pt[0] < rightBottom[0] and leftTop[1] < pt[1] < rightBottom[1]
    return logic


def processNewFrame(cap, background):
    global clickLoc
    # get frame
    ret, frame = cap.read()
    # get brightest red pixel
    minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(frame[:, :, 2])
    # draw pos of brightest pixel
    brightEnough = maxVal > _.BrightnessAccept
    insideScreen = rectContains(_.WebcamLT, _.WebcamRB, maxLoc)
    insideLightswitch = rectContains(_.LightswitchLT, _.LightswitchRB, maxLoc)

    if not brightEnough:
        if rectContains(_.WebcamLT, _.WebcamRB, clickLoc):
            clickOn(translateToScreen(clickLoc))
        elif rectContains(_.LightswitchLT, _.LightswitchRB, clickLoc):
            toggleLightswitch()

    if brightEnough and insideScreen:
        clr = (0, 0, 255)
        clickLoc = maxLoc
        moveMouseAbs(translateToScreen(clickLoc))
    elif brightEnough and insideLightswitch:
        clr = (0, 255, 0)
        clickLoc = maxLoc
    else:
        clr = (255, 0, 0)
        clickLoc = (0, 0)

    if not background:
        # screen
        cv.rectangle(frame, _.WebcamLT, _.WebcamRB, (0, 255, 0), 1)
        # lightswitch
        cv.rectangle(frame, _.LightswitchLT, _.LightswitchRB, (255, 0, 255), 1)
        # laser dot
        cv.circle(frame, maxLoc, 2, clr, 2)
        cv.imshow('img', frame)


def getPointerPos():
    data = display.Display().screen().root.query_pointer()._data
    return data['root_x'] + _.ScreenOffsetX, data['root_y'] - _.ScreenOffsetY


def moveMouseAbs(pt):
    pyautogui.moveTo(pt[0], pt[1])

def clickOn(pt):
    pyautogui.moveTo(pt[0], pt[1])
    pyautogui.click()

def translateToScreen(pt):
    x_rel = (_.WebcamLT[0] - pt[0]) / _.Webcam_X
    y_rel = (_.WebcamLT[1] - pt[1]) / _.Webcam_Y

    if _.FlipScreen:
        x_rel = 1 - x_rel
        y_rel = 1 - y_rel

    screenSize = pyautogui.size()
    screenSize = (screenSize[0] + _.ScreenOffsetX, screenSize[1] + _.ScreenOffsetY)

    point = (int(x_rel * screenSize[0]) - _.ScreenOffsetX, int(y_rel * screenSize[1]) - _.ScreenOffsetY)

    return point

def toggleLightswitch():
    global lightOn
    turn = 'on' if lightOn else 'off'
    requests.get('http://192.168.0.8:2060/lights?turn=%s' % (turn))
    lightOn = not lightOn
