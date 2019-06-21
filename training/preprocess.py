import os
from pathlib import Path
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
from tqdm import tqdm
import random

home = os.path.abspath("../")


def tokenize():
    super_corpus = os.path.join(home, "super_corpus")
    # super_corpus = os.path.join(home, "test_corpus")
    logpath = os.path.join(super_corpus, "log.txt")
    files = os.listdir(super_corpus)
    random.shuffle(files)
    t = tqdm(files)
    for file in t:
        t.set_postfix(file=file)
        with open(logpath, "r") as f:
            text = f.readlines()
            if file + "\n" in text:
                print("skipping " + file)
                continue

        if file.startswith("taaq"):
            filepath = os.path.join(super_corpus, file)
            newfile = filepath.replace(file, "tok" + file)
            text = ""
            with open(filepath, "r") as f:
                for line in f:
                    # in case of original files cut from the mongoexported .csv;
                    # Requires using "rb" in open(filepath, "rb)
                    # line = line.decode("utf-8", "ignore")

                    # Remove the quotation marks around the post
                    # post_regex = re.compile(r"\"(.*)\"\n")

                    # match = re.match(post_regex, line)
                    # if match:
                    #     line = match.group(1)
                    print(line)
                    line = re.sub(" +", " ", line)
                    line = sent_tokenize(line)
                    line = "\n".join(line)
                    text += line + "\n"

            with open(newfile, "w") as f:
                f.write(text)

            # with open(logpath, "a") as f:
            #     f.write(file + "\n")


def super_vocabulary():
    super_corpus = os.path.join(home, "super_corpus")
    # super_corpus = "text/"
    # vocab = []

    c = Counter()
    print(c)
    for i, file in enumerate(os.listdir(super_corpus)):
        print(file)
        filepath = os.path.join(super_corpus, file)
        with open(filepath, "r") as f:
            text = word_tokenize(f.read().replace("\n", ""))
            # text = f.read().replace("\n", "").split(" ")
            c += Counter(text)
            print(c.most_common(10))

    with open("super_vocabulary.txt", "a") as newf:
        vocab = "\n".join(sorted(c, key=c.get, reverse=True))
        newf.write(vocab)


def replace(path):
    text = ""
    counter = 0
    with open(path, "rb") as infile:
        for line in infile:
            line = line.decode("utf-8", "ignore")

            # post_regex = re.compile(r"\"(.*)\"\n")

            # match = re.match(post_regex, line)
            # if match:
            #     line = match.group(1)
            line = "\n".join(sent_tokenize(line))

            if line.endswith("\n"):
                text += line
            else:
                text += line + "\n"

    with open(path + "2.txt", "w") as outfile:
        outfile.write(text)


if __name__ == '__main__':
    tokenize()
    # super_vocabulary()
