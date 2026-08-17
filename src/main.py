import pyautogui
import time

while True: 
    position = pyautogui.position()
    im = pyautogui.screenshot() 
    colour = im.getpixel(position)
    print(F"{position} | {colour}")
    time.sleep(0.05)
