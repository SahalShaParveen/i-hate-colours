import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QWidget, QLabel, QFrame, QHBoxLayout, QVBoxLayout
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
        self.layout.setSpacing(12)

        # Pixel colour
        colour_layout = QVBoxLayout()
        colour_layout.setSpacing(4)

        self.colour_box = QFrame()
        self.colour_box.setFixedSize(50, 50)

        colour_label = QLabel("Pixel colour")
        colour_label.setAlignment(Qt.AlignCenter)
        colour_label.setStyleSheet("""
            QLabel {
                border: none;
                color: black;
                font-size: 10px;
                font-weight: normal;
            }
        """)

        colour_layout.addWidget(self.colour_box)
        colour_layout.addWidget(colour_label)

        # Closest CSS colour
        css_layout = QVBoxLayout()
        css_layout.setSpacing(4)

        self.css_colour_box = QFrame()
        self.css_colour_box.setFixedSize(50, 50)

        css_label = QLabel("Closest CSS")
        css_label.setAlignment(Qt.AlignCenter)
        css_label.setStyleSheet("""
            QLabel {
                border: none;
                color: black;
                font-size: 10px;
                font-weight: normal;
            }
        """)

        css_layout.addWidget(self.css_colour_box)
        css_layout.addWidget(css_label)

        # Text
        self.text_label = QLabel()
        self.text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.layout.addLayout(colour_layout)
        self.layout.addLayout(css_layout)
        self.layout.addWidget(self.text_label)

        colour_label.setObjectName("colourLabel")
        css_label.setObjectName("colourLabel")

        self.setStyleSheet("""
            CursorOverlay {
                background-color: white;
                border: 2px solid black;
                border-radius: 0px;
            }

            QLabel {
                border: none;
                color: black;
                font-size: 14px;
                font-weight: normal;
            }

            QLabel#colourLabel {
                font-size: 10px;
            }
        """)


    def move_to_cursor(self):
        position = QCursor.pos()
        self.move(position.x() + 20, position.y() + 20)

    def update_colour(self, r, g, b, hex_colour, settings):
        text = ""

        colour_name = get_css_name(hex_colour, settings["overlay_text"]["distance_metric"])

        if settings["overlay_text"]["show_colour_name"]:
            text += f"Closest Match: {colour_name}\n"

        if settings["overlay_text"]["show_rgb"]:
            text += f"RGB: ({r}, {g}, {b})\n"

        if settings["overlay_text"]["show_hex"]:
            text += f"HEX: {hex_colour}"

        self.text_label.setText(text)

        self.colour_box.setStyleSheet(f"""
            QFrame {{
                background-color: {hex_colour};
                border: 2px solid black;
                border-radius: 0px;
            }}
        """)

        #NOTE: .....TEMPORARY. TO REMOVE OR CHANGE LATER:.....
        with open("data/css-colours.json", "r") as f:
            css_colours = json.load(f)

        css_hex = hex_colour

        for x in css_colours:
            if css_colours.get(x) == colour_name:
                css_hex = x
                break

        self.css_colour_box.setStyleSheet(f"""
            QFrame {{
                background-color: {css_hex};
                border: 2px solid black;
                border-radius: 0px;
            }}
        """)
        # ......................................................
        self.adjustSize()