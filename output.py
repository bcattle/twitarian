from datetime import datetime
from openpyxl import Workbook


def get_filename(username, extension=''):
    extension_str = '.%s' % extension if extension else ''
    return '%s - %s%s' % (
        username,
        datetime.now().strftime('%b %d, %Y %I.%M.%S %p'),
        extension_str
    )


def save_to_csv(username, tweet_lists):
    filename = get_filename(username, extension='csv')
    with open(filename, 'w') as csvfile:
        for tweet_list in tweet_lists:
            tweet_list.save_output_file(csvfile)
    return filename


def save_to_excel(username, tweet_lists):
    filename = get_filename(username, extension='xlsx')

    wb = Workbook()
    for i, tweet_list in enumerate(tweet_lists):
        if i == 0:
            # First sheet, already there
            ws = wb.get_active_sheet()
        else:
            # Second sheet, create it
            ws = wb.create_sheet()

        ws.title = tweet_list.name
        tweet_list.save_into_worksheet(ws)

    # Save the file
    wb.save(filename)

    return filename
