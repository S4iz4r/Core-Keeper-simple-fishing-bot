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
cv2.namedWindow("dst", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("dst", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
_, _, screenWidth, screenHeight = cv2.getWindowImageRect('dst')
cv2.destroyAllWindows()
print(f'Meassured screen size: {screenWidth}x{screenHeight}')

exclamation = cv2.imread('img/exclamation.jpg', cv2.IMREAD_UNCHANGED)
filter1 = HsvFilter(111, 0, 59, 179, 254, 255, 103, 0, 255, 54)
filter2 = HsvFilter(115, 0, 0, 179, 255, 203, 226, 0, 115, 36)
rod = cv2.imread('img/rod.jpg', cv2.IMREAD_GRAYSCALE)
rodLeft = cv2.imread('img/rodLeft.jpg', cv2.IMREAD_GRAYSCALE)
fishing = cv2.imread('img/fishing.jpg', cv2.IMREAD_GRAYSCALE)
# pull = cv2.imread('img/pullFish.jpg', cv2.IMREAD_UNCHANGED)
pull = cv2.imread('img/pullFish.jpg', cv2.IMREAD_GRAYSCALE)
fishCaught = cv2.imread('img/fishCaught.jpg', cv2.IMREAD_UNCHANGED)

fishing_dimensions = {
    'left': int(screenWidth / 2 - 275),
    'top': int(screenHeight / 2 + 383),
    'width': 552,
    'height': 105
}

player_dimensions = {
    'left': int(screenWidth / 2 - 120),  # 860
    'top': int(screenHeight / 2 - 140),  # 450
    'width': 225,
    'height': 180
}
dimensions_left = {
    'left': int(screenWidth / 2 - 55),  # 882
    'top': int(screenHeight / 2 - 230),  # 565
    'width': 100,
    'height': 100
}
dimensions = {
    'left': int(screenWidth / 2 - 55),  # 1005
    'top': int(screenHeight / 2 - 230),  # 565,
    'width': 100,
    'height': 100
}
full_dimensions = {
    'left': 0,
    'top': 0,
    'width': screenWidth,
    'height': screenHeight
}


def checkExclamation(sct, img=exclamation, filter=filter1, Type=1, dimensions=dimensions):
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
    return max_val, result


def pullCheck(sct, img=pull, dimensions=fishing_dimensions):
    scr = numpy.array(sct.grab(dimensions))
    scr_remove = cv2.cvtColor(scr, cv2.COLOR_BGR2GRAY)
    # scr_remove = scr[:, :, :3]
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
    if max_val >= .42:
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
        text += f' {round(result[0], 2)}'
    except:
        yloc, xloc = numpy.where(result[2] >= threshold)
        text += f' {round(result[0], 2)}'
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x + dimensions['left']),
                          int(y + dimensions['top']), int(w), int(h)])
        rectangles.append([int(x + dimensions['left']),
                          int(y + dimensions['top']), int(w), int(h)])
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
    cv2.rectangle(scr, (dimensions['left'], dimensions['top']), (dimensions['left'] +
                  dimensions['width'], dimensions['top'] + dimensions['height']), (0, 0, 255), 2)
    org = (dimensions['left'], dimensions['top'] - 10)
    fontFace = cv2.FONT_HERSHEY_DUPLEX
    fontScale = 0.5
    color = (0, 0, 255)
    scr = cv2.putText(scr, text, org, fontFace, fontScale, color)
    return scr


def showFrames(sct, start, duration, Type, dimensions=dimensions):

    while True:
        if Type == 1:
            img = showRectangles(sct, checkExclamation(
                sct), 0.55, exclamation, dimensions, 'exclamation')
            name = 'fishing with filter1'
        else:
            img = showRectangles(sct, checkExclamation(
                sct, exclamation, filter2, 2), 0.55, exclamation, dimensions, 'exclamation')
            name = 'fishing with filter2'
        img = showRectangles(img, checkRod(sct), 0.60,
                             rod, player_dimensions, 'Rod')
        img = showRectangles(img, Fishing(sct), 0.60,
                             fishing, fishing_dimensions, 'Fishing')
        img = showRectangles(img, pullCheck(sct), 0.55,
                             pull, fishing_dimensions, 'Pulling')
        img = showRectangles(img, caughtCheck(0, None, sct),
                             0.42, fishCaught, fishing_dimensions, 'Caught!')
        img = showDetectionArea(showDetectionArea(showDetectionArea(
            img, fishing_dimensions, 'Fishing area'), dimensions, 'Cork area'), player_dimensions, 'Player area')
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(name, 600, 750)
        hWnd = win32gui.FindWindow(None, name)
        win32gui.SetWindowPos(hWnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
        cv2.imshow(name, img[int(screenHeight / 2 - 250):int(screenHeight /
                                                             2 + 500), int(screenWidth / 2 - 300):int(screenWidth / 2 + 300)])

        cv2.waitKey(1)
        if keyboard.is_pressed('q') or divmod((datetime.now() - start).total_seconds(), 60)[0] >= duration:
            break


def quit(sct, start, duration, trys, items, fishes, fails, minute, Type):
    if keyboard.is_pressed('q') or divmod((datetime.now() - start).total_seconds(), 60)[0] >= duration:
        end = datetime.now()
        clear()
        if checkRod(sct)[0] >= .65:
            throwRod()
        total_duration = int(divmod((end - start).total_seconds(), 60)[0])
        clear()
        text = f'Session started at: {start.strftime("%H:%M:%S")}\nTrys: {trys}\nItems: {items}\nFishes: {fishes}\nFails: {fails}\nSession ended at: {end.strftime("%H:%M:%S")}\nSession duration: {total_duration} {minute}\nFilter type: {Type}'
        try:
            text += f'\nCatches per minute ratio: {round((items + fishes) / total_duration, 2)}'
        except:
            text += '\nToo little time to be able to calculate the catches/minute ratio'
        with open('results.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        f.close()
        print('Press "q" to quit')
        keyboard.wait('q')
        print('Results saved in the file "results.txt"')
        return True
