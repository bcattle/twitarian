#!/usr/bin/env python

__version__ = '0.2.1'

from pytz import UTC
from twitter import Twitter, OAuth, oauth_dance
from tweetlist import TweetList
from ux import write_and_flush, get_screenname, get_start_date, \
    prompt_to_open_file, print_copyright
from output import save_to_csv, save_to_excel
from prefs import AppPreferences
from settings import *


# PRELIMINARIES

print_copyright(__version__)

# Load app preferences (if any)
prefs = AppPreferences()

# Ask the user for their screenname
twitter_account = get_screenname(default=prefs.get('last_screenname', ''))

# Ask the user for the start date
start_date = get_start_date()
# Set the timezone so we can compare w/ what's returned by Twitter
start_date = UTC.localize(start_date)

print 'Okay, pulling your tweets back to %s' % start_date.strftime('%Y-%m-%d')


# Auth
write_and_flush('Checking your password...')

credentials = prefs.get('credentials', {})

if not twitter_account.lower() in credentials:
    oauth_token, oauth_secret = \
        oauth_dance('Twidarian', CONSUMER_KEY, CONSUMER_SECRET)
    credentials[twitter_account.lower()] = oauth_token, oauth_secret
    prefs['credentials'] = credentials

oauth_token, oauth_secret = credentials[twitter_account.lower()]

#if not os.path.exists(CREDENTIALS_FILE):
#    oauth_dance('Twidarian', CONSUMER_KEY, CONSUMER_SECRET,
#                CREDENTIALS_FILE)
#oauth_token, oauth_secret = read_token_file(CREDENTIALS_FILE)

write_and_flush('password good.\n')


# DATA PULL

# Connect
write_and_flush('Connecting to twitter...')
t = Twitter(api_version=1.1,
            auth=OAuth(oauth_token, oauth_secret,
                       CONSUMER_KEY, CONSUMER_SECRET))
write_and_flush('done\n')

# Pull tweets and mentions
write_and_flush('Pulling tweets...')
tweets = TweetList.pull_tweets_for_user(t, twitter_account, start_date)
write_and_flush('done\n')

write_and_flush('Pulling mentions...')
mentions = TweetList.pull_mentions(t, start_date)
write_and_flush('done\n')

# This doesn't work, it returns sparse results
#write_and_flush('Pulling retweets...')
#retweets = TweetList.pull_manual_retweets(t, TWITTER_ACCOUNT, START_DATE)
#write_and_flush('done\n')

# INTERMEDIATE CALCULATIONS

write_and_flush('Analyzing the data...')

# Pull re-tweets out of the mentions
re_tweets = mentions.extract_retweets(twitter_account)

write_and_flush('done\n')



# DATA OUTPUT

all_data = [
    tweets, mentions, re_tweets
]

# Save to a csv file
#filename = save_to_csv(username=twitter_account,
#                       tweet_lists=all_data)

# Save to an excel workbook
write_and_flush('Saving everything in an Excel file...')
filename = save_to_excel(username=twitter_account,
                         tweet_lists=all_data)
write_and_flush('done!\n')


print '\nEverything ran successfully. The data was saved to the file'
print '\n\t%s\n' % filename

# Save preferences
prefs['last_screenname'] = twitter_account
prefs.save()

prompt_to_open_file(filename)



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
