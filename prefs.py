import cPickle

FILENAME = '.prefs'

class AppPreferences(dict):
    """
    This class handles saving and restoring app preferences
    from a single pickled dictionary.
    """
    def __init__(self):
        """
        Open and unpickle the file if it exists
        """
        unpickled = {}
        try:
            with open(FILENAME, 'rb') as pfile:
                unpickled = cPickle.load(pfile)
        except IOError:
            # File doesn't exist
            pass
        super(AppPreferences, self).__init__(unpickled)

    def save(self):
        """
        Saves the contents of this dict to the file
        """
        with open(FILENAME, 'wb') as pfile:
            cPickle.dump(self, pfile)
