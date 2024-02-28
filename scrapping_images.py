import argparse
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def parse_arguments():
    parser = argparse.ArgumentParser(description="Download images of animals.")
    parser.add_argument("animal", type=str, help="Name of the animal to download images for.")
    parser.add_argument("--num-images", type=int, default=5, help="Number of images to download (default: 5).")
    parser.add_argument("--output-folder", type=str, default="images", help="Folder to save downloaded images (default: 'images').")
    return parser.parse_args()

