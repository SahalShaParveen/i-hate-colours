import pyautogui
import time

def RGBtoHEX(r, g, b): 
    hex = f"#{r:02x}{g:02x}{b:02x}"
    return hex

while True: 
    position = pyautogui.position()
    im = pyautogui.screenshot() 
    colour = im.getpixel(position)

    r, g, b = colour
    hex = RGBtoHEX(r,g,b)


    print(F"{position} | {colour} | {hex}")
    time.sleep(0.05)


# Takes a screenshot once every 0.05 seconds tho. 