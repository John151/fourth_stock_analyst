import datetime as dt
from psaw import PushshiftAPI
'''for reference:
 youtuber sentdex has a lot of useful information
 found on his channel https://www.youtube.com/watch?v=KX2jvnQ3u60
mostly Part Time Larry's Tracking WallStreetBets Stocks with Python, Reddit API, and SQL
https://www.youtube.com/watch?v=CJAdCLZaISw&t=309s
'''

api = PushshiftAPI()

# TODO accept user input, year month day hardcoded for now
year = 2021
month = 3
day = 14
max_responses = 10

def scrape_wsb_by_date(year, month, day):

    start_epoch = int(dt.datetime(year, month, day).timestamp())
    # generator object needed, we're looking at thousands or maybe tens of thousands of posts
    api_submissions_generator = api.search_submissions(after=start_epoch,
                                                       subreddit='wallstreetbets',
                                                       filter=['url', 'author', 'title', 'subreddit'])
    return api_submissions_generator

def parse_submission_data(api_submissions_generator):

    # finds items in title that either start with '$' or are uppercase and have 3 or 4 digits
    for submission in api_submissions_generator:
        words = submission.title.split()
        possible_stocks = list(set(filter(lambda word: word.startswith('$') or word.isupper() and 3 <= len(word) <= 4, words)))
        if len(possible_stocks) > 0:
            possible_symbol = possible_stocks
            title = submission.title
            url = submission.url

def scrape_wsb_comments_by_date(year, month, day, max_responses):

    start_epoch = int(dt.datetime(year, month, day).timestamp())
    # generator object needed, we're looking at thousands or maybe tens of thousands of posts
    api_comments_generator = api.search_comments(after=start_epoch,
                                                 subreddit='wallstreetbets',
                                                 filter=['url', 'author', 'body', 'subreddit'])

    max_response_cache = max_responses
    comment_cache = []
    # finds items in title that either start with '$' or are uppercase and have 3 or 4 digits
    for comment in api_submissions_generator:
        cache.append(comment)
        if len(cache) >= max_response_cache:
            break
        # If you really want to: pick up where we left off to get the rest of the results.
    if False:
        for comment in api_submissions_generator:
            cache.append(c)
    return comment_cache

def parse_comment_data():


    words = comment.title.split()
    possible_stocks = list(set(filter(lambda word: word.startswith('$') or word.isupper() and 3 <= len(word) <= 4, words)))
    if len(possible_stocks) > 0:
        possible_symbol = possible_stocks
        title = submission.title
        url = submission.url

scrape_wsb_by_date(2021, 3, 14)