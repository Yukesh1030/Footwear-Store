import os
from PIL import Image

def convert_to_webp(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith(".png") or filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
            filepath = os.path.join(directory, filename)
            webp_filepath = os.path.join(directory, os.path.splitext(filename)[0] + ".webp")
            
            # Skip if webp already exists
            if os.path.exists(webp_filepath):
                continue
                
            img = Image.open(filepath)
            
            # Ensure it's in RGB mode if saving as WebP
            if img.mode != "RGB" and img.mode != "RGBA":
                img = img.convert("RGBA")
                
            # Resize image to make it smaller if it's too large (original images are 8-9MB)
            # Let's resize them to max 1920x1080 while keeping aspect ratio
            img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
                
            target_min = 70 * 1024
            target_max = 90 * 1024
            
            # Binary search for quality
            min_q = 1
            max_q = 100
            best_q = 80
            
            for _ in range(7): # 7 iterations of binary search should be enough
                q = (min_q + max_q) // 2
                img.save(webp_filepath, "webp", quality=q)
                size = os.path.getsize(webp_filepath)
                
                if target_min <= size <= target_max:
                    best_q = q
                    break
                elif size < target_min:
                    min_q = q + 1
                    best_q = q
                else:
                    max_q = q - 1
            
            # Final save
            img.save(webp_filepath, "webp", quality=best_q)
            print(f"Converted {filename} to WebP. Size: {os.path.getsize(webp_filepath)/1024:.2f} KB")

if __name__ == "__main__":
    convert_to_webp(r"D:\yukesh\projects\Footwear Store\assets")
