'''
Created on Jun 28, 2012

@author: lwoydziak
'''
import unittest
from mapusers import PivotalToJiraUserMap

class PivotalToJiraUserMapTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        PivotalToJiraUserMap().reset()
        
    def test_canMapJiraUserToPivotalUser(self):
        pivotalUser = "First Last"
        jiraUser = "flast"
        PivotalToJiraUserMap().addMapping(jira=jiraUser, pivotal=pivotalUser)
        self.assertEqual(PivotalToJiraUserMap().translateUserTo('pivotal', jiraUser), pivotalUser)
        self.assertEqual(PivotalToJiraUserMap().translateUserTo('jira', pivotalUser), jiraUser)
        
    def test_whenNoInsertsNothingCanBeTranslated(self):
        self.assertEqual(None, PivotalToJiraUserMap().translateUserTo('pivotal', None))
        self.assertEqual(None, PivotalToJiraUserMap().translateUserTo('jira', None))

    def test_getNoneWhenLookingForGarbageUser(self):  
        pivotalUser = "First Last"
        jiraUser = "flast"
        PivotalToJiraUserMap().addMapping(jira=jiraUser, pivotal=pivotalUser)
        self.assertEqual(None, PivotalToJiraUserMap().translateUserTo('pivotal', "garbage"))
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()