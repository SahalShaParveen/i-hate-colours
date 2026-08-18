import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QLabel


class CursorOverlay(QLabel): 
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.setText("RGB: (0, 0, 0)\nHEX: #000000")

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
        self.setText(f"RGB: ({r}, {g}, {b})\nHEX: {hex_colour}")
        self.adjustSize()


    def move_to_cursor(self):
        position = QCursor.pos()
        self.move(position.x() + 20, position.y() + 20)     