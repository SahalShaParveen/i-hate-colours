import keyboard
import time
import sys 
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication
from overlay import CursorOverlay
from colour import get_cursor_pixel_colour
from colour_names import get_css_name

HOTKEY = "ctrl + shift + z"
quit_requested = False
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


def request_quit():
    global quit_requested
    quit_requested = True


keyboard.add_hotkey(HOTKEY, callback=toggleState)
keyboard.add_hotkey("ctrl+shift+q", callback=request_quit) #NOTE temporary way to quit the program


def update_overlay():
    if quit_requested:
        quit_app()
        return

    if not state: 
        cursor_overlay.hide()
        return
    
    cursor_overlay.show()
    (r,g,b) ,hex_colour = get_cursor_pixel_colour()
    print(get_css_name(hex_colour))

    cursor_overlay.move_to_cursor()
    cursor_overlay.update_colour(r,g,b, hex_colour)

timer = QTimer() 
timer.timeout.connect(update_overlay)
timer.start(50)

app.exec() 