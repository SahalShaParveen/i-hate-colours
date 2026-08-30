import json 
from colour_utils import hex_to_rgb, get_distance, convert_colour_system_to_lab

with open("data/css-colours.json", "r") as f:
    css_colours = json.load(f)


css_lab = convert_colour_system_to_lab("css-colours")

def get_css_name(hex_code, distance_metric): 
    if distance_metric == "exact": 
        return css_colours.get(hex_code)    
    else: 
        rgb = hex_to_rgb(hex_code)

        nearest_dist, nearest_colour = 10000000000, None


        for c in css_lab: 
            distance = get_distance(rgb, c, distance_metric)

            if distance < nearest_dist: 
                nearest_dist, nearest_colour = distance, c

        nearest_colour_name = css_lab.get(nearest_colour)
        return nearest_colour_name