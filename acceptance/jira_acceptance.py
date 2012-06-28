'''
Created on Mar 29, 2012

@author: lwoydziak
'''
import unittest
import sys
from config import Env
from acceptance_test_support import Testing, SingleJira
from jiraitemfactory import jiraItemFactory
sys.path.insert(0, "src")
from mappivotaltojirastatus import PivotalToJiraStatusMap
from trackeritemstatus import TrackerItemStatus



class JiraAccpetanceTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.jira_ = SingleJira().instance()
        pass
    
    def tearDown(self):
        self.jira_.deleteAllItems()
        PivotalToJiraStatusMap().reset()
        unittest.TestCase.tearDown(self)
    
    def test_canConnectToJira(self):
        tracker = self.jira_
        self.assertTrue(tracker.valid())
        
    def test_canDeleteJiraIssue(self):
        tracker = self.jira_
        item = jiraItemFactory(Env().jiraProject, "test_canDeleteJiraIssue", "A test description")
        tracker.update(item)
        tracker.delete(next(tracker.items()))
        
    def test_canDownloadStoriesFromJira(self):
        tracker = self.jira_
        item = jiraItemFactory(Env().jiraProject, "test_canDownloadStoriesFromJira-1", "A test description")
        tracker.update(item)
        item.withSummary("test_canDownloadStoriesFromJira-2")
        tracker.update(item)
        storiesIterator = tracker.items()
        next(storiesIterator)
        next(storiesIterator)
        self.assertRaises(StopIteration, next, storiesIterator)
    
    def test_canAddStoryStoryToJira(self):
        tracker = self.jira_
        name = "test_canAddStoryStoryToPivotal"
        description = "this is a test"
        item = jiraItemFactory(Env().jiraProject, name, description)
        tracker.update(item)
        story = next(tracker.items())
        self.assertEqual(story.summary(), name)
        self.assertEqual(story.description(), description)
        
    def test_canRemoveAllStoriesFromJira(self):
        tracker = self.jira_
        item = jiraItemFactory(Env().jiraProject, "test_canRemoveAllStoriesFromJira-1", "can delete this?")
        tracker.update(item)
        item.withSummary("test_canRemoveAllStoriesFromJira-2")
        tracker.update(item)
        tracker.deleteAllItems()
        self.assertRaises(StopIteration, next, tracker.items())
        
    def test_canUpdateItemAlreadyInJira(self):
        tracker = self.jira_
        item = jiraItemFactory(Env().jiraProject, "test_canUpdateItemAlreadyInJira-1", "can update this?")
        tracker.update(item)
        Testing.canUpdateItemsIn(tracker, self)        
    
    def test_canAddCommentsToTicket(self):
        tracker = self.jira_
        item = jiraItemFactory(Env().jiraProject, "test_canAddCommentsToTicket-1", "can comment on this?")
        tracker.update(item)
        aComment = Testing.addCommentToItemIn(tracker)
        item = next(tracker.items())
        self.assertEqual(item.comments()[0], aComment)

    def test_canGetAvailableStatusesForJira(self):
        tracker = self.jira_
        Testing.mapStatuses(tracker)
        self.assertEqual(len(PivotalToJiraStatusMap()), 4)
        
    def test_canAdjustStateOfTicket(self):
        tracker = self.jira_
        Testing.mapStatuses(tracker)
        item = jiraItemFactory(Env().jiraProject, "test_canAdjustStateOfTicket-1", "can change the status of this ticket?")
        Testing.putItemToTrackerAndChangeStatusTo("accepted", item, tracker)
        item = next(tracker.items())
        self.assertEqual(item.status(), TrackerItemStatus("accepted"))

    def test_canFilterTicketsReturnedFromJiraSoNoMatchesAreFound(self):
        tracker = self.jira_
        item = jiraItemFactory(Env().jiraProject, "test_canFilterTicketsReturnedFromJiraSoNoMatchesAreFound", "description")
        tracker.update(item)
        forFilter = "labels = WLK"
        self.assertRaises(StopIteration, next, tracker.items(forFilter))
        
    def test_canFilterTicketsReturnedFromJiraOnlyOneMatchIsFound(self):
        tracker = self.jira_
        item = jiraItemFactory(Env().jiraProject, "test_canFilterTicketsReturnedFromJiraOnlyOneMatchIsFound", "description")
        tracker.update(item)
        searchableSummary = "searchForMe"
        forFilter = "summary ~ " + searchableSummary
        item = jiraItemFactory(Env().jiraProject, searchableSummary, "description")
        tracker.update(item)
        item = tracker.items(forFilter)
        self.assertEqual(next(item).summary(), searchableSummary)
        self.assertRaises(StopIteration, next, item)
        
    def test_ticketUpdatedWhenNotChangedDoesNotModifyTicket(self):
        tracker = self.jira_
        item = jiraItemFactory(Env().jiraProject, "test_ticketUpdatedWhenNotChangedDoesNotModifyTicket", "description")
        tracker.update(item)
        itemInJira = next(tracker.items())
        itemInJira.syncWith(itemInJira)
        tracker.update(itemInJira)
        updatedItem = next(tracker.items())
        self.assertEquals(itemInJira.updatedAt(), updatedItem.updatedAt())

    def test_canMoveNewStateToInWork(self):
        tracker = self.jira_
        Testing.mapStatuses(tracker)
        item = jiraItemFactory(Env().jiraProject, "test_canMoveNewStateToInWork-1", "can change the status to In Work?")
        Testing.putItemToTrackerAndChangeStatusTo("started", item, tracker)
        item = next(tracker.items())
        self.assertEqual(item.status(), TrackerItemStatus("started"))

    def test_pass(self):
        pass
       
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_canConnectToPivotalTrackerTestProject']
    unittest.main()
