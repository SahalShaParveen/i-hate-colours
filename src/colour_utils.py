import json
from colour_model import Colour
import colour as colour_science
import pyautogui
import numpy as np


def load_colour_system(colour_system: str) -> list[Colour]:
    with open(f"data/colour_systems/{colour_system}.json", "r") as file:
        colour_data = json.load(file)

    return [
        Colour.from_hex(hex_code, name)
        for hex_code, name in colour_data.items()
    ]


def get_nearest_colour(colour: Colour, distance_metric: str, colour_system: list[Colour]) -> Colour:
    match distance_metric:
        case "RGB_Euclidean":
            reference_rgbs = np.array([
                c.rgb
                for c in colour_system
            ])

            pixel_rgb = np.array(colour.rgb)

            distances = np.sqrt(
                np.sum(
                    (reference_rgbs - pixel_rgb) ** 2,
                    axis=1
                )
            )

        case "CIE76":
            reference_labs = np.array([
                c.lab
                for c in colour_system
            ])

            distances = colour_science.delta_E(
                colour.lab,
                reference_labs,
                method="CIE 1976"
            )

        case "CIEDE2000":
            reference_labs = np.array([
                c.lab
                for c in colour_system
            ])

            distances = colour_science.delta_E(
                colour.lab,
                reference_labs,
                method="CIE 2000"
            )

        case _:
            raise ValueError(
                f"Unknown distance metric: {distance_metric}"
            )

    nearest_index = np.argmin(distances)

    return colour_system[nearest_index]


def get_cursor_pixel_colour() -> Colour:
    position = pyautogui.position()
    im = pyautogui.screenshot()

    return Colour(rgb=im.getpixel(position))
