import praw
import pymongo

reddit = praw.Reddit(client_id="yvmTRQmbs91y8A", client_secret="musranLO2f-D3dskNePZ9hTyw0A",
                     user_agent="ger_reddit_crawl")

subreddits = ["de", "de_iama", "rocketbeans", "austria"]

#  mongod --dbpath ./db/ -- start server/daemon
# mongo -- opens shell at localhost:27017
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["comments"]

mylist = []
# for submission in reddit.subreddit("de").hot(limit=2):
#     submission.comments.replace_more(limit=None)
#     for comment in submission.comments.list():
#         comm = {"body": comment.body}
#         # comm = vars(comment)
#         # print(comm)
#         # print(" ")
#         mylist.append(comm)
#         # print(vars(comment))
#         # mycol.insert_one(comm)

# x = mydb.mycol.insert_many(mylist)
# print(x.inserted_ids)
myresult = mycol.find().limit(5)

for r in myresult:
    print(r)