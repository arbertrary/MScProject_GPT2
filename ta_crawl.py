import requests
import re
import os
from bs4 import BeautifulSoup
import pymongo
import time
import random

DIRS = ["ta-text", "ta-sitemaps", "ta-mongodb", "ta-logs"]
TOP_SITEMAP = "https://www.team-andro.com/sitemap-google.xml"


def crawl_ta():
    # Pymongo stuff
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient["ta-data"]
    coll = db["ta-posts"]

    # Get all sitemaps
    andro_sitemaps = list(map(lambda l: os.path.join("ta-sitemaps", l), os.listdir("ta-sitemaps")))
    random.shuffle(andro_sitemaps)
    total_sitemaps = len(andro_sitemaps)

    # Create a logfile that remembers which sitemaps have already been completed
    sitemap_logfile = "ta-logs/sitemap-logs"
    open(sitemap_logfile, "a").close()

    # Iterate over sitemaps
    for si, sitemap in enumerate(andro_sitemaps):

        # Skip if sitemap has been completed
        with open(sitemap_logfile, "r+") as log:
            lines = log.readlines()
            if sitemap + "\n" in lines:
                print("Skipping sitemap " + sitemap)
                continue

        # Processing sitemap
        print("Reading: " + sitemap + " (" + str(si) + " of " + str(total_sitemaps) + ")")
        try:
            pages = read_sitemap_xml(sitemap)
        except FileNotFoundError:
            continue

        # Iterate over page links in sitemap
        total = len(pages)
        for i, page in enumerate(pages):
            if "phpBB3" not in page:
                continue

            if i % 20 == 0:
                time.sleep(2)

            # Progress
            if i % 1000 == 0:
                print(str(i * 100 / total) + "% (" + str(i) + "/" + str(total) + " done)")

            # Error handling or writing to mongodb
            metadata = get_forum_page(page)
            if isinstance(metadata, list):
                x = coll.insert_many(metadata)
            elif isinstance(metadata, str):
                print(metadata)
                raise AttributeError("Error at sitemap: " + sitemap)
            else:
                continue

        # Add sitemap to logfile if completed
        with open(sitemap_logfile, "a") as log:
            log.write(sitemap + "\n")


# Get all page links from a xml file sitemap
def read_sitemap_xml(xml_path):
    with open(xml_path) as xml:
        sitemap = BeautifulSoup(xml.read(), "lxml-xml")
        links = list(map(lambda x: x.getText(), sitemap.find_all("loc")))
    return links


# Get all page links from the sitemap online
def read_sitemap(url):
    try:
        top_sitemap = requests.get(url)
    except requests.exceptions.ConnectionError:
        print(url)
        return

    sitemap = BeautifulSoup(top_sitemap.text, "lxml-xml")
    links = list(map(lambda x: x.getText(), sitemap.find_all("loc")))

    return links


# Read a single forum page
def get_forum_page(url):
    try:
        text = requests.get(url).text
    except Exception as e:
        return "### Error at: " + url + "\n" + str(e)

    soup = BeautifulSoup(text, "html.parser")

    m = re.search(r"-(t\d+)(-\d+)*.html", url)
    if m:
        thread_id = m.group(1)
        if m.group(2):
            thread_id += m.group(2)
    else:
        thread_id = "t0000"
    try:
        posts = soup.find_all("div", id=re.compile(r"p\d+"))
        navlinks = soup.find("ul", class_="linklist navlinks").find_all("a")
        navlinks = [x.getText().replace(" ", "-") for x in navlinks]
        navlinks.append(thread_id)
        path = os.path.join("ta-text", *navlinks)
    except Exception as e:
        return "### Error at: " + url + "\n" + str(e)

    if not os.path.exists(path):
        os.makedirs(path)
    else:
        return

    meta_list = []

    # Iterate over al posts in a page
    for post in posts:
        try:
            post_id = post.get("id")
        except Exception as e:
            return "### Could not find post id at" + url + "\n" + str(e)

        filepath = os.path.join(path, post_id)
        if os.path.exists(filepath):
            continue
        try:
            post_url = url + "#" + post_id
            text = post.find("div", class_="content").getText()
            user_block = post.find("a", href=re.compile(r"team-andro.com/my/.+-u\d+"))
            author_string = post.find("p", class_="author").getText()
        except Exception as e:
            return "### Error at: " + url + "\n" + str(e)

        author_regex = r"von\s(.+)\s.\s(\d{2}\s\w{3}\s\d{4})\s(.+)\s"
        pattern = re.compile(author_regex)
        m = re.search(pattern, author_string)
        if m:
            author_name = m.group(1)
            post_date = m.group(2)
            post_time = m.group(3)
        else:
            author_name = "John Doe"
            post_date = "1 Jan 2000"
            post_time = "00:00"

        if user_block:
            user_url = user_block.get("href")
        else:
            user_url = "user_deleted"

        with open(filepath, "w") as post_textfile:
            post_textfile.write(text)

        # Available Info:
        metadata = {"thread_url": url, "thread_id": thread_id, "post_id": post_id, "post_url": post_url,
                    "post_date": post_date, "post_time": post_time, "author_name": author_name,
                    "user_url": user_url, "file_path": filepath, "text": text}
        meta_list.append(metadata)

    return meta_list


# Download all sitemaps to folder
def get_andro_sitemaps_as_files():
    top_sitemaps = read_sitemap(TOP_SITEMAP)
    sitemap_dir = "ta-sitemaps/"
    if not os.path.exists(sitemap_dir):
        os.makedirs(sitemap_dir)

    for sm in top_sitemaps:
        time.sleep(2)
        print(sm)
        filename = sitemap_dir + sm.split("/")[-1]
        text = requests.get(sm).text
        if not os.path.exists(filename):
            with open(filename, "w") as file:
                file.write(str(text))


if __name__ == '__main__':
    get_andro_sitemaps_as_files()
    for ta_dir in DIRS:
        if not os.path.exists(ta_dir):
            os.makedirs(ta_dir)
    crawl_ta()
