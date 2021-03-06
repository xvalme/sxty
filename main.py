from logging import exception
import urllib, json, praw
import time
import pdb
import re
import os

from praw.reddit import Submission

r = praw.Reddit('bot1')

#Collecting variables
ignore_list=["sxtybot"]
time_to_sleep = 3
lenght = 60
subred = "bottestingxval"
subreddit = r.subreddit(subred)
type_of_message = "private" #One of “public”, “private”, “private_exposed”. 
message_title="Post removed"
message_wrong_lenght="a"
message_not_a_video="b"
removal_reason_1 = 0   #not a 60 second video
removal_reason_2 = 1   #not a video file

def delete_post(submission, id, reason):
    if id not in removed_posts:
        #Answering reason why was removed
        if reason == "wrong_lenght":
            reason = r.subreddit(str(subred)).mod.removal_reasons[removal_reason_1]
            submission = r.submission(id=submission.id)
            submission.mod.remove(reason_id=(reason.id))
            submission.mod.send_removal_message(message_wrong_lenght, title=message_title, type=type_of_message)
 
        if reason == "not_a_video":
            reason = r.subreddit(str(subred)).mod.removal_reasons[removal_reason_2]
            submission = r.submission(id=submission.id)
            submission.mod.remove(reason_id=(reason.id))
            submission.mod.send_removal_message(message_not_a_video, title=message_title, type=type_of_message)

        #Registering in database
        removed_posts.append(id)

        with open("removed_posts.txt", "w") as f:
            for post_id in removed_posts:
                f.write(post_id + "\n")

    return 0

def to_ignore(username):
    for x in ignore_list:
        if x == username:
            return 0
    return 2 

def main():
    try:
        print("Getting posts...")
        for submission in subreddit.new(limit=5):      #Gets the last submissions

            try:
                duration = (submission.media['reddit_video']['duration'])

                if duration != lenght and to_ignore(submission.author) == 2:

                    delete_post(submission, submission.id,"wrong_lenght")
                    print("Deleting a post because it did not have 60seconds.")

            except:
                print("Deleting a post because it was not a video.")
                delete_post(submission, submission.id, "not_a_video")

        time.sleep(time_to_sleep)
        print("Sleeping...")
        main()
    except:
        print("Could not connect to Reddit servers. Trying again in 10sec...")
        time.sleep(10)
        main()


#Starting database below
if not os.path.isfile("removed_posts.txt"):
    removed_posts = []
else:
    with open("removed_posts.txt", "r") as f:
        removed_posts = f.read()
        removed_posts = removed_posts.split("\n")
        removed_posts = list(filter(None, removed_posts))

#Start running
main()

