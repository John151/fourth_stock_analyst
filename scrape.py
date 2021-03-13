from reddit_instance import create_instance
'''for reference:
 youtuber sentdex has a lot of useful information, much of this was
 found on his channel https://www.youtube.com/watch?v=KX2jvnQ3u60'''

def scrape_subreddit():
    print('banana')
    words_in_titles = []
    words_in_comments = []

    subreddit = create_instance()

    for submission in subreddit.hot(limit=3):
    #     if not submission.stickied:
    #         title = submission.title
    #         title_split = title.split()
    #         words_in_titles.append(title_split)

        submission.comments.replace_more(limit=10) # praw documentation tutorials https://praw.readthedocs.io/en/latest/tutorials/comments.html#extracting-comments-with-praw
        for comment in submission.comments.list():
            body = comment.body
            print(body)
    #         body_split = body.split()
    #         print(body_split)
    #         words_in_comments.append(body_split)
    # print(words_in_comments)
#    return words_in_titles, words_in_comments


scrape_subreddit()

