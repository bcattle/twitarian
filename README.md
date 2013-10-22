twitarian
=========

Your twitter librarian. Calculates some (possibly) useful metrics.
Retweet count, favorites count, followers count.
Outputs an Excel 2007 file

## How to use on Windows

1. Download the program. Click the "Download ZIP" button to the right
2. Save the zip file somewhere and open it
3. Go in the `dist/` folder and run `twitarian.exe`. You should see:

![Screenshot: Waiting for PIN](https://raw.github.com/bcattle/twitarian/master/img/twitarian0.png)

As you can see, it is waiting for you to enter a PIN. The way this works is that you need to give this app ("Twitarian")
permission to access Twitter on your behalf. This is mainly so it can pull a list of people who have mentioned you -
users are only able to see their *own* mentions.

The way you do this is by visiting a page on `twitter.com` and authorizing the app to access your tweets.

The app should also open a web browser with this screen:

![Screenshot: Web browser](https://raw.github.com/bcattle/twitarian/master/img/twitarian2.png)

4. Click "Authorize" and you should see

![Screenshot: Web browser with PIN](https://raw.github.com/bcattle/twitarian/master/img/twitarian3.png)

Go back to the command prompt and type this code in.

![Screenshot: PIN typed in](https://raw.github.com/bcattle/twitarian/master/img/twitarian1.png)

The script should run, and you should see


To open the file in Excel, press <kbd>Enter</kbd>, otherwise press any other key to quit.

