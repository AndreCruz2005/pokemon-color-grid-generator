from PIL import Image
import numpy as np
import colorsys
import requests
import json
from io import BytesIO
import threading
from collections import Counter

def get_pokemon_links() -> dict:
    with open("src/pokemon_sprites.json", "r") as file:
        return json.load(file)

def get_image(url):
    response = requests.get(url)
    return BytesIO(response.content)

def get_dominant_color(image_data):
    image = Image.open(image_data)
    image = image.convert("RGBA")
    pixels = np.array(image)
    pixels = pixels.reshape(-1, 4)

    # Remove fully transparent pixels
    pixels = pixels[pixels[:, 3] > 0]

    # Extract RGB values
    rgb_pixels = pixels[:, :3]
    
        # Count colors
    color_counter = Counter()

    for r, g, b in rgb_pixels:
        if r < 55 and g < 55 and b < 55:  # Direct RGB check for extreme colors
            color_counter["black"] += 1
            continue
        
        elif r > 220 and g > 220 and b > 220: 
            color_counter["white"] += 1
            continue
        
        # Normalize RGB values
        norm_r, norm_g, norm_b = r / 255.0, g / 255.0, b / 255.0

        # Convert RGB to HSL
        h, l, s = colorsys.rgb_to_hls(norm_r, norm_g, norm_b)

        # Get color name
        color = get_color(h * 360)
        color_counter[color] += 1

    # Return most common color
    return color_counter.most_common(1)[0][0]

def get_color(hue):
    if hue < 30 or hue >= 345:
        return "red"
    if 30 <= hue < 50: 
        return "orange"
    if 50 <= hue < 75: 
        return "yellow"
    if 75 <= hue < 160: 
        return "green"
    if 160 <= hue < 250: 
        return "blue"
    if 250 <= hue < 285: 
        return "violet"
    if 285 <= hue < 345: 
        return "pink"

def pokemon_thread(pokemon, url):
    print(pokemon)
    try:
        image_data = get_image(url)
        color = get_dominant_color(image_data)
        
        # Add the URL to the corresponding color list in color_data
        if color not in color_data:
            color_data[color] = []
        color_data[color].append(url)
        
    except Exception as e:
        print(e)

def main():
    global color_data
    color_data = {}
    threads = []
    
    for pokemon, url in get_pokemon_links().items():
        t = threading.Thread(target=pokemon_thread, args=(pokemon, url))
        t.start()
        threads.append(t)
        
    for thread in threads:
        thread.join()
        
    with open('src/pokemon_color_data.json', 'w') as file:
        json.dump(color_data, file, indent=4)
    
if __name__ == "__main__":
    main()