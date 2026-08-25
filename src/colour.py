import pyautogui

def get_cursor_pixel_colour():
    position = pyautogui.position()
    im = pyautogui.screenshot()
    rgb = im.getpixel(position)
    
    hex_colour = rgb_to_hex(rgb)
    return rgb, hex_colour

 
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