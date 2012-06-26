'''
Created on Jun 24, 2012

@author: lwoydziak
'''
import unittest
from datetime import datetime, timedelta
from timezonejira import JiraTimezone

class JiraTimezoneTest(unittest.TestCase):
    def test_jiraTimezone(self):
        offset = -8
        jiraTimezone = JiraTimezone(offset)
        dateTime = datetime.now()
        self.assertEqual("JiraTimezone", jiraTimezone.tzname(None))
        self.assertEqual(timedelta(hours=1), jiraTimezone.dst(dateTime))
        self.assertEqual(timedelta(hours=offset+1), jiraTimezone.utcoffset(dateTime))
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()