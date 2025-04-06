from PIL import Image
import numpy as np
import colorsys
import requests
import json
from io import BytesIO
import threading

def get_pokemon_links() -> dict:
    with open("src/pokemon_sprites.json", "r") as file:
        return json.load(file)

def get_image(url):
    response = requests.get(url)
    return BytesIO(response.content)

def get_HSL_average(image_data):
    image = Image.open(image_data)
    
    image = image.convert("RGBA")
    pixels = np.array(image)
    pixels = pixels.reshape(-1, 4)

    # Remove fully transparent pixels
    pixels = pixels[pixels[:, 3] > 0]

    # Extract RGB and normalize
    avg_r = np.median(pixels[:, 0]) / 255.0
    avg_g = np.median(pixels[:, 1]) / 255.0
    avg_b = np.median(pixels[:, 2]) / 255.0

    
    # Convert RGB to HSL
    h, l, s = colorsys.rgb_to_hls(avg_r, avg_g, avg_b)
    
    # Return as HSL (rearranging from HLS to HSL)
    return {
        'hue': h * 360,  # Scale to 0-360 degrees
        'saturation': s * 100,  # Scale to 0-100%
        'lightness': l * 100  # Scale to 0-100%
    }

def pokemon_thread(pokemon, url):
    print(pokemon)
    try:
        image_data = get_image(url)
        hsl_avg = get_HSL_average(image_data)
        hsl_data[pokemon] = hsl_avg
    except Exception as e:
        print(e)

def main():
    global hsl_data
    hsl_data = {}
    threads = []
    
    for pokemon, url in get_pokemon_links().items():
        t = threading.Thread(target=pokemon_thread, args=(pokemon, url))
        t.start()
        threads.append(t)
        
    for thread in threads:
        thread.join()
        
    with open('src/pokemon_hsl_data.json', 'w') as file:
        json.dump(hsl_data, file)
    
if __name__ == "__main__":
    main()