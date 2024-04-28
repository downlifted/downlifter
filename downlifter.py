import requests
import json
import os
import mimetypes
from PIL import Image
import logging
import time
from tqdm import tqdm

# Base URL of the webpage to scrape
base_url = "https://ipfs.io/ipfs/QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/"

# Function to extract image link from metadata
def extract_image_link(metadata):
    if isinstance(metadata, dict) and 'image' in metadata:
        return metadata['image'].replace("ipfs://", "https://ipfs.io/ipfs/")
    return ""

# Function to get file extension from URL
def get_file_extension(url):
    content_type = requests.head(url).headers.get('content-type')
    return mimetypes.guess_extension(content_type) or ""

# Directories for images and metadata
images_folder = 'images'
metadata_folder = 'metadata'

# Create the folder structure if it doesn't exist
os.makedirs(images_folder, exist_ok=True)
os.makedirs(metadata_folder, exist_ok=True)

# Find the highest image number already processed
existing_images = [int(f.split('.')[0]) for f in os.listdir(images_folder) if f.endswith(('jpg', 'jpeg', 'png', 'gif'))]
last_processed_image = max(existing_images) if existing_images else 0

# Define the range for this instance
start_image_number = last_processed_image + 1
end_image_number = start_image_number + 2000000
total_images = end_image_number - start_image_number

# Fun prints for user engagement
print("🚀 Let's get scraping some cool images and metadata!")

# Iterate through each number within the specified range
for i in tqdm(range(start_image_number, end_image_number), total=total_images, desc="Scraping Progress"):
    try:
        page_url = f"{base_url}{i}"
        response = requests.get(page_url)
        if response.status_code == 200:
            metadata = json.loads(response.text)
            metadata_filename = os.path.join(metadata_folder, f"{i}.json")
            with open(metadata_filename, 'w') as file:
                json.dump(metadata, file, indent=4)

            image_link = extract_image_link(metadata)
            img_filename = os.path.join(images_folder, f"{i}{get_file_extension(image_link)}")
            if os.path.exists(img_filename):
                print(f"😜 Already got this one: {img_filename}. On to the next!")
                continue

            img_response = requests.get(image_link)
            if img_response.status_code == 200:
                with open(img_filename, 'wb') as file:
                    file.write(img_response.content)
                print(f"🎉 Woo-hoo! Snagged a new image: {img_filename}")

                img = Image.open(img_filename)
                img_resized = img.resize((1000, 1000))
                img_resized.save(img_filename)
            else:
                print(f"🤔 Hmm, couldn't download the image. Status: {img_response.status_code}")
        else:
            print(f"🧐 Uh-oh, couldn't get the page. Status: {response.status_code}")

        # Update the last processed image number
        with open('last_processed_image.txt', 'w') as file:
            file.write(str(i))
    except Exception as e:
        print(f"💥 Oops! Something went wrong: {e}")
        time.sleep(5)

print("👍 All done! Check out the images and metadata you've collected!")
