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

false_positives = ['YOLO', 'HOLD', 'APE', 'MEME', 'ETF', 'FOMO', ]

def scrape_wsb_by_date(year, month, day):

    start_epoch = int(dt.datetime(year, month, day).timestamp())
    # generator object needed, we're looking at thousands or maybe tens of thousands of posts
    api_submissions_generator = api.search_submissions(after=start_epoch,
                                                       subreddit='wallstreetbets',
                                                       filter=['url', 'author', 'title', 'subreddit'])
    return api_submissions_generator

def parse_submission_data(api_submissions_generator):

    # finds items in title that either start with '$' or are uppercase and have 3 or 4 digits
    title_submission_list = []
    for submission in api_submissions_generator:
        words = submission.title.split()
        possible_stocks = list(set(filter(lambda word: word.startswith('$') or word.isupper() and 3 <= len(word) <= 4, words)))
        if len(possible_stocks) > 0:
            entry = {
                'possible_symbol': possible_stocks,
                'title': submission.title,
                'url': submission.url
            }
            title_submission_list.append(entry)
    return title_submission_list

def scrape_wsb_comments_by_date(year, month, day, max_responses):

    start_epoch = int(dt.datetime(year, month, day).timestamp())
    # generator object needed, we're looking at thousands or maybe tens of thousands of posts
    api_comments_generator = api.search_comments(after=start_epoch,
                                                 subreddit='wallstreetbets',
                                                 filter=['permalink', 'author', 'body', 'score', 'subreddit'])

    max_response_cache = max_responses
    comment_cache = []
    # finds items in title that either start with '$' or are uppercase and have 3 or 4 digits
    for comment in api_comments_generator:
        comment_cache.append(comment)
        if len(comment_cache) >= max_response_cache:
            break
        # If you really want to: pick up where we left off to get the rest of the results.
    if False:
        for comment in api_submissions_generator:
            cache.append(comment)
    return comment_cache


def parse_comment_data(comment_cache):
    comment_submission_list = []
    for comment in comment_cache:
        if comment.score > 0:
            words = comment.body.split()
            possible_stocks = list(set(filter(lambda word: word not in false_positives and word.startswith('$') or
                                                           word not in false_positives and word.isupper() and 3 <= len(word) <= 4, words)))
            if len(possible_stocks) > 0:
                entry = {
                    'possible_symbol': possible_stocks,
                    'body': comment.body,
                    'url': comment.permalink,
                    'subreddit': comment.subreddit
                }
                comment_submission_list.append(entry)
    return comment_submission_list


title_cache = scrape_wsb_by_date(2021, 3, 14)
title_list = parse_submission_data(title_cache)
comment_cache = scrape_wsb_comments_by_date(2021, 3, 15, 40)
comment_list = parse_comment_data(comment_cache)


