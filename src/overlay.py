import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QLabel
from colour_names import get_css_name

class CursorOverlay(QLabel): 
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.setText(" ")

        self.setStyleSheet("""
            QLabel {
                background-color: white;
                color: black;
                font-size: 14px;
                font-weight: bold;
                padding: 6px 8px;
                border: 1px solid black;
                border-radius: 4px;
            }
        """)


    def update_colour(self, r, g, b, hex_colour):
        text = f"RGB: ({r}, {g}, {b})" + "\n"
        text += f"HEX: {hex_colour}" + "\n"
        text += f"{get_css_name(hex_colour)}"
        self.setText(text)
        self.adjustSize()
        self.isTopLevel = True


    def move_to_cursor(self):
        position = QCursor.pos()
        self.move(position.x() + 20, position.y() + 20)     