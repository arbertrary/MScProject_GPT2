import requests
import re
import os
from bs4 import BeautifulSoup
import pymongo
from tqdm import tqdm


# get list of urls from sitemap here
# https://www.team-andro.com/sitemap-google.xml

def crawl_ta():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["ta_data"]
    mycol = mydb["ta_posts"]

    top_sitemap = "https://www.team-andro.com/sitemap-google.xml"
    andro_sitemaps = read_sitemap(top_sitemap)

    for sitemap in andro_sitemaps:
        pages = read_sitemap(sitemap)
        for page in tqdm(pages):
            metadata = get_forum_page(page)

            if metadata:
                x = mydb.mycol.insert(metadata)


def read_sitemap(url):
    top_sitemap = requests.get(url)
    sitemap = BeautifulSoup(top_sitemap.text, "lxml-xml")
    sitemaps = list(map(lambda x: x.getText(), sitemap.find_all("loc")))

    return sitemaps


def get_forum_page(url):
    if "phpBB3" in url:
        text = requests.get(url).text
        soup = BeautifulSoup(text, "html.parser")

        m = re.search(r"-(t\d+)", url)
        if m:
            thread_id = m.group(1)
        else:
            thread_id = "t0000"

        posts = soup.find_all("div", id=re.compile(r"p\d+"))
        navlinks = soup.find("ul", class_="linklist navlinks").find_all("a")
        navlinks = [x.getText().replace(" ", "_") for x in navlinks]
        navlinks.append(thread_id)
        path = os.path.join("andro_text", *navlinks)

        if not os.path.exists(path):
            os.makedirs(path)

        for post in posts:
            post_id = post.get("id")
            text = post.find("div", class_="content").getText()
            user_block = post.find("a", href=re.compile(r"team-andro.com/my/.+-u\d+"))
            author_string = post.find("p", class_="author").getText()
            author_regex = r"von\s(.+)\s.\s(\d{2}\s\w{3}\s\d{4})\s(.+)"
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

            filepath = os.path.join(path, post_id)
            if not os.path.exists(filepath):
                with open(filepath, "w") as post_textfile:
                    post_textfile.write(text)

            # Available Info:
            metadata = {"thread_url": url, "thread_id": thread_id, "post_id": post_id, "post_date": post_date,
                        "post_time": post_time,
                        "author_name": author_name, "user_url": user_url, "file_path": filepath}
            print(metadata)
            return metadata


# def read_sitemap_xml():
#     for sitemap in os.listdir("andro_sitemaps"):
#
#         path = os.path.join("andro_sitemaps", sitemap)
#         print(path)
#
#         with open(path) as xml:
#             sitemap = BeautifulSoup(xml.read(), "lxml-xml")
#             links = list(map(lambda x: x.getText(), sitemap.find_all("loc")))
#
#             for link in tqdm(links):
#                 get_forum_page(link)

# def get_all_andro_pages():
#     top_sitemaps = read_sitemap("https://www.team-andro.com/sitemap-google.xml")
#     all_sites = itertools.chain([read_sitemap(url) for url in top_sitemaps])


# def get_andro_sitemaps_as_files():
#     top_sitemaps = read_sitemap("https://www.team-andro.com/sitemap-google.xml")
#
#     for sm in top_sitemaps:
#         print(sm)
#         filename = "andro_sitemaps/" + sm.split("/")[-1]
#         text = requests.get(sm).text
#         with open(filename, "w") as file:
#             file.write(str(text))


# def create_folders():
#     for file in os.listdir("andro_sitemaps"):
#         name = os.path.splitext(file)[0]
#         print(name)
#         os.mkdir(os.path.join("andro_text", name))


if __name__ == '__main__':
    crawl_ta()
    # author_string = "von Jan- » 08 Dez 2006 23:48"
    # author_regex = r"von\s(.+)\s.\s(\d{2}\s\w{3}\s\d{4})\s(.+)"
    # pattern = re.compile(author_regex)
    # m = re.search(pattern, author_string)
    # print(m)
    # for group in m.groups():
    #     print(group)
