import requests
from bs4 import BeautifulSoup
import itertools


# get list of urls from sitemap here
# https://www.team-andro.com/sitemap-google.xml
# Download sitemap xmls?

def read_sitemap(url):
    top_sitemap = requests.get(url)
    # print(url)
    sitemap = BeautifulSoup(top_sitemap.text, "lxml-xml")
    sitemaps = list(map(lambda x: x.getText(), sitemap.find_all("loc")))

    return sitemaps


def get_all_andro_pages():
    top_sitemaps = read_sitemap("https://www.team-andro.com/sitemap-google.xml")
    all_sites = itertools.chain([read_sitemap(url) for url in top_sitemaps])


def get_andro_sitemaps_as_files():
    top_sitemaps = read_sitemap("https://www.team-andro.com/sitemap-google.xml")

    for sm in top_sitemaps:
        print(sm)
        filename = "andro_sitemaps/" + sm.split("/")[-1]
        text = requests.get(sm).text
        with open(filename, "w") as file:
            file.write(str(text))


def crawl_andro():
    url = "https://www.team-andro.com/phpBB3/smartphone-handy-kaufberatung-und-talk-t295707.html"
    page = requests.get(url)

    text = page.text

    # print(text)

    soup = BeautifulSoup(text, "html.parser")

    # print(soup.head)
    # print(soup.title)

    # For TA forum
    posts = soup.find_all("div", ["post bg1", "post bg2"])

    print(posts[0].find("div", class_="content").getText())

    # For TA news


if __name__ == '__main__':
# get_andro_sitemaps_as_files()
