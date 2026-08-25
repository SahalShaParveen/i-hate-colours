import json 
from colour import hex_to_rgb

with open("data/css-colours.json", "r") as f:
    css_colours = json.load(f)


def get_css_name(hex_code, exact=False, distance_tolerance=10): 
    if exact: 
        return css_colours.get(hex_code)
    else: 
        rgb = hex_to_rgb(hex_code)

        nearest_dist, nearest_colour_hex = 10000000000, None

        for css_hex in css_colours: 
            css_rgb = hex_to_rgb(css_hex)
            distance = euclidean_distance(rgb, css_rgb)

            if distance < nearest_dist: 
                nearest_dist, nearest_colour_hex = distance, css_hex

        nearest_colour_name = css_colours.get(nearest_colour_hex)
        return nearest_colour_name


def euclidean_distance(rgb1, rgb2): 
    r1, g1, b1, = rgb1
    r2, g2, b2 = rgb2

    r = r2-r1; g = g2-g1; b = b2-b1;
    distance = (r**2 + g**2 + b**2)**(1/2)
    return distance 