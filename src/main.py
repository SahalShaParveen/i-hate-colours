import pyautogui
import keyboard
import time

HOTKEY = "ctrl + shift + z"

def get_cursor_pixel_colour():
    position = pyautogui.position()
    im = pyautogui.screenshot() 
    colour = im.getpixel(position)
    return colour


def RGBtoHEX(r, g, b): 
    hex = f"#{r:02x}{g:02x}{b:02x}"
    return hex


state = False

def toggleState(): 
    global state 
    state = not state


keyboard.add_hotkey(HOTKEY, callback=toggleState)

while True:
    if state: 
        r, g, b = get_cursor_pixel_colour()
        hex = RGBtoHEX(r,g,b)   

        print(F"({r}, {g}, {b}) | {hex}")
        time.sleep(0.05)
    else: 
        time.sleep(0.1)


# Takes a screenshot once every 0.05 seconds tho. 