FROM python:3
ADD preprocess.py /
RUN pip3 install nltk tqdm
RUN python3 -m nltk.downloader -d /usr/local/share/nltk_data punkt
CMD ["python3", "./preprocess.py"]
