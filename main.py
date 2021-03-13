import scrape
import parse


def main():
    words_in_titles, words_in_comments = scrape.scrape_subreddit()
    shorter_list = parse.filter_by_length(words_in_titles, words_in_comments)
    print(shorter_list)

if __name__ == "__main__":
    main()

