#!/usr/bin/env python
import logging, os
from twitter import Twitter, OAuth, oauth_dance, read_token_file
from models import TweetList
from settings import *

logger = logging.getLogger(__name__)


# Auth
if not os.path.exists(CREDENTIALS_FILE):
    oauth_dance('Twidarian', CONSUMER_KEY, CONSUMER_SECRET,
                CREDENTIALS_FILE)
oauth_token, oauth_secret = read_token_file(CREDENTIALS_FILE)


# Connect
t = Twitter(api_version=1.1,
            auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))


# Pull tweets and mentions
tweets = TweetList.pull_tweets_for_user(t, TWITTER_ACCOUNT, START_DATE)
mentions = TweetList.pull_mentions(t, START_DATE)


# Save to a file
with open(OUTPUT_FILE, 'w') as csvfile:
    tweets.save_output_file(csvfile)
    mentions.save_output_file(csvfile)


# Calculate unique mentioners
#mention_usernames = []
#mention_user_by_username = {}
#for mention in mentions:
#    mention_usernames.append(mention.user_handle)
#    mention_user_by_username[mention.user_handle] = {
#        'followers':
#        'total_tweets':
#    }
#    self.user_followers     = raw_mention['user']['followers_count']
#    self.user_total_tweets  = raw_mention['user']['statuses_count']
#    self.location           = raw_mention['user']['location']
#    self.user_name          = raw_mention['user']['name']
#    self.user_handle
#
#mentioner_counter = collections.Counter()

