import cv2
import mss
import numpy
import pyautogui
from time import sleep
import keyboard
from datetime import datetime
import win32gui
import win32con
import os
def clear(): return os.system('cls')

class HsvFilter:

    def __init__(self, hMin=None, sMin=None, vMin=None, hMax=None, sMax=None, vMax=None,
                 sAdd=None, sSub=None, vAdd=None, vSub=None):
        self.hMin = hMin
        self.sMin = sMin
        self.vMin = vMin
        self.hMax = hMax
        self.sMax = sMax
        self.vMax = vMax
        self.sAdd = sAdd
        self.sSub = sSub
        self.vAdd = vAdd
        self.vSub = vSub

sct = mss.mss()

cork = cv2.imread('img/cork.jpg', cv2.IMREAD_UNCHANGED)
processed_cork = cv2.imread('img/processedCork.jpg', cv2.IMREAD_UNCHANGED)
filter1 = HsvFilter(111, 0, 59, 179, 254, 255, 103, 0, 255, 54)
processed_cork2 = cv2.imread('img/processedCork.jpg', cv2.IMREAD_UNCHANGED)
filter2 = HsvFilter(115, 0, 0, 179, 255, 203, 226, 0, 115, 36)
rod = cv2.imread('img/rod.jpg', cv2.IMREAD_GRAYSCALE)
rodLeft = cv2.imread('img/rodLeft.jpg', cv2.IMREAD_GRAYSCALE)
fishing = cv2.imread('img/fishing.jpg', cv2.IMREAD_GRAYSCALE)
pull = cv2.imread('img/pullFish.jpg', cv2.IMREAD_UNCHANGED)
fishCaught = cv2.imread('img/fishCaught.jpg', cv2.IMREAD_UNCHANGED)

fishing_dimensions = {
    'left': 750,
    'top': 820,
    'width': 420,
    'height': 145
}

player_dimensions = {
    'left': 860,
    'top': 450,
    'width': 200,
    'height': 150
}
dimensions_left = {
    'left': 882,
    'top': 565,
    'width': 40,
    'height': 20
}
dimensions = {
    'left': 1005,
    'top': 565,
    'width': 40,
    'height': 20
}
full_dimensions = {
    'left': 0,
    'top': 0,
    'width': 1920,
    'height': 1080
}


def checkCork(sct, img=processed_cork, filter=filter1, Type=1, dimensions_right=dimensions, dimensions_left=dimensions_left):
    if checkRod(sct)[2]:
        dimensions = dimensions_right
    else:
        dimensions = dimensions_left
    scr = numpy.array(sct.grab(dimensions))
    scr = apply_hsv_filter(scr, filter, Type)
    result = cv2.matchTemplate(
        scr, img, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    return max_val, result


def checkRod(sct, img=rod, imgl=rodLeft, dimensions=player_dimensions):
    scr = numpy.array(sct.grab(dimensions))
    scr_remove = cv2.cvtColor(scr, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(
        scr_remove, img, cv2.TM_CCOEFF_NORMED)
    resultL = cv2.matchTemplate(
        scr_remove, imgl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    _, max_valL, _, max_locL = cv2.minMaxLoc(resultL)
    if max_valL > max_val + (max_val * 20 / 100):
        rodRight = False
        return max_valL, resultL, rodRight
    else:
        rodRight = True
        return max_val, result, rodRight


def throwRod():
    pyautogui.press('5')
    sleep(0.1)
    pyautogui.hotkey('alt', '1')
    return


def Fishing(sct, img=fishing, dimensions=fishing_dimensions):
    scr = numpy.array(sct.grab(dimensions))
    scr_remove = cv2.cvtColor(scr, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(scr_remove, img, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    return max_val


def pullCheck(sct, img=pull, dimensions=fishing_dimensions):
    scr = numpy.array(sct.grab(dimensions))
    scr_remove = scr[:, :, :3]
    result = cv2.matchTemplate(scr_remove, img, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    return max_val, result


def pullRod():
    pyautogui.keyDown('alt')
    pyautogui.keyDown('1')


def releaseRod():
    pyautogui.keyUp('1')
    pyautogui.keyUp('alt')


def caughtCheck(fishes, caught, sct, img=fishCaught, dimensions=fishing_dimensions):
    scr = numpy.array(sct.grab(dimensions))
    scr_remove = scr[:, :, :3]
    result = cv2.matchTemplate(scr_remove, img, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val >= .82:
        fishes += 1
        caught = True
        releaseRod()
        return fishes, caught, result
    else:
        return fishes, caught, result


def apply_hsv_filter(sct, hsv_filter, Type):
    if Type == 1:
        name = 'filter1'
    else:
        name = 'filter2'
    hsv = cv2.cvtColor(sct, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = shift_channel(s, hsv_filter.sAdd)
    s = shift_channel(s, -hsv_filter.sSub)
    v = shift_channel(v, hsv_filter.vAdd)
    v = shift_channel(v, -hsv_filter.vSub)
    hsv = cv2.merge([h, s, v])
    lower = numpy.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
    upper = numpy.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(hsv, hsv, mask=mask)
    img = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)
    return img


def shift_channel(c, amount):
    if amount > 0:
        lim = 255 - amount
        c[c >= lim] = 255
        c[c < lim] += amount
    elif amount < 0:
        amount = -amount
        lim = amount
        c[c <= lim] = 0
        c[c > lim] -= amount
    return c


def showRectangles(sct, result, threshold, target, dimensions, text, fullScreen=full_dimensions):
    try:
        scr = numpy.array(sct.grab(fullScreen))
    except:
        scr = sct
    w = target.shape[1]
    h = target.shape[0]
    rectangles = []
    try:
        yloc, xloc = numpy.where(result[1] >= threshold)
    except:
        yloc, xloc = numpy.where(result[2] >= threshold)
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x + dimensions['left']), int(y + dimensions['top']), int(w), int(h)])
        rectangles.append([int(x + dimensions['left']), int(y + dimensions['top']), int(w), int(h)])
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.3)
    for (x, y, w, h) in rectangles:
        cv2.rectangle(scr, (x, y), (x + w, y + h), (0, 255, 0), 2)
        org = (int(x), int(y + h + 15))
        fontFace = cv2.FONT_HERSHEY_DUPLEX
        fontScale = 0.5
        color = (0, 255, 25)
        scr = cv2.putText(scr, text, org, fontFace, fontScale, color)
    return scr


def showDetectionArea(sct, dimensions, text, fullScreen=full_dimensions):
    try:
        scr = numpy.array(sct.grab(fullScreen))
    except:
        scr = sct
    cv2.rectangle(scr, (dimensions['left'], dimensions['top']), (dimensions['left'] + dimensions['width'], dimensions['top'] + dimensions['height']), (0, 0, 255), 2)
    org = (dimensions['left'], dimensions['top'] - 10)
    fontFace = cv2.FONT_HERSHEY_DUPLEX
    fontScale = 0.5
    color = (0, 0, 255)
    scr = cv2.putText(scr, text, org, fontFace, fontScale, color)
    return scr


def showFrames(sct, start, duration, Type, dimensions_right=dimensions, dimensions_left=dimensions_left):

    while True:
        if checkRod(sct)[2]:
            dimensions = dimensions_right
        else:
            dimensions = dimensions_left
        if Type == 1:
            img = showRectangles(sct, checkCork(sct), 0.55, processed_cork, dimensions, 'cork  **1**')
            name = 'fishing with filter1'
        else:
            img = showRectangles(sct, checkCork(sct, processed_cork2, filter2, 2), 0.55, processed_cork2, dimensions, 'cork  **2**')
            name = 'fishing with filter2'
        img = showRectangles(img, checkRod(sct), 0.70, rod, player_dimensions, 'Rod')
        img = showRectangles(img, pullCheck(sct), 0.80, pull, fishing_dimensions, 'Fishing')
        img = showRectangles(img, caughtCheck(0, None, sct),  0.82, fishCaught, fishing_dimensions, 'Caught!')
        img = showDetectionArea(showDetectionArea(showDetectionArea(img, fishing_dimensions, 'Fishing area'), player_dimensions, 'Player area'), dimensions, 'Cork area')
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(name, 440, 500)
        hWnd = win32gui.FindWindow(None, name)
        win32gui.SetWindowPos(hWnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
        cv2.imshow(name, img[400:900, 740:1180])
        cv2.waitKey(1)
        if keyboard.is_pressed('q') or divmod((datetime.now() - start).total_seconds(), 60)[0] >= duration:
            break


def quit(sct, start, duration, trys, items, fishes, fails, minute, Type):
    if keyboard.is_pressed('q') or divmod((datetime.now() - start).total_seconds(), 60)[0] >= duration:
        end = datetime.now()
        clear()
        if checkRod(sct)[0] >= .60:
            throwRod()
        total_duration = int(divmod((end - start).total_seconds(), 60)[0])
        clear()
        print(f'\nSession started at: {start.strftime("%H:%M:%S")}')
        print(f'Trys: {trys}\nItems: {items}\nFishes: {fishes}\nFails: {fails}')
        print(f'Session ended at: {end.strftime("%H:%M:%S")}')
        print(f'Session duration: {total_duration} {minute}')
        try:
            print(
                f'Catches per minute ratio: {(items + fishes) / total_duration}')
        except:
            print('Too little time to be able to calculate the catches/minute ratio')
        print(f'Filter type: {Type}')
        print('\nPress "q" to quit')
        keyboart.wait('q')
        return True
