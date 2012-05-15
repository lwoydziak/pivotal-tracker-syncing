'''
Created on May 15, 2012

@author: lwoydziak
'''
import unittest
from trackeritemstatus import TrackerItemStatus


class TrackerItemStatusTests(unittest.TestCase):
    def test_BasePivotalAndJiraValues(self):
        status = TrackerItemStatus()
        self.assertEqual(status.forJiraTracker(), 0)
        self.assertEqual(status.forPivotalTracker(), 0)
        pass
    
    def test_InTestStatusReturnsCorrect(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()