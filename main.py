from logging import exception
import urllib, json, praw
import time

r = praw.Reddit('bot1')

#Collecting variables
ignore_list=["sxtybot"]
time_to_sleep = 5
subreddit = r.subreddit("bottesting")

def delete_post(reason):
    print("Deleted")
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

                delete_post("wrong_lenght")

            else:
                print("Approved")
                #Bot approves

        except:
            delete_post("not_a_video")

    time.sleep(time_to_sleep)
    main()





main()

