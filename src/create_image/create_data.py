from PIL import Image, ImageFile
import numpy as np
import colorsys
import requests
import json
from io import BytesIO
import threading
from collections import Counter
import pickle

from utils import check_color, colors

def get_image(url):
    response = requests.get(url)
    return BytesIO(response.content)

def get_dominant_color(image_data) -> tuple[str, ImageFile.ImageFile]:
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
        # Normalize RGB values
        norm_r, norm_g, norm_b = r / 255.0, g / 255.0, b / 255.0

        # Convert RGB to HSL
        h, l, s = colorsys.rgb_to_hls(norm_r, norm_g, norm_b)

        # Get color name
        color = check_color(h * 360, l * 100, s * 100)
        color_counter[color] += 1

    # Return most common color
    return color_counter.most_common(1)[0][0], image

def pokemon_thread(color_data, pokemon, url):
    print(pokemon)
    try:
        image_data = get_image(url)
        color, image = get_dominant_color(image_data)
        
        # Add the URL to the corresponding color list in color_data
        if color not in color_data:
            color_data[color] = []
        color_data[color].append(image)
        
    except Exception as e:
        print(e)

def main(data_source):
    
    with open(data_source, "r") as file:
        pokemon_links: dict = json.load(file)
    
    color_data = {}
    threads = []
    
    for pokemon, url in pokemon_links.items():
        t = threading.Thread(target=pokemon_thread, args=(color_data, pokemon, url))
        t.start()
        threads.append(t)
        
    for thread in threads:
        thread.join()
    
    # Sort color data 
    color_data = {key:color_data[key] for key in colors if key in color_data}
    
    with open('src/create_image/color_data/pokemon_color_data.pkl', 'wb') as file:
        pickle.dump(color_data, file)
            
if __name__ == "__main__":
    main()