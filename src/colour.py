import pyautogui

def get_cursor_pixel_colour():
    position = pyautogui.position()
    im = pyautogui.screenshot()

    rgb = im.getpixel(position)
    hex_colour = rgb_to_hex(rgb)

    return rgb, hex_colour


def rgb_to_hex(r, g, b): 
    hex = f"#{r:02x}{g:02x}{b:02x}"
    return hex
