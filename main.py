from logging import exception
import urllib, json, praw
import time
import pdb
import re
import os

r = praw.Reddit('bot1')

#Collecting variables
ignore_list=["sxtybot"]
time_to_sleep = 5
subreddit = r.subreddit("bottesting")

def delete_post(id, reason):
    if id not in removed_posts:
        #Answering and deleting post

        #Registering in database
        removed_posts.append(id)

        with open("removed_posts.txt", "w") as f:
            for post_id in removed_posts:
                f.write(post_id + "\n")

    else:    #Already commented
        return 0

def to_ignore(username):
    for x in ignore_list:
        if x == username:
            return 0
    return 2 

def main():
    for submission in subreddit.new(limit=5):      #Gets the last submissions
        try:
            duration = (submission.media['reddit_video']['duration'])

            if duration != 60 and to_ignore(submission.author) == 2:

                delete_post(submission.id,"wrong_lenght")

            else:
                print("Approved")
                #Bot approves

        except:
            delete_post(submission.id, "not_a_video")

    time.sleep(time_to_sleep)
    main()


#Starting database below
if not os.path.isfile("removed_posts.txt"):
    removed_posts = []
else:
    with open("removed_posts.txt", "r") as f:
        removed_posts = f.read()
        removed_posts = posts_replied_to.split("\n")
        removed_posts = list(filter(None, posts_replied_to))

#Start running
main()

