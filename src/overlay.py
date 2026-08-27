import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QWidget, QLabel, QFrame, QHBoxLayout
from colour_names import get_css_name
import json

class CursorOverlay(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(8, 6, 8, 6)
        self.layout.setSpacing(8)

        self.colour_box = QFrame()
        self.colour_box.setFixedSize(30, 30)

        self.css_colour_box = QFrame() 
        self.css_colour_box.setFixedSize(30, 30)

        self.text_label = QLabel()

        self.layout.addWidget(self.colour_box)
        self.layout.addWidget(self.css_colour_box)
        self.layout.addWidget(self.text_label)

        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid black;
                border-radius: 4px;
            }

            QLabel {
                border: none;
                color: black;
                font-size: 14px;
                font-weight: bold;
            }
        """)


    def move_to_cursor(self):
        position = QCursor.pos()
        self.move(position.x() + 20, position.y() + 20)


    def update_colour(self, r, g, b, hex_colour, settings):
        text = ""

        colour_name = get_css_name(hex_colour)

        if settings["overlay_text"]["show_colour_name"]:
            text += f"{colour_name}\n"

        if settings["overlay_text"]["show_rgb"]:
            text += f"RGB: ({r}, {g}, {b})\n"

        if settings["overlay_text"]["show_hex"]:
            text += f"HEX: {hex_colour}"

        self.text_label.setText(text)

        self.colour_box.setStyleSheet(f"""
            QFrame {{
                background-color: {hex_colour};
                border: 1px solid black;
                border-radius: 3px;
            }}
        """)

        #NOTE: .....TEMPORARY. TO REMOVE OR CHANGE LATER:.....
        with open("data/css-colours.json", "r") as f:
            css_colours = json.load(f)

        for x in css_colours: 
            if css_colours.get(x) == colour_name: 
                css_hex = x

        self.css_colour_box.setStyleSheet(f"""
            QFrame {{
                background-color: {css_hex};
                border: 1px solid black;
                border-radius: 3px;
            }}
        """)
        # ......................................................
        self.adjustSize()