import keyboard
import time
import sys 
import json
from PySide6.QtCore import Qt, QTimer, QObject, Signal
from PySide6.QtWidgets import QApplication
from overlay import CursorOverlay
from colour import get_cursor_pixel_colour
from colour_names import get_css_name
import config

def get_settings():
    with open("data/settings.json", "r") as f:
        settings = json.load(f)
        return settings


settings = get_settings()
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

def open_config_window(): 
    global config_window
    config_window = config.SettingsWindow()
    config_window.resize(350, 250)
    config_window.show()
    config_window.raise_()
    config_window.activateWindow()


class HotkeyBridge(QObject):
    config_requested = Signal()


hotkey_bridge = HotkeyBridge()
hotkey_bridge.config_requested.connect(open_config_window)

keyboard.add_hotkey(settings["hotkey"], callback=toggleState)
keyboard.add_hotkey(settings["config_hotkey"], callback=hotkey_bridge.config_requested.emit) #NOTE temporary way to quit the program


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
    cursor_overlay.update_colour(r,g,b, hex_colour, settings)

timer = QTimer() 
timer.timeout.connect(update_overlay)
timer.start(settings["delay_ms"])

app.exec() 
