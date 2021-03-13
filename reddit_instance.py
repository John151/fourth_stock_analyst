import praw
import psaw
from keys import CLIENT_ID, SECRET
# credentials

# reddit object for praw library
def create_instance():
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=SECRET,
                         user_agent="praw practice")

    # with reddit instance bound to variable, create subreddit
    subreddit = reddit.subreddit('wallstreetbets')
    return subreddit
