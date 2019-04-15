import requests
from bs4 import BeautifulSoup

url = "https://www.team-andro.com/phpBB3/smartphone-handy-kaufberatung-und-talk-t295707.html"

# get list of urls from sitemap here
# https://www.team-andro.com/sitemap-google.xml
# Download sitemap xmls?




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