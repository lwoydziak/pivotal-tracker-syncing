'''
Created on May 15, 2012

@author: lwoydziak
'''
import unittest
from trackeritemstatus import TrackerItemStatus
from jiraticket import JiraTicket
from mockito.mockito import verify, when
from mockito.mocking import mock
from mockito import inorder
from mockito.verification import never
from mockito.matchers import any


class TrackerItemStatusTests(unittest.TestCase):
    def test_whenSeedingWithRemoteStatusForJira(self):
        ticket = JiraTicket()
        statusId = "1234"
        closed = "Closed"
        ticket.setStatus(statusId)
        mapObject = mock()
        when(mapObject).translateStatusTo('jiraStatusName', statusId).thenReturn([closed])
        status = TrackerItemStatus(ticket, apiObject=mapObject)
        status.pivotal()
        inorder.verify(mapObject).translateStatusTo('jiraStatusName', statusId)
        inorder.verify(mapObject).translateStatusTo('pivotal', closed)
        self.assertEqual(status.jira(), [closed])

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
        
    def test_whenJiraIdIsZeroNameIsNone(self):
        jiraStatus = mock()
        mapObject = mock()
        when(jiraStatus).status().thenReturn("")
        status = TrackerItemStatus(jiraStatus, mapObject)
        verify(mapObject, never).translateStatusTo(any(), any())
        self.assertEqual(status.jira(), None)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()