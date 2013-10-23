twitarian
=========

Your twitter librarian. Calculates some (possibly) useful metrics.

## What does it do?

This app pulls your tweets and the tweets of people who have mentioned you, over a time interval that you specify.
It dumps this data into Excel, and calculates some metrics for you, like
- Number of re-tweets
- Number of favorites
- Number of times others mentioned you
- Your most-popular tweets
- Who talks about you the most
- A measurement of your "Engagement"

The app generates an Excel 2007 file

## How to use on Windows

1. Download the latest release of the program from [this page](https://github.com/bcattle/twitarian/releases).
Click the green button to get Windows binaries.

2. Save the zip file somewhere and open it

3. Go in the `dist/` folder and run `twitarian.exe`. You should see:

![Screenshot: Please enter username](https://raw.github.com/bcattle/twitarian/master/doc/how-to-0.png)

Begin by entering your username.

![Screenshot: Please enter start date](https://raw.github.com/bcattle/twitarian/master/doc/how-to-1.png)

Next, you need to tell the app how far back to analyze. If you have a lot of tweets, it can be slow to process them all.
THe app guesses that you might want to do a quarterly tally, and offers a suggested date. You can override it with a date
of your choice, or just hit <kbd>Enter</kbd> for the default.

![Screenshot: Waiting for PIN](https://raw.github.com/bcattle/twitarian/master/doc/how-to-2.png)

Now you need to tell the app how to access your Twitter account. The app needs to do this because only you are allowed
to see a list of who has mentioned you.

As you can see, it is waiting for you to enter a PIN. The way this works is that you need to give this app ("Twitarian")
permission to access Twitter on your behalf. The way you do this is by visiting a page on [twitter.com](http://twitter.com/)
in your web browser and getting a PIN that lets the app to access your tweets.

> IMPORTANT: The account you authorize with Twitter *must be the same account* you enter into Twitarian when it asks for
your username. Otherwise the app won't know on whose behalf it should be working!

The app should also open a web browser with this screen:

![Screenshot: Web browser](https://raw.github.com/bcattle/twitarian/master/doc/auth1.png)

Click "Authorize" and you should see

![Screenshot: Web browser with PIN](https://raw.github.com/bcattle/twitarian/master/doc/auth2.png)

Go back to the command prompt and type this code in. Press <kbd>Enter</kbd>, and presto! the app should run:

![Screenshot: PIN typed in](https://raw.github.com/bcattle/twitarian/master/doc/how-to-3.png)

Once the app is done, it will tell you the name of the file where it saved the results:

![Screenshot: Console after run](https://raw.github.com/bcattle/twitarian/master/doc/how-to-4.png)

To open the file in Excel, press <kbd>Enter</kbd>, otherwise press any other key to quit.

Happy tweeting!

### Uh oh, something went wrong

You may get the bogus error that "MSVCR90.dll is Missing or Not Found". If you do, you need to install a small library
from Microsoft. Download and run the installer [here](http://www.microsoft.com/en-us/download/details.aspx?id=29).

## How to use on a Mac

Go to the [releases](https://github.com/bcattle/twitarian/releases) page. Don't download the binaries, download the
source code tar.gz. Open a command prompt and unzip

```
% tar -zxvf 1.0.0.tar.gz
```

Install the needed libraries with

```
% sudo pip install -r requirements.txt
```

Then, simply run the script

```
% python twitarian.py
```

After that, the process is the same as above. Enter username, enter date of interest, authorize, and profit.
