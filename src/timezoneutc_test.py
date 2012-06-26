'''
Created on Jun 22, 2012

@author: lwoydziak
'''
import unittest
from timezoneutc import UTC
from datetime import timedelta

class UTC_Tests(unittest.TestCase):
    def test_utc(self):
        utc = UTC()
        self.assertEqual("UTC", utc.tzname(None))
        self.assertEqual(timedelta(0), utc.utcoffset(None))
        self.assertEqual(timedelta(0), utc.dst(None))
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()