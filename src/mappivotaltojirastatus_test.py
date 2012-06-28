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
        self.assertEqual(PivotalToJiraStatusMap().translateStatusTo('pivotal', jiraStatus.name), pivotalClosedStatus)
        self.assertEqual(PivotalToJiraStatusMap().translateStatusTo('jira', pivotalClosedStatus), [jiraStatus.name])
        self.assertEqual(PivotalToJiraStatusMap().translateStatusTo('jiraStatusName', jiraStatus.id), [jiraStatus.name])      
        
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
        
    def test_whenNoInsertsNothingCanBeTranslated(self):
        self.assertEqual(None, PivotalToJiraStatusMap().translateStatusTo('pivotal', None))
        self.assertEqual(None, PivotalToJiraStatusMap().translateStatusTo('jira', None))
        self.assertEqual(None, PivotalToJiraStatusMap().translateStatusTo('jiraStatusName', None))
    
    def setupBasicMapping(self):
        pivotalStatus = "started"
        jiraStatus = "In Test"
        jiraTransition = "Assigned"
        PivotalToJiraStatusMap().addMapping(jira=jiraStatus, pivotal=pivotalStatus)
        PivotalToJiraStatusMap().addMapping(jira=jiraStatus, transitionFrom=jiraTransition)
        return pivotalStatus, jiraStatus, jiraTransition
        
    def test_canAddJiraAliasForAlreadyExistingItem(self):
        pivotalStatus, jiraStatus, jiraTransition = self.setupBasicMapping()
        jiraStatuses = []
        jiraStatuses.append(RemoteStatus())
        jiraStatuses.append(RemoteStatus())
        jiraStatuses[0].id = 234
        jiraStatuses[0].name = jiraTransition
        jiraStatuses[1].id = 235
        jiraStatuses[1].name = jiraStatus
        PivotalToJiraStatusMap().insert(jiraStatuses)
        self.assertEqual([jiraStatus, jiraTransition], PivotalToJiraStatusMap().translateStatusTo('jira', pivotalStatus))
        self.assertEqual(PivotalToJiraStatusMap().translateStatusTo('jiraStatusName', jiraStatuses[0].id), [jiraStatus,jiraTransition])  
        
    def test_doNotAddDuplicateTransistion(self):
        pivotalStatus, jiraStatus, jiraTransition = self.setupBasicMapping()
        PivotalToJiraStatusMap().addMapping(jira=jiraStatus, transitionFrom=jiraTransition)
        aliases = PivotalToJiraStatusMap().getAllAliasesFor_[jiraStatus]
        self.assertEqual(len(set(aliases)), len(aliases))
        
    def test_getNoneStatusWhenNoItemsFor(self):
        PivotalToJiraStatusMap().addMapping(jira="closed", pivotal="Accepted")
        PivotalToJiraStatusMap().insert(self.jiraClosedRemoteStatus())
        self.assertEqual(PivotalToJiraStatusMap().translateStatusTo('pivotal', 'garbage'), None)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_canMapJiraStatusToPivotalStatus']
    unittest.main()