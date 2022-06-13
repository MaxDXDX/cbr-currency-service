"""A primitive logger. It was also possible to use ready to use modules (logging for example), but I have built this
one from scratch to decrease count of third-party modules.

.. moduleauthor:: Max Dubrovin <mihadxdx@gmail.com>

"""

import datetime as dt


class Logger:
    def __init__(self, log_file, enable=True, show_time=True):
        self.file = log_file
        self.show_time = show_time
        self.enable = enable

    def log(self, text):
        """Put log message to log file and print it in console"""
        if self.enable:
            message = self.message(text)
            self.to_console(message)
            self.to_file(message)

    def message(self, text):
        """Build log message from plain text and current time/date"""
        log_message = text
        now = dt.datetime.now().strftime('%Y-%m-%d %X')
        if self.show_time:
            log_message = f'{now}  {log_message}'
        return log_message

    def to_file(self, message):
        """Append log message to log file"""
        with open(self.file, 'a') as f:
            f.write(message + '\n')

    def to_console(self, message):
        """Print log message to console"""
        print(message)
