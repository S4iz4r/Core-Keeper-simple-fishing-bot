import mss
from time import time, sleep
import pyautogui
from functions import *
from datetime import datetime
from threading import Thread


def main():
    sct = mss.mss()
    Type = 1
    filter = filter1
    thershold = 0.60
    duration = 60
    debug = False
    trys, items, fishes, fails, minute = 0, 0, 0, 0, 'minute'
    choice = input(
        '\nDebug mode disabled by default\nDo you want to enable it? Y/N ')
    if choice.lower() == 'y':
        debug = True
        print('\nDebug mode enabled')
    else:
        print('\nDebug mode disabled')
    try:
        duration_choice = int(input(
            f'\nDefault session duration is {duration} minutes\ninsert another duration in minutes if you want to change it: '))
        if duration_choice > 0 and duration_choice != duration:
            duration = duration_choice
        if duration != 1:
            minute += 's'
        print(f'Assigned new duration for the session [{duration} {minute}]')
    except:
        minute = 'minutes'
        print(f'Session duration "default" {duration} {minute}')
        pass

    print(f'\nDefault detection mode is "1"\nYou can try with detection mode "2"')
    while True:
        try:
            detection_choice = int(input('Chose detection mode [1 or 2]: '))
            if detection_choice != 2 and detection_choice != 1:
                print('You only have 2 options [1 or 2] leave the field blank')
            elif detection_choice == 2:
                Type = 2
                filter = filter2
                print(f'\nSelected filter type: {Type}')
                break
            else:
                break
        except:
            print(f'\nSelected filter type: {Type}')
            break

    def fishingBot(sct, start, duration):
        print("\nPress 'q' to quit.")
        print('\nStarting!\n')
        sleep(2)
        trys = 0
        items = 0
        fishes = 0
        fails = 0
        coords = int(screenWidth / 2 + 480), int(screenHeight / 2)
        pyautogui.click(coords)
        sleep(0.2)
        pyautogui.keyDown('d')
        sleep(0.1)
        pyautogui.keyUp('d')
        sleep(1)
        throwRod()
        sleep(1)
        if checkRod(sct)[0] < .50:
            coords = int(screenWidth / 2 - 480), int(screenHeight / 2)
            pyautogui.keyDown('a')
            sleep(0.5)
            pyautogui.keyUp('a')
            sleep(0.2)
            pyautogui.click(coords)
            sleep(0.2)
            throwRod()
            sleep(1)
            if checkRod(sct)[0] < .50:
                print(
                    'Rod not detected, try to place your character closer to the water')
                exit()
        sleep(2)
        trys += 1
        Time = time()
        while True:
            if (time() - Time) > 10:
                if checkRod(sct)[0] < .50:
                    pyautogui.click(coords)
                    sleep(0.1)
                    throwRod()
                    sleep(2)
                    fails += 1
                    trys += 1
                    Time = time()
                Time = time()
            if checkExclamation(sct, exclamation, filter, Type)[0] >= thershold:
                throwRod()
                sleep(0.2)
                if Fishing(sct)[0] >= .70:
                    caught = False
                    Time = time()
                    while Fishing(sct)[0] > .70:
                        Time = time()
                        if pullCheck(sct)[0] >= .50:
                            pullRod()
                        else:
                            releaseRod()
                        fishes, caught, _ = caughtCheck(
                            fishes, caught, sct)
                        if caught:
                            sleep(0.8)
                            throwRod()
                            sleep(0.2)
                        if quit(sct, start, duration, trys, items, fishes, fails, minute, Type):
                            break
                    if not caught:
                        fails += 1
                        releaseRod()
                        sleep(0.1)
                        throwRod()
                    caught = False
                    Time = time()
                else:
                    items += 1
                    Time = time()
                    sleep(0.5)
                    throwRod()
                clear()
                print(f'\nSession started at: {start.strftime("%H:%M:%S")}')
                end = datetime.now()
                print(
                    f'Trys: {trys}\nItems: {items}\nFishes: {fishes}\nFails: {fails}')
                print(
                    f'Actual session duration: {int(divmod((end - start).total_seconds(), 60)[0])} {minute}')
                trys += 1
                sleep(3)
                if checkRod(sct)[0] < .50:
                    fails += 1
                    trys += 1
                    pyautogui.click(coords)
                    sleep(0.1)
                    throwRod()
                    sleep(2)
                Time = time()
            if quit(sct, start, duration, trys, items, fishes, fails, minute, Type):
                break
        return
    start = datetime.now()
    t1 = Thread(target=fishingBot, args=(sct, start, duration,))
    t1.start()
    if debug:
        t2 = Thread(target=showFrames, args=(sct, start, duration, Type,))
        t2.start()


if __name__ == '__main__':
    main()
