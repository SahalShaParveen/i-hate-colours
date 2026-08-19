import json 

with open("data/css-colours.json", "r") as f:
    css_colours = json.load(f)


def get_css_name(hex_code): 
    return css_colours.get(hex_code)