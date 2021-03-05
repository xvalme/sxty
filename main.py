import urllib, json, praw

r = praw.Reddit('bot1')
subreddit = r.subreddit("bottesting")

def collect_variables():
    return 0

def delete_post():
    return 0

def main():
    for submission in subreddit.new(limit=50):

        try:
            duration = (submission.media['reddit_video']['duration'])

            if duration !== 60:

                #Need to check if author is meant to ignore 
                if submission.approved_by == None:

                    delete_post()

            else:

        except: #Not a video so will be deleted



main()

