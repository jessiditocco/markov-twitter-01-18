"""A Markov chain generator that can tweet random messages."""

import os
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Take list of files. Open them, read them, and return one long string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Take dictionary of Markov chains; return random text."""

    charecter_count = 0
    key = choice(chains.keys())
    words = [key[0], key[1]]
    charecter_count += len(key[0]) + len(key[1]) + 1
    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text).
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])

        charecter_count += len(word) + 1
        
        if charecter_count >= 140:
            break


        words.append(word)
        key = (key[1], word)

    text = " ".join(words)
    print len(text)
    return text

# def tweet(chains):
#     """Create a tweet and send it to the Internet."""

#     # Use Python os.environ to get at environmental variables
#     # Note: you must run `source secrets.sh` before running this file
#     # to make sure these environmental variables are set.


#     api = twitter.Api(
#         consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
#         consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
#         access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
#         access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

#     # this will print info about credentials to make sure that they are correct
#     # print api.VerifyCredentials()

#     # sends a tweet

#     status = api.PostUpdate(make_text(chains))

#     # prints to terminal the tweet you have sent
#     # print status.text


## this version of tweet(chains) adds a loop asking user if they want to tweet again
def tweet(chains):
    """Create a tweet and send it to the Internet."""

    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.


    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    # this will print info about credentials to make sure that they are correct
    print api.VerifyCredentials()

    # sends a tweet

    status = api.PostUpdate(make_text(chains))

    # prints to terminal the tweet you have sent
    print status.text

    #### FIX WHILE LOOP
    while True:
        retweet = raw_input("Enter to tweet again [q to quit] ")
        retweet = retweet.lower()
        tweet(chains)
        if retweet == "q":
            break


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)


# Your task is to write a new function tweet, that will take chains as input
# tweet(chains)

tweet(chains)

# while True:
#     retweet = raw_input("Enter to tweet again [q to quit] ")
#     retweet = retweet.lower()
#     tweet(chains)
#     if retweet == "q":
#         break
