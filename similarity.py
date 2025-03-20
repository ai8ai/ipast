import os
import shutil
import imagehash
from PIL import Image
from collections import defaultdict

def get_image_hash(image_path):
    try:
        with Image.open(image_path) as img:
            return imagehash.phash(img)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def find_similar_images(folder):
    image_hashes = defaultdict(list)
    image_files = [f for f in os.listdir(folder) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))]
    
    for image_file in image_files:
        image_path = os.path.join(folder, image_file)
        img_hash = get_image_hash(image_path)
        if img_hash is not None:
            image_hashes[img_hash].append(image_file)
    
    return image_hashes

def move_similar_images(folder, image_hashes):
    ss_folder = os.path.join(folder, "ss")
    os.makedirs(ss_folder, exist_ok=True)
    
    for img_hash, files in image_hashes.items():
        if len(files) > 1:
            print(f"Similar images (hash: {img_hash}):")
            for file in files:
                print(f"  - {file}")
                shutil.move(os.path.join(folder, file), os.path.join(ss_folder, file))
    print("All similar images moved to 'ss' folder.")

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python id.py foldername")
        return
    
    folder = sys.argv[1]
    if not os.path.isdir(folder):
        print("Invalid folder path.")
        return
    
    image_hashes = find_similar_images(folder)
    move_similar_images(folder, image_hashes)

if __name__ == "__main__":
    main()
