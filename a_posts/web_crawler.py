import requests
from bs4 import BeautifulSoup

# from .forms import PostCreateForm

def flickr_crawler(url):
    website = requests.get(url)
    sourcecode = BeautifulSoup(website.text, 'html.parser')
    # print(sourcecode)
    find_image = sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
    image = find_image[0]['content']
    # print('image:', image)

    find_title = sourcecode.select('h1.photo-title')
    title = find_title[0].text.strip()
    # print('title:', title)

    find_artist = sourcecode.select('a.owner-name')
    artist = find_artist[0].text.strip()
    # print('artist:', artist)

    return image, title, artist