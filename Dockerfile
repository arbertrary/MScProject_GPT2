FROM python:3
ADD forum_crawl.py /
RUN pip install beautifulsoup4 lxml tqdm requests pymongo
CMD ["python3", "./ta_crawl.py"]
