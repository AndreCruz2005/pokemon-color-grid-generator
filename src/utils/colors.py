colors = {
    "black": {"hue": [0, 361], "saturation": [0, 101], "lightness": [0, 10]},
    "grey": {"hue": [0, 361], "saturation": [0, 10], "lightness": [10, 90]},
    "white": {"hue": [0, 361], "saturation": [0, 101], "lightness": [90, 101]},
    "red": {"hue": [0, 30], "saturation": [0, 101], "lightness": [0, 101]},
    "orange": {"hue": [30, 50], "saturation": [0, 101], "lightness": [0, 101]},
    "yellow": {"hue": [50, 75], "saturation": [0, 101], "lightness": [0, 101]},
    "green": {"hue": [75, 160], "saturation": [0, 101], "lightness": [0, 101]},
    "blue": {"hue": [160, 250], "saturation": [0, 101], "lightness": [0, 101]},
    "violet": {"hue": [250, 285], "saturation": [0, 101], "lightness": [0, 101]},
    "pink": {"hue": [285, 345], "saturation": [0, 101], "lightness": [0, 101]},
    "magenta": {"hue": [345, 361], "saturation": [0, 101], "lightness": [0, 101]},
}

def check_color(h: float, s: float, l: float) -> str:
    for color in colors:
        data = colors[color]
        
        hue_check = data["hue"][0] <= h < data["hue"][1]
        saturation_check = data["saturation"][0] <= s < data["saturation"][1]
        lightness_check = data["lightness"][0] <= l < data["lightness"][1]
        
        if hue_check and saturation_check and lightness_check:
            return color
        
    return "none"