import requests
from PIL import Image
from io import BytesIO
import threading
import math
import pickle
from utils import colors

with open("src/create_image/color_data/pokemon_color_data.pkl", "rb") as file:
    data = pickle.load(file)

def create_image(images):    
    # Get image size
    img_width, img_height = 96, 96
    
    # Overlap settings
    overlap_x = int(img_width * 0.5) 
    overlap_y = int(img_height * 0.5)
    
    # Create blank canvas
    count = sum(len(images[color]) for color in images)
    cols = math.ceil(math.sqrt(count))
    rows = math.ceil(count / cols) 
    canvas_width = img_width + (cols - 1) * (img_width - overlap_x)
    canvas_height = img_height + (rows - 1) * (img_height - overlap_y)
    grid_image = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255, 0))
    
    # Paste images into grid
    index = 0
    for color in images:
        for img_data in images[color]:
            row = index // cols
            col = index % cols
            x = col * (img_width - overlap_x)
            y = row * (img_height - overlap_y)
            index += 1

            temp = Image.new("RGBA", grid_image.size, (255, 255, 255, 0))
            temp.paste(img_data, (x, y), img_data)
            grid_image = Image.alpha_composite(grid_image, temp)

    # Save to file
    grid_image.save("image_grid.png")
    print("Saved image_grid.png!")
    
if __name__ == "__main__":
    create_image(data)
