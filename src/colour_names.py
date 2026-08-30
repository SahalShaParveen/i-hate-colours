import json 
from colour_utils import hex_to_rgb, get_distance

with open("data/css-colours.json", "r") as f:
    css_colours = json.load(f)


def get_css_name(hex_code, distance_metric): 
    if distance_metric == "exact": 
        return css_colours.get(hex_code)    
    else: 
        rgb = hex_to_rgb(hex_code)

        nearest_dist, nearest_colour_hex = 10000000000, None

        for css_hex in css_colours: 
            css_rgb = hex_to_rgb(css_hex)
            distance = get_distance(rgb, css_rgb, distance_metric)

            if distance < nearest_dist: 
                nearest_dist, nearest_colour_hex = distance, css_hex

        nearest_colour_name = css_colours.get(nearest_colour_hex)
        return nearest_colour_name