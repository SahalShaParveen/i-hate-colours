import pyautogui
import colour 
import json

def get_cursor_pixel_colour():
    position = pyautogui.position()
    im = pyautogui.screenshot()
    rgb = im.getpixel(position)
    
    hex_colour = rgb_to_hex(rgb)
    return rgb, hex_colour


def get_distance(c1_rgb, c2_lab, distance_metric):
    match distance_metric:
        case "CIE76":
            lab1 = rgb_to_lab(c1_rgb)
            lab2 = c2_lab
            return colour.delta_E(lab1, lab2, method="CIE 1976")

        case "CIEDE2000":
            lab1 = rgb_to_lab(c1_rgb)
            lab2 = c2_lab
            return colour.delta_E(lab1, lab2, method="CIE 2000")

        # case "OKLab":
        #     oklab1 = rgb_to_oklab(rgb1)
        #     oklab2 = rgb_to_oklab(rgb2)
        #     return euclidean_distance(oklab1, oklab2)

        case _:
            raise ValueError(f"Unknown distance metric: {distance_metric}")


def convert_colour_system_to_lab(colour_system):
    with open(f"data/{colour_system}.json", "r") as file:
        colour_system_dict = json.load(file)

    return {
        tuple(rgb_to_lab(hex_to_rgb(colour))): value
        for colour, value in colour_system_dict.items()
    }

        
def rgb_to_lab(rgb): 
    rgb_normalised = [x / 255 for x in rgb]

    xyz = colour.sRGB_to_XYZ(rgb_normalised)
    lab = colour.XYZ_to_Lab(xyz)
    return lab
    
 
def rgb_to_hex(rgb):
    r, g, b = rgb 
    hex_code = f"#{r:02x}{g:02x}{b:02x}"
    return hex_code


def hex_to_rgb(hex_code): 
    r_hex = hex_code[1] + hex_code[2]
    g_hex = hex_code[3] + hex_code[4]
    b_hex = hex_code[5] + hex_code[6]

    rgb_colour = (int(r_hex, base=16), int(g_hex, base=16), int(b_hex, base=16))
    return rgb_colour