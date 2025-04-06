import requests
from PIL import Image
from io import BytesIO
import threading
import json
import math

def get_pokemon_links() -> dict:
    with open("src/pokemon_sprites.json", "r") as file:
        return json.load(file)
    
def get_pokemon_hues() -> dict:
    with open("src/pokemon_hsl_data.json", "r") as file:
        return json.load(file)
    
def get_image(url, pokemon, color_data):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        images[pokemon] = {"image": img, "color_data": color_data}
    except Exception as e:
        print(e)
    
def create_image(links_dict):
    global images
    images = {}
    threads = []
    
    for pokemon, color_data in get_pokemon_hues().items():
        print(pokemon)
        t = threading.Thread(target=get_image, args=(links_dict[pokemon], pokemon, color_data))
        t.start()
        threads.append(t)
        
    for thread in threads:
        thread.join()

    sorted_data = {k: v for k, v in sorted(images.items(), key=lambda item: item[1]['color_data']['hue'])}

    # Determine grid size
    count = len(sorted_data)
    cols = 37
    rows = math.ceil(count / cols)

    # Create blank canvas
    grid_image = Image.new('RGBA', (cols * 96, rows * 96), (255, 255, 255, 1))# Grid config
    count = len(sorted_data)
    cols = math.ceil(math.sqrt(count))
    rows = math.ceil(count / cols)

    # Get image size
    img_width, img_height = 96, 96

    # Overlap settings
    overlap_x = int(img_width * 0.5) 
    overlap_y = int(img_height * 0.5)

    # Calculate canvas size
    canvas_width = img_width + (cols - 1) * (img_width - overlap_x)
    canvas_height = img_height + (rows - 1) * (img_height - overlap_y)
    grid_image = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255, 0))

    # Paste images into grid
    for index, pokemon in enumerate(sorted_data):
        print(index)

        img_data = sorted_data[pokemon]['image']
        row = index // cols
        col = index % cols
        x = col * (img_width - overlap_x)
        y = row * (img_height - overlap_y)

        temp = Image.new("RGBA", grid_image.size, (255, 255, 255, 0))
        temp.paste(img_data, (x, y), img_data)
        grid_image = Image.alpha_composite(grid_image, temp)

    # Save to file
    grid_image.save("image_grid.png")
    print("Saved image_grid.png!")
    
if __name__ == "__main__":
    create_image(get_pokemon_links())
