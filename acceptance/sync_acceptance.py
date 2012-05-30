'''
Created on Apr 18, 2012

@author: lwoydziak
'''
import unittest
import sys
from config import Env
from acceptance_test_support import SingleJira, SinglePivotal
sys.path.insert(0, "src")
from jiratracker import JiraTracker
from pivotaltracker import PivotalTrackerFor
from jiraitemfactory import jiraItemFactory
from pivotaltrackeritem import PivotalTrackerItem
from trackersyncby import TrackerSyncBy
from unit_test_support import Testing



class SyncAcceptanceTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.jira_ = SingleJira().instance()
        self.pivotal_ = SinglePivotal().instance()
        pass

    def tearDown(self):
        self.jira_.deleteAllItems()
        self.pivotal_.deleteAllItems()
        unittest.TestCase.tearDown(self)

    def syncNewItemToPivotal(self, newJiraItem, jira, pivotal):
        jira.update(newJiraItem)
        syncByAddingItems = TrackerSyncBy.addingItemsOfType(PivotalTrackerItem)
        syncByAddingItems(fromTracker=jira, toTracker=pivotal)
    
    def test_newIssueInJiraIsCopiedToPivotal(self):
        jira = self.jira_
        pivotal = self.pivotal_
        summary = "test_newIssueInJiraIsCopiedToPivotal"
        newJiraItem = jiraItemFactory(Env().jiraProject, summary, "a test description")
        self.syncNewItemToPivotal(newJiraItem, jira, pivotal)
        pivotalItem = next(pivotal.items())
        self.assertEqual(pivotalItem.summary(), summary)
    
    def syncExistingItemFromJiraToPivotal(self, newJiraItem, jira, pivotal):
        jira.update(newJiraItem)
        jiraItem = next(jira.items())
        pivotalItem = next(pivotal.items())
        pivotalItem.syncWith(jiraItem)
        pivotal.update(pivotalItem)
    
    def test_existingIssueInJiraIsSyncedWithExistingIssueInPivotal(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newPivotalItem = PivotalTrackerItem().withSummary("to be overwritten").withDescription("a test description to be overwritten")
        pivotal.update(newPivotalItem)
        desiredSummary = "test_existingIssueInJiraIsSyncedWithExistingIssueInPivotal"
        desiredDescription = "overwritten!"
        newJiraItem = jiraItemFactory(Env().jiraProject, desiredSummary, desiredDescription )
        self.syncExistingItemFromJiraToPivotal(newJiraItem, jira, pivotal)
        updatedPivotalItem = next(pivotal.items())
        self.assertEqual(updatedPivotalItem.summary(), desiredSummary)
        self.assertEqual(updatedPivotalItem.description(), desiredDescription)
        pass
    
    def test_commentOnIssueInJiraIsSyncedToPivotal(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newPivotalItem = PivotalTrackerItem().withSummary("to test comments").withDescription("description")
        pivotal.update(newPivotalItem)
        newJiraItem = jiraItemFactory(Env().jiraProject, "to test comments", "blah")
        commentOnJira = "this commentOnJira can be synced"
        newJiraItem.addComment(commentOnJira)
        self.syncExistingItemFromJiraToPivotal(newJiraItem, jira, pivotal)
        updatedPivotalItem = next(pivotal.items())
        self.assertEqual(updatedPivotalItem.comments()[0], commentOnJira)
        pass
    
    def test_commentOnIssueInPivotalIsSyncedToJira(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newPivotalItem = PivotalTrackerItem().withSummary("to test comments").withDescription("description")
        newJiraItem = jiraItemFactory(Env().jiraProject, "to test comments", "blah")
        commentOnPivotal = "this commentOnPivotal can be synced"
        newPivotalItem.addComment(commentOnPivotal)
        pivotal.update(newPivotalItem)
        jira.update(newJiraItem)
        jiraItem = next(jira.items())
        pivotalItem = next(pivotal.items())
        jiraItem.syncWith(pivotalItem)
        jira.update(jiraItem)
        updatedJiraItem = next(jira.items())
        self.assertEqual(updatedJiraItem.comments()[0], commentOnPivotal)
        pass
    
    def test_issueInJiraAndInPivotalAreSyncable(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newJiraItem = jiraItemFactory(Env().jiraProject, "test_issueInJiraAndInPivotalAreSyncable", "a test description")
        newPivotalItem = PivotalTrackerItem().withSummary("test_issueInJiraAndInPivotalAreSyncable-2").withDescription("description")
        pivotal.update(newPivotalItem)
        self.syncExistingItemFromJiraToPivotal(newJiraItem, jira, pivotal)
        jiraItem = next(jira.items())
        pivotalItem = next(pivotal.items())
        self.assertTrue(pivotalItem.canBeSyncedWith(jiraItem))
        pass

    
    def test_20000PlusCharacterCommentsAreNotSyned(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newJiraItem = jiraItemFactory(Env().jiraProject, "test_20000PlusCharacterCommentsAreNotSyned", "blah")
        commentOnJira = Testing.stringOfAsOfSize(20002)
        newJiraItem.addComment(commentOnJira)
        self.syncNewItemToPivotal(newJiraItem, jira, pivotal)
        pivotalItem = next(pivotal.items())
        self.assertEqual(len(pivotalItem.comments()), 0)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()