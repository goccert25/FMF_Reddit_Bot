import praw
import re
from config import user_agent, client_id, client_secret, username, password

def main():
    reddit = praw.Reddit(user_agent=user_agent,
                         client_id=client_id, client_secret=client_secret,
                         username=username, password=password)

    subreddit = reddit.subreddit('test')
    amazonPatternString = "amazon"
    productPatternString = "dp/([A-Za-z0-9]+)"

    amazonRegex = re.compile(amazonPatternString)
    productRegex = re.compile(productPatternString)

    for submission in subreddit.stream.submissions():
        process_submission(submission, amazonRegex, productRegex)


def redditCommentFormatter(product):
    comment = "Beep Boop. I detected an Amazon link! Here is the [camelcamelcamel link](https://camelcamelcamel.com/product/" + product + ")"
    return comment


def process_submission(submission, amazonRegex, productRegex):

    found_amazon = amazonRegex.search(submission.url)

    if (found_amazon):

        print("amazon found!")
        print(submission.url)
        product = productRegex.search(submission.url)

        if (product):

            submission.comments.replace_more(limit=0)
            for top_level_comment in submission.comments:
                if (top_level_comment.author == username):
                    #If bot already posted here, just skip and don't post here
                    print("Found myself not posting here")
                    return

            productString = product.group(1)
            comment = redditCommentFormatter(productString)
            print(comment)
            submission.reply(comment)


if __name__ == '__main__':
    main()
