import os
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def parse_arguments():
    parser = argparse.ArgumentParser(description="Download images of animals.")
    parser.add_argument("animal", type=str, help="Name of the animal to download images for.")
    parser.add_argument("--n", type=int, default=None, help="Number of images to download.")
    parser.add_argument("--o", type=str, default="images", help="Folder to save downloaded images (default: 'images').")
    return parser.parse_args()


def search_images(animal, num_images):
    search_query = quote_plus(animal)
    url = f"https://www.google.com/search?q={search_query}&tbm=isch"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_tags = soup.find_all("img")
    image_urls = [tag['src'] for tag in image_tags]
    
    while num_images is None or len(image_urls) < num_images:
        last_image = image_tags[-1]['src']
        next_url = f"{url}&ijn={len(image_urls)}&start={len(image_urls)}"
        response = requests.get(next_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        image_tags = soup.find_all("img")
        new_image_urls = [tag['src'] for tag in image_tags]
        if new_image_urls[-1] == last_image:
            break
        image_urls.extend(new_image_urls)

    return image_urls[:num_images]


def download_images(image_urls, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            with open(os.path.join(output_folder, f"{i+1}.jpg"), 'wb') as f:
                f.write(response.content)
            print(f"Downloaded image {i+1}/{len(image_urls)}")
        except Exception as e:
            print(f"Error downloading image {i+1}: {str(e)}")


def main():
    args = parse_arguments()
    print(f"Searching for images of {args.animal}...")
    image_urls = search_images(args.animal, args.n)
    print(f"Downloading {len(image_urls)} images to {args.o}...")
    download_images(image_urls, args.o)
    print("Download complete.")


if __name__ == "__main__":
    main()














#     url = f"https://www.google.com/search?q={search_query}&tbm=isch"
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # Print the HTML content to inspect the structure
#     print(soup.prettify())
