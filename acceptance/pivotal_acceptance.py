'''
Created on Mar 29, 2012

@author: lwoydziak
'''
import unittest
import sys
from config import Env
from acceptance_test_support import Testing, SinglePivotal
import time
sys.path.insert(0, "src")
from pivotaltrackeritem import PivotalTrackerItem
from pivotaltracker import PivotalTrackerFor
from pytracker import Story



class PivotalAcceptanceTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.pivotal_ = SinglePivotal().instance()
        pass
    
    def tearDown(self):
        self.pivotal_.deleteAllItems()
        unittest.TestCase.tearDown(self)
    
    def test_canConnectToPivotalTrackerTestProject(self):
        tracker = self.pivotal_
        self.assertTrue(tracker.valid())
        pass

    def test_canDownloadStoriesFromPivotalTracker(self):
        tracker = self.pivotal_
        item = PivotalTrackerItem().withSummary("test_canDownloadStoriesFromPivotalTracker-1")
        tracker.update(item)
        item.withSummary("test_canDownloadStoriesFromPivotalTracker-2")
        tracker.update(item)
        itemIterator = tracker.items()
        next(itemIterator)
        next(itemIterator)
        self.assertRaises(StopIteration, next, itemIterator)
        pass
    
    def test_canAddStoryToPivotal(self):
        tracker = self.pivotal_
        name = "test_canAddStoryToPivotal"
        description = "this is a test"
        item = PivotalTrackerItem(Story()).withSummary(name).withDescription(description)
        tracker.update(item)
        item = next(tracker.items())
        self.assertEqual(item.summary(), name)
        self.assertEqual(item.description(), description)
        
    def test_canRemoveAllStoriesFromPivotal(self):
        tracker = self.pivotal_
        item = PivotalTrackerItem().withSummary("test_canRemoveAllStoriesFromPivotal-1")
        tracker.update(item)
        item.withSummary("test_canRemoveAllStoriesFromPivotal-2")
        tracker.update(item)
        tracker.deleteAllItems()
        self.assertRaises(StopIteration, next, tracker.items())
        
    def test_canUpdateItemAlreadyInPivotal(self):
        tracker = self.pivotal_
        item = PivotalTrackerItem().withSummary("test_canUpdateItemAlreadyInPivotal-to update").withDescription("can update?")
        tracker.update(item)
        item = next(tracker.items())
        newSummary = "test_canUpdateItemAlreadyInPivotal-1"
        newDescription = "yep - updated"
        item.withSummary(newSummary).withDescription(newDescription)
        tracker.update(item)
        item = next(tracker.items())
        self.assertEqual(item.summary(), newSummary)
        self.assertEqual(item.description(), newDescription)
        
    def test_canAddAndUpdateJiraLinksToPivotalStories(self):
        tracker = self.pivotal_
        newUrl = "https://www.jira.com/TEST-pa1234"
        jiraTicketKey = "TEST-pa1234"
        description = "this is a test\nwith\nmultiple\nlines"
        item = PivotalTrackerItem().withSummary("test_canAddAndUpdateJiraLinksToPivotalStories").withDescription(description)
        item.withJiraUrl("http://www.jira.com/TEST-pa1234").withJiraKey(jiraTicketKey)
        tracker.update(item)
        item = next(tracker.items())
        item.withJiraUrl(newUrl)
        tracker.update(item)
        item = next(tracker.items())
        self.assertEqual(item.jiraUrl(), newUrl)
        self.assertEqual(item.jiraKey(), jiraTicketKey)
        self.assertEqual(item.description(), description)

    def test_canAddCommentsToStory(self):
        tracker = self.pivotal_
        item = PivotalTrackerItem().withSummary("test_canAddCommentsToStory").withDescription("description")
        tracker.update(item)
        aComment = Testing.addCommentToItemIn(tracker)
        item = next(tracker.items())
        self.assertEqual(item.comments()[0], aComment)
        
    def test_canFilterStoriesReturnedFromTrackerSoNoMatchesAreFound(self):
        tracker = self.pivotal_
        item = PivotalTrackerItem().withSummary("test_canFilterStoriesReturnedFromTracker").withDescription("description")
        tracker.update(item)
        forFilter = "label:garabage"
        self.assertRaises(StopIteration, next, tracker.items(forFilter))
        
    def test_canFilterStoriesReturnedFromTrackerOnlyOneMatchIsFound(self):
        tracker = self.pivotal_
        forFilter = "searchForMe"
        item = PivotalTrackerItem().withSummary(forFilter).withDescription("description")
        tracker.update(item)
        item = PivotalTrackerItem().withSummary("test_canFilterStoriesReturnedFromTrackerOnlyOneMatchIsFound").withDescription("description")
        tracker.update(item)
        time.sleep(3)
        itemIterator = tracker.items(forFilter)
        next(itemIterator)
        self.assertRaises(StopIteration, next, itemIterator)
                
    def test_storyUpdatedWhenNotChangedDoesNotModifyStory(self):
        tracker = self.pivotal_
        item = PivotalTrackerItem().withSummary("test_storyUpdatedWhenNotChangedDoesNotModifyStory").withDescription("description")
        tracker.update(item)
        itemInPivotal = next(tracker.items())
        itemInPivotal.syncWith(itemInPivotal)
        tracker.update(itemInPivotal)
        updatedItem = next(tracker.items())
        self.assertEquals(itemInPivotal.updatedAt(), updatedItem.updatedAt())         
         
    def test_canChangeStoryType(self):
        tracker = self.pivotal_
        itemType = "bug"
        item = PivotalTrackerItem().withSummary("test_canChangeStoryType-1").withDescription("can change the type of this ticket?")
        tracker.update(item)
        item = next(tracker.items())
        item.withType(itemType)
        tracker.update(item)
        updatedItem = next(tracker.items())
        self.assertEqual(itemType, updatedItem.type())

    def test_canAdjustStateOfTicket(self):
        tracker = self.pivotal_
        item = PivotalTrackerItem().withSummary("test_canAdjustStateOfTicket-1").withDescription("can change the status of this ticket?").withType("bug")  
        done = Testing.putItemToTrackerAndChangeStatusToDone(item, tracker)
        item = next(tracker.items())
        self.assertEqual(item.status(), done)        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_canConnectToPivotalTrackerTestProject']
    unittest.main()