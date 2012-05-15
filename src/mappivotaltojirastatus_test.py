'''
Created on May 15, 2012

@author: lwoydziak
'''
import unittest
from mappivotaltojirastatus import PivotalToJiraStatusMap
from jiraremotestructures import RemoteStatus

class PivotalToJiraStatusMapTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        PivotalToJiraStatusMap().reset()
    
    def jiraClosedRemoteStatus(self):
        jiraStatus = RemoteStatus()
        jiraStatus.id = 6
        jiraStatus.name = "closed"
        return jiraStatus
    
    def test_canMapJiraStatusToPivotalStatus(self):
        pivotalClosedStatus = "Accepted"
        jiraStatus = self.jiraClosedRemoteStatus()
        PivotalToJiraStatusMap().addMapping(jira=jiraStatus.name, pivotal=pivotalClosedStatus)
        PivotalToJiraStatusMap().insert(jiraStatus)
        self.assertEqual(PivotalToJiraStatusMap().getPivotalStatusFor(jiraStatus.id), pivotalClosedStatus)
        self.assertEqual(PivotalToJiraStatusMap().getJiraStatusFor(pivotalClosedStatus), jiraStatus.id)
        
    def test_canInsertMultipleJiraStatuses(self):
        PivotalToJiraStatusMap().addMapping(jira="closed", pivotal="Accepted")
        PivotalToJiraStatusMap().addMapping(jira="new", pivotal="Not Yet Started")
        jiraStatuses = []
        jiraStatuses.append(self.jiraClosedRemoteStatus())
        jiraStatuses.append(RemoteStatus())
        jiraStatuses[1].id = 10004
        jiraStatuses[1].name = "new"
        PivotalToJiraStatusMap().insert(jiraStatuses)
        self.assertEqual(len(PivotalToJiraStatusMap()), 2)
        
    def test_donotInsertUnmappedStatus(self):
        jiraStatus = self.jiraClosedRemoteStatus()
        PivotalToJiraStatusMap().insert(jiraStatus)
        self.assertEqual(len(PivotalToJiraStatusMap()), 0)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_canMapJiraStatusToPivotalStatus']
    unittest.main()