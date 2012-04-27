'''
Created on Apr 18, 2012

@author: lwoydziak
'''
import unittest
import sys
from config import Env
sys.path.insert(0, "src")
from jiratracker import JiraTracker
from pivotaltracker import PivotalTrackerFor
from jiraitemfactory import jiraItemFactory
from pivotaltrackeritem import PivotalTrackerItem



class SyncAcceptanceTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        jira = JiraTracker(Env().jiraUrl)
        jira.loginAs(Env().jiraUsername).withCredential(Env().jiraPassword)
        jira.selectProject([Env().jiraProject, Env().jiraJql])
        self.jira_ = jira
        pivotal = PivotalTrackerFor(Env().pivotalTrackerProject)
        pivotal.loginAs(Env().pivotalTrackerUsername).withCredential(Env().pivotalTrackerPassword)
        self.pivotal_ = pivotal
        pass


    def tearDown(self):
        self.jira_.deleteAllItems()
        self.jira_.finalize()
        self.pivotal_.deleteAllItems()
        unittest.TestCase.tearDown(self)

    def test_newIssueInJiraIsCopiedToPivotal(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newItem = jiraItemFactory(Env().jiraProject, "test_newIssueInJiraIsCopiedToPivotal", "A test description")
        jira.update(newItem)
        jiraItems = jira.items()
        newPivotalItem = PivotalTrackerItem()
        newPivotalItem.syncWith(jiraItems[0])
        pivotal.update(newPivotalItem)
        pass
    
    def test_existingIssueInJiraIsSyncedWithExistingIssueInPivotal(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newPivotalItem = PivotalTrackerItem().withSummary("to be overwritten").withDescription("A test description to be overwritten")
        pivotal.update(newPivotalItem)
        desiredSummary = "test_existingIssueInJiraIsSyncedWithExistingIssueInPivotal"
        desiredDescription = "Overwritten!"
        newJiraItem = jiraItemFactory(Env().jiraProject, desiredSummary, desiredDescription )
        jira.update(newJiraItem)
        jiraItems = jira.items()
        pivotalItems = pivotal.items()
        pivotalItems[0].syncWith(jiraItems[0])
        pivotal.update(pivotalItems[0])
        updatedPivotalItems = pivotal.items()
        self.assertEqual(updatedPivotalItems[0].summary(), desiredSummary)
        self.assertEqual(updatedPivotalItems[0].description(), desiredDescription)
        pass
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()