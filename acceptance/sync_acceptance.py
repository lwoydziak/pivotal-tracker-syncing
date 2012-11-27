'''
Created on Apr 18, 2012

@author: lwoydziak
'''

import unittest
import sys
from acceptance_test_support import SingleJira, SinglePivotal
from jiratrackeritem import JiraTrackerItem
sys.path.insert(0, "src")
from config import Env
from jiratracker import JiraTracker
from pivotaltracker import PivotalTrackerFor
from jiraitemfactory import jiraItemFactory
from pivotaltrackeritem import PivotalTrackerItem
from trackersyncby import TrackerSyncBy
from trackeritemstatus import TrackerItemStatus
from trackeritemuser import JiraUser, PivotalUser
from trackeritemcomment import TrackerItemComment
from mappivotaltojirastatus import PivotalToJiraStatusMap
from mapusers import PivotalToJiraUserMap
from unit_test_support import Testing
from acceptance_test_support import Testing as AcceptanceTesting



class SyncAcceptanceTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.jira_ = SingleJira().instance()
        self.pivotal_ = SinglePivotal().instance()
        AcceptanceTesting.mapStatuses(self.jira_)
        AcceptanceTesting.mapUsers()
        pass

    def tearDown(self):
        self.jira_.deleteAllItems()
        self.pivotal_.deleteAllItems()
        PivotalToJiraStatusMap().reset()
        PivotalToJiraUserMap().reset()
        unittest.TestCase.tearDown(self)

    def syncNewItemToPivotal(self, newJiraItem, jira, pivotal):
        jira.update(newJiraItem)
        syncByAddingItems = TrackerSyncBy.addingItemsOfType(PivotalTrackerItem)
        syncByAddingItems(fromTracker=jira, toTracker=pivotal)
    
    def syncExistingItemFrom(self, fromTracker, toTracker):
        item = next(fromTracker.items())
        syncItem = TrackerSyncBy.syncingItem()
        syncItem(item, toTracker)
        
    def create_getOtherUserAfterUpdatingJiraItem(self, attributeSetter):
        def getOtherUserAfterUpdatingJiraItem_(jira, pivotal, newJiraItem):
            self.syncNewItemToPivotal(newJiraItem, jira, pivotal)
            jiraItem = next(jira.items())
            user = JiraUser(Env().get("jira", "otherUser"))
            attributeSetter(jiraItem, user)
            jira.update(jiraItem)
            return user
        return getOtherUserAfterUpdatingJiraItem_
    
    def create_updatePivotalAndSyncJiraItem(self, attributeSetter):
        def updatePivotalAndSyncJiraItem_(jira, pivotal):
            item = next(pivotal.items())
            attributeSetter(item, PivotalUser(Env().get("pivotal", "username")))
            pivotal.update(item)
            item = next(pivotal.items())
            attributeSetter(item, PivotalUser(None))
            syncItem = TrackerSyncBy.syncingItem()
            syncItem(item, jira)
            return next(jira.items())
        return updatePivotalAndSyncJiraItem_

    def tryToSyncUnknownUser(self, jira, pivotal):
        PivotalToJiraUserMap().reset()
        PivotalToJiraUserMap().addMapping(jira=Env().get("jira", "username"), pivotal=Env().get("pivotal", "username"))
        self.syncExistingItemFrom(jira, toTracker=pivotal)
        self.syncExistingItemFrom(pivotal, toTracker=jira)
        PivotalToJiraUserMap().addMapping(jira=Env().get("jira", "otherUser"), pivotal=Env().get("pivotal", "otherUser"))
        jiraItem = next(jira.items())
        return jiraItem

    def test_newIssueInJiraIsCopiedToPivotal(self):
        jira = self.jira_
        pivotal = self.pivotal_
        summary = "test_newIssueInJiraIsCopiedToPivotal"
        newJiraItem = jiraItemFactory(Env().get("jira", "project"), summary, "a test description")
        self.syncNewItemToPivotal(newJiraItem, jira, pivotal)
        pivotalItem = next(pivotal.items())
        self.assertEqual(pivotalItem.summary(), summary)
        self.assertEqual(pivotalItem.type(), 'bug')
    
    def test_existingIssueInJiraIsSyncedWithExistingIssueInPivotal(self):
        jira = self.jira_
        pivotal = self.pivotal_
        desiredSummary = "test_existingIssueInJiraIsSyncedWithExistingIssueInPivotal"
        desiredDescription = "overwritten!"
        newJiraItem = jiraItemFactory(Env().get("jira", "project"), "to be overwritten", "also overwritten" )
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
        newJiraItem = jiraItemFactory(Env().get("jira", "project"), "to test comments", "blah")
        self.syncNewItemToPivotal(newJiraItem, jira, pivotal)
        commentOnJira = TrackerItemComment("this commentOnJira can be synced")
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
        newJiraItem = jiraItemFactory(Env().get("jira", "project"), "test_commentOnIssueInPivotalIsSyncedToJira", "blah")
        self.syncNewItemToPivotal(newJiraItem, jira, pivotal)
        commentOnPivotal = TrackerItemComment("this commentOnPivotal can be synced")
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
        newJiraItem = jiraItemFactory(Env().get("jira", "project"), "test_issueInJiraAndInPivotalAreSyncable", "a test description")
        self.syncNewItemToPivotal(newJiraItem, jira, pivotal)
        jiraItem = next(jira.items())
        pivotalItem = next(pivotal.items())
        self.assertTrue(pivotalItem.canBeSyncedWith(jiraItem))
    
    def test_20000PlusCharacterCommentsAreNotSyned(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newJiraItem = jiraItemFactory(Env().get("jira", "project"), "test_20000PlusCharacterCommentsAreNotSyned", "blah")
        commentOnJira = TrackerItemComment(Testing.stringOfAsOfSize(20002))
        newJiraItem.addComment(commentOnJira)
        self.syncNewItemToPivotal(newJiraItem, jira, pivotal)
        pivotalItem = next(pivotal.items())
        self.assertEqual(len(pivotalItem.comments()), 0)
        
    def test_canSyncStatusToPivotalForExistingItems(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newJiraItem = jiraItemFactory(Env().get("jira", "project"), "test_canSyncStatusToPivotalForExistingItems", "a test description")
        self.syncNewItemToPivotal(newJiraItem, jira, pivotal)
        jiraItem = next(jira.items())
        status = TrackerItemStatus("accepted")
        jiraItem.withStatus(status)
        jira.update(jiraItem)
        self.syncExistingItemFrom(jira, pivotal)
        pivotalItem = next(pivotal.items())
        self.assertEqual(pivotalItem.status(),status)

    def test_canSyncReporterToPivotalForExistingItems(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newJiraItem = jiraItemFactory(Env().get("jira", "project"), "test_canSyncReporterToPivotalForExistingItems", "a test description")
        getOtherUserAfterUpdatingJiraItem = self.create_getOtherUserAfterUpdatingJiraItem(JiraTrackerItem.withRequestor)
        user = getOtherUserAfterUpdatingJiraItem(jira, pivotal, newJiraItem)
        self.syncExistingItemFrom(jira, toTracker=pivotal)
        pivotalItem = next(pivotal.items())
        self.assertEqual(pivotalItem.requestor(),user) 

    def test_doNotOverwriteJiraReporterWhenUnknown(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newJiraItem = jiraItemFactory(Env().get("jira", "project"), "test_doNotOverwriteJiraReporterWhenUnknown", "a test description")
        getOtherUserAfterUpdatingJiraItem = self.create_getOtherUserAfterUpdatingJiraItem(JiraTrackerItem.withRequestor)
        user = getOtherUserAfterUpdatingJiraItem(jira, pivotal, newJiraItem)
        jiraItem = self.tryToSyncUnknownUser(jira, pivotal)
        self.assertEqual(jiraItem.requestor(), user)
        
    def test_canSyncOwnerToPivotalForExistingItems(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newJiraItem = jiraItemFactory(Env().get("jira", "project"), "test_canSyncOwnerToPivotalForExistingItems", "a test description")
        getOtherUserAfterUpdatingJiraItem = self.create_getOtherUserAfterUpdatingJiraItem(JiraTrackerItem.withOwner)
        user = getOtherUserAfterUpdatingJiraItem(jira, pivotal, newJiraItem)
        self.syncExistingItemFrom(jira, toTracker=pivotal)
        pivotalItem = next(pivotal.items())
        self.assertEqual(pivotalItem.owner(),user)
    
    def test_doNotOverwriteJiraOwnerWhenUnknown(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newJiraItem = jiraItemFactory(Env().get("jira", "project"), "test_doNotOverwriteJiraOwnerWhenUnknown", "a test description")
        getOtherUserAfterUpdatingJiraItem = self.create_getOtherUserAfterUpdatingJiraItem(JiraTrackerItem.withOwner)
        user = getOtherUserAfterUpdatingJiraItem(jira, pivotal, newJiraItem)
        jiraItem = self.tryToSyncUnknownUser(jira, pivotal)
        self.assertEqual(jiraItem.owner(), user)

      
    def test_doNotOverwriteJiraReporterWhenUnassignedInPivotal(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newJiraItem = jiraItemFactory(Env().get("jira", "project"), "test_doNotOverwriteJiraReporterWhenUnassignedInPivotal", "a test description")
        newJiraItem.withRequestor(PivotalUser(Env().get("pivotal", "otherUser")))
        getOtherUserAfterUpdatingJiraItem = self.create_getOtherUserAfterUpdatingJiraItem(JiraTrackerItem.withRequestor)
        user = getOtherUserAfterUpdatingJiraItem(jira, pivotal, newJiraItem)
        updatePivotalAndSyncJiraItem = self.create_updatePivotalAndSyncJiraItem(PivotalTrackerItem.withRequestor)
        jiraItem = updatePivotalAndSyncJiraItem(jira, pivotal)
        self.assertEqual(jiraItem.requestor(), user)

    def test_doNotOverwriteJiraOwnerWhenUnassignedInPivotal(self):
        jira = self.jira_
        pivotal = self.pivotal_
        newJiraItem = jiraItemFactory(Env().get("jira", "project"), "test_doNotOverwriteJiraOwnerWhenUnassignedInPivotal", "a test description")
        newJiraItem.withOwner(PivotalUser(Env().get("pivotal", "otherUser")))
        getOtherUserAfterUpdatingJiraItem = self.create_getOtherUserAfterUpdatingJiraItem(JiraTrackerItem.withRequestor)
        user = getOtherUserAfterUpdatingJiraItem(jira, pivotal, newJiraItem)
        updatePivotalAndSyncJiraItem = self.create_updatePivotalAndSyncJiraItem(PivotalTrackerItem.withOwner)
        jiraItem = updatePivotalAndSyncJiraItem(jira, pivotal)
        self.assertEqual(jiraItem.owner(), user)
        
    def test_whenTicketNumberInCommentsOfOtherTickerTheRightSyncOccurs(self):
        jira = self.jira_
        pivotal = self.pivotal_
        desiredSummary = "test_whenTicketNumberInCommentsOfOtherTickerTheRightSyncOccurs-1"
        desiredDescription = "overwritten!"
        newJiraItem = jiraItemFactory(Env().get("jira", "project"), "to be overwritten", "also overwritten" )
        self.syncNewItemToPivotal(newJiraItem, jira, pivotal)
        jiraItem = next(jira.items())
        
        newJiraItem = jiraItemFactory(Env().get("jira", "project"), "test_whenTicketNumberInCommentsOfOtherTickerTheRightSyncOccurs-2", "don't overwrite" )
        newJiraItem.addComment(TrackerItemComment(jiraItem.Id()))
        self.syncNewItemToPivotal(newJiraItem, jira, pivotal)
        
        for item in jira.items():
            jiraItem = item
        
        jiraItem.withDescription(desiredDescription)
        jiraItem.withSummary(desiredSummary)
        jira.update(jiraItem)
        
        syncItem = TrackerSyncBy.syncingItem()
        for item in jira.items():
            syncItem(item, toTracker=pivotal)
        
        
        for item in pivotal.items():
            updatedPivotalItem = item
        
        self.assertEqual(updatedPivotalItem.summary(), desiredSummary)
        self.assertEqual(updatedPivotalItem.description(), desiredDescription)
        pass 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()