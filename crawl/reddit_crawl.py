import praw
import pymongo
import os
from tqdm import tqdm
import time

# Need refresh token somewhere

reddit = praw.Reddit(client_id="yvmTRQmbs91y8A", client_secret="musranLO2f-D3dskNePZ9hTyw0A",
                     user_agent="ger_reddit_crawl")

subreddits = ["de", "de_iama", "rocketbeans", "austria"]
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["reddit_data"]
# mycol = mydb["reddit_comments"]

# mylist = []

for subreddit in subreddits:
    path = os.path.join("reddit_text", subreddit)

    for submission in tqdm(reddit.subreddit(subreddit).hot()):
        time.sleep(1)
        thread_title = submission.title
        thread_content = submission.selftext
        downvotes = submission.downs
        upvotes = submission.ups
        submission_id = submission.id
        submission_author = submission.author
        submission_permalink = submission.permalink
        submission_url = submission.url

        thread_path = os.path.join(path, submission_id)
        if not os.path.exists(thread_path):
            os.makedirs(thread_path)

        submission.comments.replace_more(limit=None)
        test = vars(submission)
        # for v in test:
        #     print(v)
        #     print(test.get(v))
        #     print("####")

        for comment in submission.comments.list():
            comm = {"body": comment.body}
            text = comment.body
            comment_permalink = comment.permalink
            comment_id = comment.id
            # print(comment_permalink)

            filepath = os.path.join(thread_path, comment_id)
            if not os.path.exists(filepath):
                with open(filepath, "w") as comment_textfile:
                    comment_textfile.write(text)

# x = mydb.mycol.insert_many(mylist)
# print(x.inserted_ids)
# myresult = mycol.find().limit(5)

# for r in myresult:
#     print(r)
