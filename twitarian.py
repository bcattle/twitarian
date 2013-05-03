#!/usr/bin/env python
import logging, os, datetime, collections, csv, sys
from email.utils import parsedate_tz
from pytz import UTC, timezone
from twitter import *

logger = logging.getLogger(__name__)

## Settings

TWITTER_ACCOUNT = 'DalbergTweet'
LOCAL_TIME      = timezone('US/Eastern')
OUTPUT_FILE     = '%s - %s.csv' % (TWITTER_ACCOUNT,
                                   datetime.datetime.now(tz=LOCAL_TIME).strftime('%b %d, %Y %I.%M.%S %p'))
PULL_TWEETS     = False
PULL_MENTIONS   = True



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

if PULL_TWEETS:
    logger.info('Pulling tweets for account @%s' % TWITTER_ACCOUNT)
    raw_tweets = t.statuses.user_timeline(count=200, screen_name=TWITTER_ACCOUNT)
    logger.info('Done.')


class Tweet(object):
    def created_at_to_datetime(self, created_at):
        """
        Convert `created_at` to a `datetime`
        Returns tuple of (utc, local)
        """
        time_tuple = parsedate_tz(created_at)
        created_utc = datetime.datetime(*time_tuple[:6], tzinfo=UTC)
        created_local = created_utc.astimezone(LOCAL_TIME)
        return created_utc, created_local

    def __init__(self, raw_tweet):
        self.text               = raw_tweet['text']
        self.retweets           = raw_tweet['retweet_count']
        self.favorites          = raw_tweet['favorite_count']
        self.account_followers  = raw_tweet['user']['followers_count']
        self.created_utc, self.created_local = self.created_at_to_datetime(raw_tweet['created_at'])

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
    def __init__(self, raw_tweets, tweet_klass):
        self.tweets = []
        for raw_tweet in raw_tweets:
            self.tweets.append(tweet_klass(raw_tweet))
        self.tweets_by_day = None

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

if PULL_TWEETS:
    logger.info('Converting tweets to list')
    tweet_list = TweetList(raw_tweets, Tweet)
    logger.info('Done.')


## Pull mentions

if PULL_MENTIONS:

    logger.info('Pulling mentions...')


    # For some reason it's not giving us enough
    # Make the first call
    mention_results = t.search.tweets(count=100, q='@%s' % TWITTER_ACCOUNT)
    # Contains 'search_metadata' and 'statuses'
    raw_mentions = mention_results['statuses']

    DESIRED_MENTIONS = 200

    # Loop until we have enough
    while len(raw_mentions) < DESIRED_MENTIONS:
        last_id = raw_mentions[-1]['id']
        sys.stdout.write('^'); sys.stdout.flush()
        mention_results = t.search.tweets(count=100, q='@%s' % TWITTER_ACCOUNT, max_id=last_id - 1)
        new_mentions = mention_results['statuses']
        sys.stdout.write('\/(%d) ' % len(new_mentions)); sys.stdout.flush()
        print new_mentions[0]['id']
        if new_mentions:
            raw_mentions.extend(new_mentions)
        else:
            # If we didn't get any results, stop the loop
            break

    logger.info('Done. Got %d mentions' % len(raw_mentions))


class Mention(Tweet):
    def __init__(self, raw_mention):
        self.text               = raw_mention['text']
        self.retweets           = raw_mention['retweet_count']
        self.favorites          = raw_mention['favorite_count']
        self.source             = raw_mention['source']
        self.created_utc, self.created_local = self.created_at_to_datetime(raw_mention['created_at'])
        # User
        self.user_followers     = raw_mention['user']['followers_count']
        self.user_total_tweets  = raw_mention['user']['statuses_count']
        self.location           = raw_mention['user']['location']
        self.user_name          = raw_mention['user']['name']
        self.user_handle        = raw_mention['user']['screen_name']

    def __repr__(self):
        return '<Mention "%s">' % self.text[:40].encode('ascii', 'replace')

    def to_dict(self):
        return collections.OrderedDict([
            ('Date',         self.created_local.strftime('%m/%d/%y')),
            ('Time',         self.created_local.strftime('%I:%M:%S %p')),
            ('User',         u'@%s' % self.user_handle.encode('utf-8')),
            ('Text',         self.text.encode('utf-8')),
            ('Retweets',     self.retweets),
            ('Favorites',    self.favorites),
            ('Name',         self.user_name.encode('utf-8')),
            ('Location',     self.location.encode('utf-8')),
            ('Followers',    self.user_followers),
            ('Total tweets', self.user_total_tweets),
        ])

if PULL_MENTIONS:
    logger.info('Converting mentions to list')
    mention_list = TweetList(raw_mentions, Mention)
    logger.info('Done.')


## Write output file
if PULL_TWEETS or PULL_MENTIONS:
    with open(OUTPUT_FILE, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Tweets for @%s' % TWITTER_ACCOUNT])
        writer.writerow([])
        if PULL_TWEETS:
            writer.writerow(tweet_list[0].to_dict().keys())
            for tweet in tweet_list:
                writer.writerow(tweet.to_dict().values())

        writer.writerow([])
        writer.writerow([])

