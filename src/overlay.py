from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QWidget, QLabel, QFrame, QHBoxLayout, QVBoxLayout
from colour_utils import get_nearest_colour
from colour_model import Colour


class CursorOverlay(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(8, 6, 8, 6)
        self.layout.setSpacing(12)

        self.pixel_colour_thumbnail = ColourThumbnail("Pixel colour")
        self.nearest_colour_thumbnail = ColourThumbnail("Nearest CSS colour")

        self.text_label = QLabel()
        self.text_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.layout.addWidget(self.pixel_colour_thumbnail)
        self.layout.addWidget(self.nearest_colour_thumbnail)
        self.layout.addWidget(self.text_label)

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

    def update_overlay(self, colour: Colour, settings: dict, colour_system: list[Colour]):
        nearest_colour = get_nearest_colour(
            colour, settings["overlay_text"]["distance_metric"], colour_system)

        text = ""

        if settings["overlay_text"]["show_colour_name"]:
            text += f"Closest Match: {nearest_colour.name}\n"

        if settings["overlay_text"]["show_rgb"]:
            r, g, b = colour.rgb
            text += f"RGB: ({r}, {g}, {b})\n"

        if settings["overlay_text"]["show_hex"]:
            text += f"HEX: {colour.hex}"

        self.text_label.setText(text)

        self.pixel_colour_thumbnail.set_colour(colour)
        self.nearest_colour_thumbnail.set_colour(nearest_colour)

        self.adjustSize()


class ColourThumbnail(QWidget):
    def __init__(self, text: str, size: int = 50):
        super().__init__()

        self.size = size

        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)

        self.colour_box = QFrame()
        self.colour_box.setFixedSize(size, size)

        self.label = QLabel(text)
        self.label.setObjectName("colourLabel")
        self.label.setFixedWidth(size)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.colour_box, alignment=Qt.AlignHCenter)

        layout.addWidget(self.label)

    def set_colour(self, colour: Colour):
        self.colour_box.setStyleSheet(f"""
            QFrame {{
                background-color: {colour.hex};
                border: 2px solid black;
                border-radius: 0px;
            }}
        """)
