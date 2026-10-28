import json
import sys
from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QComboBox,
    QPushButton,
    QPushButton,
    QSpinBox,
    QSlider
)


CONFIG_FILE = "data/settings.json"


class SettingsWindow(QWidget):
    def __init__(self, hotkey_bridge):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.settings = self.load_settings()

        self.hotkey_bridge = hotkey_bridge

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Settings"))

        self.show_colour_name_checkbox = QCheckBox("Show colour name")
        layout.addWidget(self.show_colour_name_checkbox)

        self.show_rgb_checkbox = QCheckBox("Show RGB values")
        layout.addWidget(self.show_rgb_checkbox)

        self.show_hex_checkbox = QCheckBox("Show Hex code")
        layout.addWidget(self.show_hex_checkbox)

        self.show_colour_thumbnail_checkbox = QCheckBox(
            "Show pixel colour thumbnail")
        layout.addWidget(self.show_colour_thumbnail_checkbox)

        self.show_nearest_colour_thumbnail_checkbox = QCheckBox(
            "Show nearest colour thumbnail")
        layout.addWidget(self.show_nearest_colour_thumbnail_checkbox)

        # Font size control
        self.font_size_spinbox, self.font_size_slider = (
            self.create_size_control(
                "Font size:",
                "font_size",
                default=14,
                minimum=6,
                maximum=72,
                layout=layout,
            )
        )

        # Thumbnail size control
        self.thumbnail_size_spinbox, self.thumbnail_size_slider = (
            self.create_size_control(
                "Thumbnail size:",
                "thumbnail_size",
                default=50,
                minimum=10,
                maximum=150,
                layout=layout,
            )
        )

        self.colour_system_dropdown = QComboBox()
        self.colour_system_dropdown.addItems(
            self.settings["colour_system_list"])
        layout.addWidget(QLabel("Colour naming system:"))
        layout.addWidget(self.colour_system_dropdown)

        self.distance_metric_dropdown = QComboBox()
        self.distance_metric_dropdown.addItems(
            self.settings["distance_metric_list"])
        layout.addWidget(QLabel("Colour distance:"))
        layout.addWidget(self.distance_metric_dropdown)

        layout.addSpacing(10)

        layout.addWidget(
            QLabel(f"Cursor Overlay hotkey: \t{self.settings['hotkey']}"))
        layout.addWidget(
            QLabel(f"Config Window hotkey: \t{self.settings['config_hotkey']}"))

        button_layout = QHBoxLayout()

        layout.addSpacing(10)

        self.quit_app_button = QPushButton("Quit App")
        self.quit_app_button.clicked.connect(self.quit_app)
        button_layout.addWidget(self.quit_app_button)

        button_layout.addStretch()

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_settings)
        button_layout.addWidget(self.apply_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.load_into_gui()

    # JSON

    def load_settings(self):
        try:
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)

        except FileNotFoundError:
            # Default settings if the file doesn't exist
            return {
                "hotkey": "ctrl + shift + z",
                "config_hotkey": "alt + shift + z",
                "colour_system": "css",
                "distance_metric": "CIE76",
                "delay_ms": 20,
                "overlay": {
                    "colour_name": True,
                    "rgb": True,
                    "hex": True,
                    "colour_thumbnail": True,
                    "nearest_colour_thumbnail": True,
                    "font_size": 45,
                    "thumbnail_size": 30
                },
                "colour_system_list": [
                    "css"
                ],
                "distance_metric_list": [
                    "CIE76",
                    "CIEDE2000",
                    "RGB_Euclidean"
                ]
            }

    def save_settings(self):
        with open(CONFIG_FILE, "w") as file:
            json.dump(self.settings, file, indent=4)

    def create_size_control(
        self,
        label_text: str,
        setting_key: str,
        default: int,
        minimum: int,
        maximum: int,
        layout: QVBoxLayout,
    ):
        row = QHBoxLayout()

        label = QLabel(label_text)
        row.addWidget(label)

        spinbox = QSpinBox()
        spinbox.setRange(minimum, maximum)
        spinbox.setValue(
            self.settings["overlay"].get(setting_key, default)
        )
        row.addWidget(spinbox)

        slider = QSlider(Qt.Horizontal)
        slider.setRange(minimum, maximum)
        slider.setValue(spinbox.value())
        row.addWidget(slider, stretch=1)

        # Typing a number updates the slider.
        spinbox.valueChanged.connect(slider.setValue)

        # Moving the slider updates the number.
        slider.valueChanged.connect(spinbox.setValue)

        layout.addLayout(row)

        return spinbox, slider

    def load_into_gui(self):
        """
        Take values from self.settings and put them into the GUI.
        """

        self.show_colour_name_checkbox.setChecked(
            self.settings["overlay"]["colour_name"]
        )

        self.show_rgb_checkbox.setChecked(
            self.settings["overlay"]["rgb"]
        )

        self.show_hex_checkbox.setChecked(
            self.settings["overlay"]["hex"]
        )

        self.show_colour_thumbnail_checkbox.setChecked(
            self.settings["overlay"]["colour_thumbnail"]
        )

        self.show_nearest_colour_thumbnail_checkbox.setChecked(
            self.settings["overlay"]["nearest_colour_thumbnail"]
        )

        self.colour_system_dropdown.setCurrentText(
            self.settings["colour_system"]
        )

        self.distance_metric_dropdown.setCurrentText(
            self.settings["distance_metric"]
        )

    def apply_settings(self):
        """
        Take values from the GUI and put them into self.settings,
        then save them to JSON.
        """

        self.settings["overlay"]["colour_name"] = (
            self.show_colour_name_checkbox.isChecked()
        )

        self.settings["overlay"]["rgb"] = (
            self.show_rgb_checkbox.isChecked()
        )

        self.settings["overlay"]["hex"] = (
            self.show_hex_checkbox.isChecked()
        )

        self.settings["overlay"]["colour_thumbnail"] = (
            self.show_colour_thumbnail_checkbox.isChecked()
        )

        self.settings["overlay"]["nearest_colour_thumbnail"] = (
            self.show_nearest_colour_thumbnail_checkbox.isChecked()
        )

        self.settings["colour_system"] = (
            self.colour_system_dropdown.currentText()
        )

        self.settings["distance_metric"] = (
            self.distance_metric_dropdown.currentText()
        )

        self.settings["overlay"]["font_size"] = (
            self.font_size_spinbox.value()
        )

        self.settings["overlay"]["thumbnail_size"] = (
            self.thumbnail_size_spinbox.value()
        )

        self.save_settings()
        self.hotkey_bridge.update_settings_signal.emit()
        self.close()

    def quit_app(self):
        self.hotkey_bridge.quit_signal.emit()

        self.close()
