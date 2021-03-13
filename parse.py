

def filter_by_length(words_in_titles, words_in_comments):
    # if word is too long or too short, it isn't a stock ticker
    # there are some false positives
    new_list = []
    for title_list in words_in_titles:
        for word in title_list:
            if 2 <= len(word) <= 4:
                new_list.append(word)
    for comment_list in words_in_comments:
        for word in comment_list:
            if 2 <= len(word) <=4:
                new_list.append(word)

    return new_list