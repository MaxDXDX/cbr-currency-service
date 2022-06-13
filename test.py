import os
import unittest

from currency_service import OnDateCurs
from os.path import exists


class TestCur(unittest.TestCase):
    def test_create_db_file(self):
        """
        Test for creating database file
        """
        if exists('test.db'):
            os.remove('test.db')

        OnDateCurs('test.db', options=['--date=11.05.2011', '--codes=*', '--rewrite'], log_enable=False)
        existence = exists('test.db')

        if exists('test.db'):
            os.remove('test.db')

        self.assertTrue(existence)

    # TODO more test methods


if __name__ == '__main__':
    unittest.main()