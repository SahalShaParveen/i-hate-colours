import json
from colour_model import Colour
import colour as colour_science
import pyautogui


def get_nearest_colour(colour: Colour, distance_metric: str, colour_system: list[Colour]) -> Colour:
    nearest_colour, nearest_distance = None, None

    for c in colour_system:
        distance = get_distance(colour, c, distance_metric)
        if (nearest_distance is None) or (distance < nearest_distance):
            nearest_colour, nearest_distance = c, distance

    return nearest_colour


def load_colour_system(colour_system: str) -> list[Colour]:
    with open(f"data/{colour_system}-colours.json", "r") as file:
        colour_data = json.load(file)

    return [
        Colour.from_hex(hex_code, name)
        for hex_code, name in colour_data.items()
    ]


def get_distance(c1: Colour, c2: Colour, distance_metric: str) -> float:
    match distance_metric:

        case "RGB_Euclidean":
            return (
                (c1.rgb[0] - c2.rgb[0]) ** 2
                + (c1.rgb[1] - c2.rgb[1]) ** 2
                + (c1.rgb[2] - c2.rgb[2]) ** 2
            ) ** 0.5

        case "CIE76":
            return colour_science.delta_E(
                c1.lab,
                c2.lab,
                method="CIE 1976"
            )

        case "CIEDE2000":
            return colour_science.delta_E(
                c1.lab,
                c2.lab,
                method="CIE 2000"
            )

        case _:
            raise ValueError(
                f"Unknown distance metric: {distance_metric}"
            )


def get_cursor_pixel_colour() -> Colour:
    position = pyautogui.position()
    im = pyautogui.screenshot()

    return Colour(rgb=im.getpixel(position))
