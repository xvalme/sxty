from logging import exception
import urllib, json, praw
import time
import pdb
import re
import os
from configparser import ConfigParser
from praw.reddit import Submission
from datetime import datetime

r = praw.Reddit('bot1')

#Collecting variables
while True:

    try:
        parser = ConfigParser()
        parser.read('config.cfg', encoding='utf-8')

        subred = (parser.get("config", "subred"))
        subred = subred.replace('"', '')
        subreddit = r.subreddit(subred)

        ignore_list=(parser.get("config", "ignore_list"))
        ignore_list = ignore_list.split(',')

        time_to_sleep = int(parser.get("config", "time_to_sleep"))
        lenght = (parser.get("config", "lenght"))
        type_of_message = str(parser.get("config", "type_of_message"))
        type_of_message = type_of_message.replace('"', '')
        message_title=(parser.get("config", "message_title"))
        message_wrong_lenght=(parser.get("config", "message_wrong_lenght"))
        message_not_a_video=(parser.get("config", "message_not_a_video"))
        removal_reason_1 = (int(parser.get("config", "removal_reason_1"))- 1)
        removal_reason_2 = (int(parser.get("config", "removal_reason_2"))- 1) 
        break

    except:
        print("There was an error while getting data from config file. Correct any mistakes!")
        print("Trying again in 10 seconds.")
        time.sleep(10)

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
        for submission in subreddit.new(limit=10):      #Gets the last submissions
            try:
                duration = (submission.media['reddit_video']['duration'])
 
                if duration != lenght and to_ignore(submission.author) == 2:

                    delete_post(submission, submission.id,"wrong_lenght")
                    print("Deleting a post because it did not have 60seconds.")

            except:
                if to_ignore(submission.author)==2:
                    print("Deleting a post because it was not a video.")
                    delete_post(submission, submission.id, "not_a_video")

        #General clean up
        now = datetime.now()
        if now.strftime("%M") == "00":
            print("New hour! Time to do a general protective clean-up.")
            for submission in subreddit.hot(limit=1000):  

                try:
                    duration = (submission.media['reddit_video']['duration'])
    
                    if duration != lenght and to_ignore(submission.author) == 2:

                        delete_post(submission, submission.id,"wrong_lenght")
                        print("Deleting a post because it did not have 60seconds.")

                except:
                    if to_ignore(submission.author)==2:
                        print("Deleting a post because it was not a video.")
                        delete_post(submission, submission.id, "not_a_video")
            print("Sucessfull Clean-up.")
        
        print("Sleeping...")
        time.sleep(time_to_sleep)
        main()
    except:
        print("Could not contact to Reddit! Returning again in 10 seconds.")
        print("If you tried to stop me you have to do it 2 times like super fast!")
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
print("Beep. Boop. Bot is booting...")
print("B0T by u/michaelangelito. Visit https//xval.me!")
time.sleep(1)
print("")
print("Lets go! To stop me press CTRL+C 2 times really fast! It will give an error the 1st time.")
main()
