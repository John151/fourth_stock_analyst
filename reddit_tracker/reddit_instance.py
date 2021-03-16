#import praw
from database.config import CLIENT_ID, SECRET
# praw and psaw are both reddit api wrapper libraries, I'm not sure which is better for this project yet


# reddit object for praw library
def create_instance():
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=SECRET,
                         user_agent="praw practice")

    # with reddit instance bound to variable, create subreddit
    subreddit = reddit.subreddit('wallstreetbets')
    return subreddit
