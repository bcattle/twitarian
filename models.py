# -*- coding: utf-8 -*-
import collections
import datetime
from email.utils import parsedate_tz
from pytz import UTC
from dateutil.tz import tzlocal


class BaseTweet(object):
    """
    Common object for our Twitter entities
    to inherit from
    """
    def __repr__(self):
        # return '<Tweet "%s">' % self.text[:40].encode('ascii', 'replace')
        return '<%s "%s">' % (self.__class__.__name__,
                              self.text[:40].encode('ascii', 'replace'))

    def _created_at_to_datetime(self, created_at):
        """
        Convert `created_at` to a `datetime`
        Returns tuple of (utc, local)
        """
        time_tuple = parsedate_tz(created_at)
        created_utc = datetime.datetime(*time_tuple[:6], tzinfo=UTC)
        created_local = created_utc.astimezone(tz=tzlocal())
        return created_utc, created_local


## Tweet object model

class Tweet(BaseTweet):
    def __init__(self, raw_tweet):
        self.text               = raw_tweet['text']
        self.retweets           = raw_tweet['retweet_count']
        self.favorites          = raw_tweet['favorite_count']
        self.account_followers  = raw_tweet['user']['followers_count']
        self.created_utc, self.created_local = \
            self._created_at_to_datetime(raw_tweet['created_at'])

    def to_dict(self):
        return collections.OrderedDict([
            ('Date',      self.created_local.strftime('%m/%d/%y')),
            ('Time',      self.created_local.strftime('%I:%M:%S %p')),
            ('Text',      self.text.encode('utf-8')),
            ('Retweets',  self.retweets),
            ('Favorites', self.favorites),
        ])


## Mention

class Mention(BaseTweet):
    def __init__(self, raw_mention):
        self.text               = raw_mention['text']
        self.retweets           = raw_mention['retweet_count']
        self.favorites          = raw_mention['favorite_count']
        self.source             = raw_mention['source']
        self.created_utc, self.created_local = \
            self._created_at_to_datetime(raw_mention['created_at'])
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


class Mentioner(BaseTweet):
    def __init__(self, mention_count, processed_mention, username_mentioned):
        self.mention_count = mention_count
        self.username_mentioned = username_mentioned
        fields = ['user_handle', 'user_name', 'location',
                  'user_followers', 'user_total_tweets']
        for field in fields:
            setattr(self, field, getattr(processed_mention, field))

    def __repr__(self):
         return '<Mentioner "%s", %d>' % \
                (self.user_handle[:40].encode('ascii', 'replace'),
                 self.mention_count)

    def to_dict(self):
        return collections.OrderedDict([
            ('Times mentioning %s' %
             self.username_mentioned, self.mention_count),
            ('User',         u'@%s' % self.user_handle.encode('utf-8')),
            ('Name',         self.user_name.encode('utf-8')),
            ('Location',     self.location.encode('utf-8')),
            ('Followers',    self.user_followers),
            ('Total tweets', self.user_total_tweets),
        ])
