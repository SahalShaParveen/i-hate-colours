import json
import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QComboBox,
    QPushButton,
)


CONFIG_FILE = "data/settings.json"


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")

        self.settings = self.load_settings()

        # Widgets

        self.show_colour_name_checkbox = QCheckBox("Show colour name")
        self.show_rgb_checkbox = QCheckBox("Show RGB values")
        self.show_hex_checkbox = QCheckBox("Show Hex code")

        self.colour_system_dropdown = QComboBox()
        self.colour_system_dropdown.addItems(self.settings["colour_system_list"])

        self.distance_metric_dropdown = QComboBox()
        self.distance_metric_dropdown.addItems(self.settings["distance_metric_list"])

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_settings)

        self.quit_app_button = QPushButton("Quit App")
        self.quit_app_button.clicked.connect(self.quit_app)

        # Layout

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Settings"))

        layout.addWidget(self.show_colour_name_checkbox)
        layout.addWidget(self.show_rgb_checkbox)
        layout.addWidget(self.show_hex_checkbox)

        layout.addWidget(QLabel("Colour naming system:"))
        layout.addWidget(self.colour_system_dropdown)

        layout.addWidget(QLabel("Colour distance:"))
        layout.addWidget(self.distance_metric_dropdown)

        layout.addSpacing(10)

        button_layout = QHBoxLayout()
 
        button_layout.addWidget(self.quit_app_button)
        button_layout.addStretch()
        button_layout.addWidget(self.apply_button)
  

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Populate GUI using JSON values
        self.load_into_gui()


    # JSON

    def load_settings(self):
        try:
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)

        except FileNotFoundError:
            # Default settings if the file doesn't exist
            return { 
            "hotkey":"ctrl + shift + z", 
            "quit_hotkey":"ctrl + shift + q",
            "colour_system_list":["css"],
            "distance_metric_list":["euclidean"],
            "overlay_text":{
                "show_colour_name":True,  
                "colour_system":"CSS",
                "distance_metric": "Eucidean",
                "show_rgb":True, 
                "show_hex":True
            },
            "delay_ms":10
            }
        

    def save_settings(self):
        with open(CONFIG_FILE, "w") as file:
            json.dump(self.settings, file, indent=4)


    def load_into_gui(self):
        """
        Take values from self.settings and put them into the GUI.
        """

        self.show_colour_name_checkbox.setChecked(
            self.settings["overlay_text"]["show_colour_name"]
        )

        self.show_rgb_checkbox.setChecked(
            self.settings["overlay_text"]["show_rgb"]
        )

        self.show_hex_checkbox.setChecked(
            self.settings["overlay_text"]["show_hex"]
        )

        self.colour_system_dropdown.setCurrentText(
            self.settings["overlay_text"]["colour_system"]
        )

        self.distance_metric_dropdown.setCurrentText(
            self.settings["overlay_text"]["distance_metric"]
        )


    def apply_settings(self):
        """
        Take values from the GUI and put them into self.settings,
        then save them to JSON.
        """

        self.settings["overlay_text"]["show_colour_name"] = (
            self.show_colour_name_checkbox.isChecked()
        )

        self.settings["overlay_text"]["show_rgb"] = (
            self.show_rgb_checkbox.isChecked()
        )

        self.settings["overlay_text"]["show_hex"] = (
            self.show_hex_checkbox.isChecked()
        )

        self.settings["overlay_text"]["colour_system"] = (
            self.colour_system_dropdown.currentText()
        )

        self.settings["overlay_text"]["distance_metric"] = (
            self.distance_metric_dropdown.currentText()
        )

        self.save_settings()
        self.close()
        print("Settings saved!")

    def quit_app(self):
        self.close() 