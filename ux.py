import sys
import os
import datetime
from dateutil.tz import tzlocal


def write_and_flush(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def print_copyright(version):
    print '\nTwitarian, version %s' % version
    print '<http://github.com/bcattle/twitarian/>'
    print 'Bryan Cattle, (c) 2013\n'


def get_screenname(default=''):
    """
    Asks the user for their screenname and
    returns it as a string
    """
    default_str = ' or press enter to use [%s]' % default if default else ''
    while True:
        twitter_account = raw_input('Please enter your twitter username '
                                    'without the "@" sign%s: ' % default_str)
        if twitter_account and twitter_account.strip()[0] != '@':
            break
        elif not twitter_account and default:
            twitter_account = default
            break
    return twitter_account.strip()


def get_start_date():
    # Try to guess what quarter the user is interested in
    this_year = datetime.date.today().year
    quarter_start_dates = [
        datetime.date(this_year, 1, 1),
        datetime.date(this_year, 4, 1),
        datetime.date(this_year, 7, 1),
        datetime.date(this_year, 10, 1),
    ]

    # What was the start date of the most recently ended quarter?
    last_qtr = filter(lambda x: x < datetime.date.today(),
                      quarter_start_dates)[-1]

    # Allow the user to enter a different date, if desired
    print 'How far back do you want to go?'
    print 'Press <enter> for the last quarter, which started on %s' \
          % last_qtr.strftime('%B %d')
    print 'Or enter a new date as [YYYY-MM-DD]'

    while True:
        new_date = raw_input('>')

        if not new_date:
            # Accept the default
            start_date = datetime.datetime.combine(
                last_qtr, datetime.datetime.min.time()
            )
            break
        else:
            # Try to parse the input
            try:
                start_date = datetime.datetime.strptime(new_date, '%Y-%m-%d')
                # It worked
                break
            except ValueError:
                print 'Sorry, couldn\'t understand the date "%s". ' \
                      'Try again as [YYYY-MM-DD]' % new_date
    # Assume the user wants the date in their local timezone
    start_date = start_date.replace(tzinfo=tzlocal())
    return start_date


def prompt_to_open_file(filename):
    # If we're in Windows, offer to open the file in Excel
    if os.name == 'nt':

        print '\nPress <enter> to open this file in Excel,'
        print 'otherwise press any other key to quit.'

        import msvcrt
        c = msvcrt.getch()
        if c == '\r':
            # Open in excel
            #os.system('start "%s\\%s"' % (sys.path[0], filename))
            from subprocess import Popen
            Popen(filename, shell=True)

    else:
        raw_input('Press any key to continue')
