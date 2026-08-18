import keyboard
import time
import sys 
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication
from overlay import CursorOverlay
from colour import get_cursor_pixel_colour

HOTKEY = "ctrl + shift + z"
state = False

app = QApplication(sys.argv)
cursor_overlay = CursorOverlay()



def toggleState(): 
    global state 
    state = not state


def quit_app():
    keyboard.unhook_all()
    cursor_overlay.close()
    app.quit()


keyboard.add_hotkey(HOTKEY, callback=toggleState)
keyboard.add_hotkey("ctrl+shift+q", callback=quit_app) #NOTE temporary way to quit the program


def update_overlay():
    if not state: 
        cursor_overlay.hide()
        return 
    
    cursor_overlay.show()
    (r,g,b) ,hex_colour = get_cursor_pixel_colour()

    cursor_overlay.move_to_cursor()
    cursor_overlay.update_colour(r,g,b, hex_colour)

timer = QTimer() 
timer.timeout.connect(update_overlay)
timer.start(50)

app.exec() 