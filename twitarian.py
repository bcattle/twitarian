#!/usr/bin/env python
import logging, os, datetime, collections, csv
from email.utils import parsedate_tz
from pytz import UTC, timezone
from twitter import *

logger = logging.getLogger(__name__)

## Settings

TWITTER_ACCOUNT = 'DalbergTweet'
LOCAL_TIME = timezone('US/Eastern')
OUTPUT_FILE = '%s - %s.csv' % (TWITTER_ACCOUNT,
                                    datetime.datetime.now(tz=LOCAL_TIME).strftime('%b %d, %Y %I.%M.%S %p'))


## Authentication

CONSUMER_KEY = 'du4W5e4hbaTJqGLX5U270g'
CONSUMER_SECRET = 'wL0OvhRoIB5RrXLh3FvrEFt9e1PFsCkDVXurNx7YQc'

# Do the auth
CREDENTIALS_FILE = '.twitter_credentials'
if not os.path.exists(CREDENTIALS_FILE):
    logger.info('No credentials file found, getting user login')
    oauth_dance('Twidarian', CONSUMER_KEY, CONSUMER_SECRET,
                CREDENTIALS_FILE)

oauth_token, oauth_secret = read_token_file(CREDENTIALS_FILE)
logger.info('Credentials found.')


## Connect

t = Twitter(api_version=1.1,
            auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))


## Pull tweets

logger.info('Pulling tweets for account @%s' % TWITTER_ACCOUNT)
raw_tweets = t.statuses.user_timeline(count=200, screen_name=TWITTER_ACCOUNT)
logger.info('Done.')


class Tweet(object):
    def __init__(self, raw_tweet):
        self.text               = raw_tweet['text']
        self.retweets           = raw_tweet['retweet_count']
        self.favorites          = raw_tweet['favorite_count']
        self.account_followers  = raw_tweet['user']['followers_count']
        # Convert `created_at` to a `datetime`
        time_tuple = parsedate_tz(raw_tweet['created_at'])
        self.created_utc = datetime.datetime(*time_tuple[:6], tzinfo=UTC)
        self.created_local = self.created_utc.astimezone(LOCAL_TIME)

    def __repr__(self):
        return '<Tweet "%s">' % self.text[:40].encode('ascii', 'replace')

    def to_dict(self):
        return {
            'Date':      self.created_local.strftime('%m/%d/%y'),
            'Time':      self.created_local.strftime('%I:%M:%S %p'),
            'Text':      self.text.encode('utf-8'),
            'Retweets':  self.retweets,
            'Favorites': self.favorites,
        }


class TweetList(object):
    tweets = []
    tweets_by_day = None

    def __init__(self, raw_tweets):
        for raw_tweet in raw_tweets:
            self.tweets.append(Tweet(raw_tweet))

    def __len__(self):
        return len(self.tweets)

    def __getitem__(self, item):
        return self.tweets[item]

    def get_tweets_by_day(self):
        if not self.tweets_by_day:
            # Bucket the tweets by day
            self.tweets_by_day = collections.defaultdict(list)
            for tweet in self.tweets:
                key = tweet.created_local.strftime('%m/%d/%y')
                self.tweets_by_day[key].append(tweet)
        return self.tweets_by_day

logger.info('Converting tweets to list')
tweet_list = TweetList(raw_tweets)
logger.info('Done.')

## Write output file
with open(OUTPUT_FILE, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(tweet_list[0].to_dict().keys())
    for tweet in tweet_list:
        writer.writerow(tweet.to_dict().values())


## Pull mentions

# mentions = t.statuses.mentions_timeline(id=TWITTER_ACCOUNT)

