from logging import exception
import urllib, json, praw
import time
import pdb
import re
import os
from configparser import ConfigParser
from praw.reddit import Submission

r = praw.Reddit('bot1')
subreddit = r.subreddit("bottestingxval")

for submission in subreddit.new(limit=5):
    print(submission.id)