'''
Created on Jun 28, 2012

@author: lwoydziak
'''
import unittest
from trackeritemuser import PivotalUser, JiraUser, BaseUser
from mockito.mocking import mock
from mockito.mockito import when

class TrackerItemUserTest(unittest.TestCase):
    def test_whenSeedingWithUserForJira(self):
        pivotalUser = "me"
        jiraUser = "you"
        mapObject = mock()
        when(mapObject).translateUserTo('pivotal', jiraUser).thenReturn(pivotalUser)
        userObject = JiraUser(jiraUser, apiObject=mapObject)
        self.assertEqual(pivotalUser, userObject.pivotal())
        self.assertEqual(jiraUser, userObject.jira())
        
    def test_whenSeedingWithUserForPivotal(self):
        pivotalUser = "me"
        jiraUser = "you"
        mapObject = mock()
        when(mapObject).translateUserTo('jira', pivotalUser).thenReturn(jiraUser)
        userObject = PivotalUser(pivotalUser, apiObject=mapObject)
        self.assertEqual(pivotalUser, userObject.pivotal())
        self.assertEqual(jiraUser, userObject.jira())
        
    def test_canCreateDefault(self):
        status = BaseUser()
        self.assertEqual(status.jira(), None) 
        self.assertEqual(status.pivotal(), None)
        
    def test_equalityOfStatuses(self):
        pivotalUser = "me"
        jiraUser = "you"
        mapObject = mock()
        when(mapObject).translateUserTo('pivotal', jiraUser).thenReturn(pivotalUser)
        when(mapObject).translateUserTo('jira', pivotalUser).thenReturn(jiraUser)
        status = PivotalUser(pivotalUser, apiObject=mapObject)
        statusEqual = JiraUser(jiraUser, apiObject=mapObject)
        self.assertTrue(status == statusEqual)
        self.assertFalse(status is statusEqual)
        self.assertTrue(status == status)
        
    def test_inequalityOfStatused(self):
        pivotalUser = "me"
        jiraUser = "you"
        mapObject = mock()
        when(mapObject).translateUserTo('pivotal', jiraUser).thenReturn("garbage")
        when(mapObject).translateUserTo('jira', pivotalUser).thenReturn("garbage")
        status = PivotalUser(pivotalUser, apiObject=mapObject)
        statusEqual = JiraUser(jiraUser, apiObject=mapObject)
        self.assertTrue(status != statusEqual)
        self.assertTrue(status != "garbage")
        
    def test_isUnknownWhenOneIsNone(self):
        user = JiraUser("blah")
        self.assertTrue(user.unknown())
        user = PivotalUser("blah")
        self.assertTrue(user.unknown())
        
    def test_isKnownWhenAllAreNone(self):
        user = BaseUser()
        self.assertFalse(user.unknown())
        
    def test_isKnownWhenBothAreNotNone(self):
        user = BaseUser("blah")
        self.assertFalse(user.unknown())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()