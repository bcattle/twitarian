# -*- coding: utf-8 -*-
import csv, collections
from email.utils import parsedate_tz
from pytz import UTC
from settings import *
from twitter import TwitterHTTPError


class BaseTweet(object):
    """
    Common object for our Twitter entities
    to inherit from
    """
    def __repr__(self):
        # return '<Tweet "%s">' % self.text[:40].encode('ascii', 'replace')
        return '<%s "%s">' % (self.__class__.__name__, self.text[:40].encode('ascii', 'replace'))


    def _created_at_to_datetime(self, created_at):
        """
        Convert `created_at` to a `datetime`
        Returns tuple of (utc, local)
        """
        time_tuple = parsedate_tz(created_at)
        created_utc = datetime.datetime(*time_tuple[:6], tzinfo=UTC)
        created_local = created_utc.astimezone(LOCAL_TIME)
        return created_utc, created_local


## Tweet object model

class Tweet(BaseTweet):
    def __init__(self, raw_tweet):
        self.text               = raw_tweet['text']
        self.retweets           = raw_tweet['retweet_count']
        self.favorites          = raw_tweet['favorite_count']
        self.account_followers  = raw_tweet['user']['followers_count']
        self.created_utc, self.created_local = self._created_at_to_datetime(raw_tweet['created_at'])

    def to_dict(self):
        return {
            'Date':      self.created_local.strftime('%m/%d/%y'),
            'Time':      self.created_local.strftime('%I:%M:%S %p'),
            'Text':      self.text.encode('utf-8'),
            'Retweets':  self.retweets,
            'Favorites': self.favorites,
        }


## Mention

class Mention(BaseTweet):
    def __init__(self, raw_mention):
        self.text               = raw_mention['text']
        self.retweets           = raw_mention['retweet_count']
        self.favorites          = raw_mention['favorite_count']
        self.source             = raw_mention['source']
        self.created_utc, self.created_local = self._created_at_to_datetime(raw_mention['created_at'])
        # User
        self.user_followers     = raw_mention['user']['followers_count']
        self.user_total_tweets  = raw_mention['user']['statuses_count']
        self.location           = raw_mention['user']['location']
        self.user_name          = raw_mention['user']['name']
        self.user_handle        = raw_mention['user']['screen_name']

    # def __repr__(self):
    #     return '<Mention "%s">' % self.text[:40].encode('ascii', 'replace')

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


## Results collection

class TweetList(list):
    """
    Results collection.
    Holds both tweets *and* mentions (which are also tweets)
    """

    def __init__(self, raw_tweets, tweet_klass):
        super(TweetList, self).__init__()
        for raw_tweet in raw_tweets:
            self.append(tweet_klass(raw_tweet))
        self.tweets_by_day = None

    def get_tweets_by_day(self):
        if not self.tweets_by_day:
            # Bucket the tweets by day
            self.tweets_by_day = collections.defaultdict(list)
            for tweet in self:
                key = tweet.created_local.strftime('%m/%d/%y')
                self.tweets_by_day[key].append(tweet)
        return self.tweets_by_day

    @staticmethod
    def pull_tweets_for_user(twitter, screenname, start_date=None):
        """
        This can pull tweets for *any user*, assuming their tweets are public
        """
        last_id = None
        raw_tweets = []
        while True:
            params = {
                'count': 200,
                'screen_name': screenname,
            }
            if last_id:
                params['max_id'] = last_id

            new_raw_tweets = twitter.statuses.user_timeline(**params)           # <----
            if not new_raw_tweets:
                break
            raw_tweets.extend(new_raw_tweets)

            if start_date:
                # Is the date of our last tweet < start date?
                last_tweet = Tweet(raw_tweets[-1])
                if last_tweet.created_local > start_date:
                    last_id = raw_tweets[-1]['id_str']
                else:
                    break
            else:
                break

        tweet_list = TweetList(raw_tweets, Tweet)
        return tweet_list


    @staticmethod
    def pull_mentions(twitter, start_date=None):
        """
        Only able to pull mentions for the **logged in user**
        """
        last_id = None
        raw_mentions = []
        while True:
            params = {
                'count': 200,
            }
            if last_id:
                params['max_id'] = last_id

            new_raw_mentions = twitter.statuses.mentions_timeline(**params)         # <----
            if not new_raw_mentions:
                break
            raw_mentions.extend(new_raw_mentions)

            if start_date:
                # Is the date of our last tweet < start date?
                last_tweet = Mention(raw_mentions[-1])
                if last_tweet.created_local > start_date:
                    last_id = raw_mentions[-1]['id_str']
                else:
                    break
            else:
                break

        mention_list = TweetList(raw_mentions, Mention)
        return mention_list


    @staticmethod
    def pull_manual_retweets(twitter, screenname, start_date=None):
        """
        Pulls "manual retweets" = those specified like "RT @comebody"
        The theory is that these aren't included in the official
        Twitter-returned "retweet count"
        """
        last_id = None
        raw_retweets = []
        while True:
            params = {
                'count': 200,
                'q': '"RT @%s"' % screenname
            }
            if last_id:
                params['max_id'] = last_id

            # This call returns the most recent tweets of mine that were re-tweeted,
            # without specifying who actually did the retweeting
            #new_raw_retweets = twitter.statuses.retweets_of_me(**params)

            try:
                new_raw_retweets = twitter.search.tweets(**params)['statuses']         # <----

                import ipdb
                ipdb.set_trace()

            except TwitterHTTPError, e:
                print 'Twitter returned an error, this probably means we were rate-limited.'
                print '\tThe error was: %s' % e.response_data
                print '\tcontinuing with the data we have...'
                break

            #import ipdb
            #ipdb.set_trace()

            if not new_raw_retweets:
                break
            raw_retweets.extend(new_raw_retweets)

            if start_date:
                # Is the date of our last tweet < start date?
                last_retweet = Mention(raw_retweets[-1])
                if last_retweet.created_local > start_date:
                    last_id = raw_retweets[-1]['id_str']
                else:
                    break
            else:
                break

        mention_list = TweetList(raw_retweets, Mention)
        return mention_list


    def save_output_file(self, file_object):
        """
        Saves to a flat CSV file, one table after the other
        """
        writer = csv.writer(file_object)
        writer.writerow(['Tweets/mentions for @%s' % TWITTER_ACCOUNT])
        writer.writerow([])
        writer.writerow(self[0].to_dict().keys())
        for tweet in self:
            writer.writerow(tweet.to_dict().values())
        writer.writerow([])
        writer.writerow([])


    def save_into_worksheet(self, ws):
        """
        Saves output data to am Excel workbook using OpenPyXL
        http://pythonhosted.org/openpyxl/tutorial.html

        See also ---
           http://scienceoss.com/write-excel-files-with-python-using-xlwt/
        """
        row_index = 0
        if len(self):
            # First, write the column headers
            for index, key in enumerate(self[0].to_dict().keys()):
                ws.cell(row = 0, column = index).value = key

            # Then, iterate through all the rows and write
            for row_index, row in enumerate(self):
                for col_index, cell_value in enumerate(row.to_dict().values()):
                    ws.cell(row = row_index + 1, column = col_index).value = cell_value

        return row_index
