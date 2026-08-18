import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QCursor, QShortcut, QKeySequence
from PySide6.QtWidgets import QApplication, QLabel


app = QApplication(sys.argv)

label = QLabel("Hello!")
label.setWindowFlag(Qt.FramelessWindowHint)


def move_to_cursor():
    position = QCursor.pos()
    label.move(position.x() + 20, position.y() + 20)


timer = QTimer()
timer.timeout.connect(move_to_cursor)
timer.start(20)


shortcut = QShortcut(QKeySequence("Esc"), label)
shortcut.activated.connect(app.quit)


label.show()

app.exec()