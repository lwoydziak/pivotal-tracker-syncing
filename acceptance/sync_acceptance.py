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
        self.assertEqual(pivotalItem.type(), 'bug')
    
    def syncExistingItemFrom(self, fromTracker, toTracker):
        item = next(fromTracker.items())
        syncItem = TrackerSyncBy.syncingItem()
        syncItem(item, toTracker)
    
    def test_existingIssueInJiraIsSyncedWithExistingIssueInPivotal(self):
        jira = self.jira_
        pivotal = self.pivotal_
        desiredSummary = "test_existingIssueInJiraIsSyncedWithExistingIssueInPivotal"
        desiredDescription = "overwritten!"
        newJiraItem = jiraItemFactory(Env().jiraProject, "to be overwritten", "also overwritten" )
        self.syncNewItemToPivotal(newJiraItem, jira, pivotal)
        jiraItem = next(jira.items())
        jiraItem.withDescription(desiredDescription)
        jiraItem.withSummary(desiredSummary)
        jira.update(jiraItem)
        self.syncExistingItemFrom(jira, pivotal)
        updatedPivotalItem = next(pivotal.items())
        self.assertEqual(updatedPivotalItem.summary(), desiredSummary)
        self.assertEqual(updatedPivotalItem.description(), desiredDescription)
        pass
    
    def test_commentOnIssueInJiraIsSyncedToPivotal(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newJiraItem = jiraItemFactory(Env().jiraProject, "to test comments", "blah")
        self.syncNewItemToPivotal(newJiraItem, jira, pivotal)
        commentOnJira = "this commentOnJira can be synced"
        jiraItem = next(jira.items())
        jiraItem.addComment(commentOnJira)
        jira.update(jiraItem)
        self.syncExistingItemFrom(jira, pivotal)
        updatedPivotalItem = next(pivotal.items())
        self.assertEqual(updatedPivotalItem.comments()[0], commentOnJira)
        pass
    
    def test_commentOnIssueInPivotalIsSyncedToJira(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newJiraItem = jiraItemFactory(Env().jiraProject, "test_commentOnIssueInPivotalIsSyncedToJira", "blah")
        self.syncNewItemToPivotal(newJiraItem, jira, pivotal)
        commentOnPivotal = "this commentOnPivotal can be synced"
        pivotalItem = next(pivotal.items())
        pivotalItem.addComment(commentOnPivotal)
        pivotal.update(pivotalItem)
        self.syncExistingItemFrom(pivotal, jira)
        updatedJiraItem = next(jira.items())
        self.assertEqual(updatedJiraItem.comments()[0], commentOnPivotal)
        pass
    
    def test_issueInJiraAndInPivotalAreSyncable(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newJiraItem = jiraItemFactory(Env().jiraProject, "test_issueInJiraAndInPivotalAreSyncable", "a test description")
        self.syncNewItemToPivotal(newJiraItem, jira, pivotal)
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