import keyboard
import sys
import json
from PySide6.QtCore import Qt, QTimer, QObject, Signal
from PySide6.QtWidgets import QApplication
from overlay import CursorOverlay
from colour_utils import get_cursor_pixel_colour, load_colour_system
import config


def get_settings():
    global settings
    global colour_system

    with open("data/settings.json", "r") as f:
        settings = json.load(f)

    colour_system = load_colour_system(
        settings["overlay_text"]["colour_system"])


get_settings()

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
    config_window = config.SettingsWindow(hotkey_bridge)
    config_window.resize(350, 250)
    config_window.show()
    config_window.raise_()
    config_window.activateWindow()


class HotkeyBridge(QObject):
    config_requested = Signal()
    quit_signal = Signal()
    update_settings_signal = Signal()


hotkey_bridge = HotkeyBridge()
hotkey_bridge.config_requested.connect(open_config_window)
hotkey_bridge.quit_signal.connect(request_quit)
hotkey_bridge.update_settings_signal.connect(get_settings)

keyboard.add_hotkey(settings["hotkey"], callback=toggleState)
keyboard.add_hotkey(settings["config_hotkey"],
                    callback=hotkey_bridge.config_requested.emit)


# Temporary quit hotkey to use when testing:
keyboard.add_hotkey("ctrl + alt + x", callback=hotkey_bridge.quit_signal.emit)


def update_overlay():
    if quit_requested:
        quit_app()
        return

    if not state:
        cursor_overlay.hide()
        return

    cursor_overlay.show()
    pixel_colour = get_cursor_pixel_colour()

    cursor_overlay.move_to_cursor()
    cursor_overlay.update_overlay(pixel_colour, settings, colour_system)


timer = QTimer()
timer.timeout.connect(update_overlay)
timer.start(settings["delay_ms"])

app.exec()
