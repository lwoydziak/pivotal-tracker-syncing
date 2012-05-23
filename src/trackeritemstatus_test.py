'''
Created on May 15, 2012

@author: lwoydziak
'''
import unittest
from trackeritemstatus import TrackerItemStatus
from jiraticket import JiraTicket
from mockito.mockito import verify
from mockito.mocking import mock


class TrackerItemStatusTests(unittest.TestCase):
    def test_whenSeedingWithRemoteStatusForJira(self):
        ticket = JiraTicket()
        statusId = "1234"
        ticket.setStatus(statusId)
        mapObject = mock()
        status = TrackerItemStatus(ticket, apiObject=mapObject)
        status.pivotal()
        verify(mapObject).translateStatusTo('pivotal', statusId)
        self.assertEqual(status.jira(), statusId)

    def test_whenSeedingWithPivotalStatus(self):
        pivotalStatus = "Started"
        mapObject = mock()
        status = TrackerItemStatus(pivotalStatus, apiObject=mapObject)
        status.jira()
        verify(mapObject).translateStatusTo('jira', pivotalStatus)
        self.assertEqual(status.pivotal(), pivotalStatus) 
        
    def test_canCreateDefaultStatus(self):
        status = TrackerItemStatus()
        self.assertEqual(status.jira(), None) 
        self.assertEqual(status.pivotal(), None)
        
    def test_equalityOfStatuses(self):
        status = TrackerItemStatus()
        statusEqual = TrackerItemStatus()
        self.assertTrue(status == statusEqual)
        self.assertFalse(status is statusEqual)
        
    def test_inequalityOfStatused(self):
        status = TrackerItemStatus()
        garbage = "garbage"
        pivotalStatus = "Started"
        mapObject = mock()
        statusNotEqual = TrackerItemStatus(pivotalStatus, apiObject=mapObject)
        self.assertTrue(status != statusNotEqual)
        self.assertFalse(status is statusNotEqual)
        self.assertTrue(status != garbage)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()