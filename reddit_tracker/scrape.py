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


false_positives = ['YOLO', 'HOLD', 'APE', 'MEME', 'ETF', 'FOMO']


def scrape_wsb_by_date(year, month, day):

    start_epoch = int(dt.datetime(year, month, day).timestamp())
    # generator object needed, we're looking at thousands or maybe tens of thousands of posts
    api_submissions_generator = api.search_submissions(after=start_epoch,
                                                       subreddit='wallstreetbets',
                                                       filter=['url', 'author', 'title', 'subreddit'])
    print('Generator created.')
    return api_submissions_generator


def parse_submission_data(api_submissions_generator, stocks):
    # finds items in title that either start with '$' or are uppercase and have 3 or 4 digits
    print('Parsing submission data...')
    title_submission_list = []
    count_for_fun = 1
    for submission in api_submissions_generator:
        words = submission.title.split()
        possible_stocks = list(set(filter(lambda word: word.startswith('$') or word.isupper() and 3 <= len(word) <= 4, words)))
        if len(possible_stocks) > 0:
            for stock in possible_stocks:
                if not stock.startswith('$'):
                    stock = '$' + stock
                if stock in stocks:
                    post_time = dt.datetime.fromtimestamp(submission.created_utc).isoformat()
                    entry = {
                        'submission_type': 'Post',
                        'date_time': post_time,
                        'id': stocks[stock],
                        'body': submission.title,
                        'url': submission.url,
                        'subreddit': submission.subreddit
                    }
                    title_submission_list.append(entry)
                    print(f'{count_for_fun} title entries added...')
                    count_for_fun = count_for_fun + 1
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
    return comment_cache


def parse_comment_data(comment_cache, stocks):
    comment_submission_list = []
    print('Parsing comment data...')
    count_for_fun = 1
    for comment in comment_cache:
        if comment.score > 0:
            words = comment.body.split()
            possible_stocks = list(set(filter(lambda word: word not in false_positives and word.startswith('$') or
                                                           word not in false_positives and word.isupper() and 3 <= len(word) <= 4, words)))
            if len(possible_stocks) > 0:
                for stock in possible_stocks:
                    if not stock.startswith('$'):
                        stock = '$' + stock
                    if stock in stocks:
                        post_time = str(dt.datetime.fromtimestamp(comment.created_utc).isoformat())
                        entry = {
                            'submission_type': 'Comment',
                            'date_time': post_time,
                            'id': stocks[stock],
                            'body': comment.body,
                            'url': comment.permalink,
                            'subreddit': comment.subreddit
                        }
                        comment_submission_list.append(entry)
                        print(f'{count_for_fun} comment entries added...')
                        count_for_fun = count_for_fun + 1
    return comment_submission_list


