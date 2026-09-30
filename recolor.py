from PIL import Image
import os

img_path = r"D:\yukesh\projects\Footwear Store\assets\Brand-logo.webp"

try:
    img = Image.open(img_path).convert("RGBA")
    data = img.getdata()
    
    new_data = []
    # Target color: #b08d57 -> R: 176, G: 141, B: 87
    for item in data:
        # If the pixel is not completely transparent, change its color to the target color
        # Maintain the original alpha value
        if item[3] > 0:
            new_data.append((176, 141, 87, item[3]))
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    img.save(img_path, "WEBP")
    print("Logo updated successfully to #b08d57.")
except Exception as e:
    print(f"Error: {e}")
