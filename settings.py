# -*- coding: utf-8 -*-
import datetime
#from pytz import timezone
from pytz import UTC

VERSION = '0.2.0'

## Settings

TWITTER_ACCOUNT = 'DalbergTweet'
#LOCAL_TIME      = timezone('US/Eastern')

# START_DATE      = datetime.datetime(2013, 1, 1, tzinfo=LOCAL_TIME)
# START_DATE      = datetime.datetime(2013, 4, 1, tzinfo=LOCAL_TIME)
#START_DATE      = datetime.datetime(2013, 7, 1, tzinfo=LOCAL_TIME)

# We need to use UTC, py2exe can't handle pytz time zones
START_DATE      = datetime.datetime(2013, 7, 1, tzinfo=UTC)


## Authentication

CONSUMER_KEY = 'du4W5e4hbaTJqGLX5U270g'
CONSUMER_SECRET = 'wL0OvhRoIB5RrXLh3FvrEFt9e1PFsCkDVXurNx7YQc'

CREDENTIALS_FILE = '.twitter_credentials'


## I/O

OUTPUT_FILENAME     = '%s - %s' % (
    TWITTER_ACCOUNT,
    #datetime.datetime.now(tz=LOCAL_TIME).strftime('%b %d, %Y %I.%M.%S %p')
    datetime.datetime.now().strftime('%b %d, %Y %I.%M.%S %p')
)
