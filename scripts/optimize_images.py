import os
from PIL import Image
import sys

def optimize_images(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                file_name, _ = os.path.splitext(file_path)
                webp_path = file_name + ".webp"
                
                try:
                    with Image.open(file_path) as img:
                        img.save(webp_path, "WEBP", quality=80)
                        print(f"Converted: {file} -> {os.path.basename(webp_path)}")
                except Exception as e:
                    print(f"Failed to convert {file}: {e}")

if __name__ == "__main__":
    images_dir = os.path.join(os.getcwd(), "images")
    if os.path.exists(images_dir):
        optimize_images(images_dir)
    else:
        print("Images directory not found.")
