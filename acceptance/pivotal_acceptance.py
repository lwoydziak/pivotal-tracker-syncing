'''
Created on Mar 29, 2012

@author: lwoydziak
'''
import unittest
import sys
from config import Env
from acceptance_test_support import Testing
sys.path.insert(0, "src")
from pivotaltrackeritem import PivotalTrackerItem
from pivotaltracker import PivotalTrackerFor
from pytracker import Story



class PivotalAcceptanceTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        tracker = PivotalTrackerFor(Env().pivotalTrackerProject)
        tracker.loginAs(Env().pivotalTrackerUsername).withCredential(Env().pivotalTrackerPassword)
        self.pivotal_ = tracker
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
    
    def test_canAddStoryStoryToPivotal(self):
        tracker = self.pivotal_
        name = "test_canAddStoryStoryToPivotal"
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
        item = PivotalTrackerItem().withSummary("test_canAddAndUpdateJiraLinksToPivotalStories").withDescription("description")
        item.withJiraUrl("http://www.jira.com/TEST-pa1234").withJiraKey(jiraTicketKey)
        tracker.update(item)
        item = next(tracker.items())
        item.withJiraUrl(newUrl)
        tracker.update(item)
        item = next(tracker.items())
        self.assertEqual(item.jiraUrl(), newUrl)
        self.assertEqual(item.jiraKey(), jiraTicketKey)

    def test_canAddCommentsToStory(self):
        tracker = self.pivotal_
        item = PivotalTrackerItem().withSummary("test_canAddCommentsToStory").withDescription("description")
        tracker.update(item)
        aComment = Testing.addCommentToItemIn(tracker)
        item = next(tracker.items())
        self.assertEqual(item.comments()[0], aComment)  
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_canConnectToPivotalTrackerTestProject']
    unittest.main()