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
        stories = tracker.items()
        self.assertEqual(len(stories), 2)
        pass
    
    def test_canAddStoryStoryToPivotal(self):
        tracker = self.pivotal_
        name = "test_canAddStoryStoryToPivotal"
        description = "this is a test"
        item = PivotalTrackerItem().withSummary(name).withDescription(description)
        tracker.update(item)
        stories = tracker.items()
        self.assertEqual(stories[0].summary(), name)
        self.assertEqual(stories[0].description(), description)
        
    def test_canRemoveAllStoriesFromPivotal(self):
        tracker = self.pivotal_
        item = PivotalTrackerItem().withSummary("test_canRemoveAllStoriesFromPivotal-1")
        tracker.update(item)
        item.withSummary("test_canRemoveAllStoriesFromPivotal-2")
        tracker.update(item)
        tracker.deleteAllItems()
        stories = tracker.items()
        self.assertEqual(len(stories), 0)
        
    def test_canUpdateItemAlreadyInPivotal(self):
        tracker = self.pivotal_
        item = PivotalTrackerItem().withSummary("test_canUpdateItemAlreadyInPivotal-to update").withDescription("can update?")
        tracker.update(item)
        items = tracker.items()
        newSummary = "test_canUpdateItemAlreadyInPivotal-1"
        newDescription = "yep - updated"
        items[0].withSummary(newSummary).withDescription(newDescription)
        tracker.update(items[0])
        items = tracker.items()
        self.assertEqual(items[0].summary(), newSummary)
        self.assertEqual(items[0].description(), newDescription)
        
    @unittest.expectedFailure
    def test_canAddAndUpdateJiraLinksToPivotalStories(self):
        tracker = self.pivotal_
        newUrl = "https://www.jira.com/TEST-pa1234"
        jiraTicketKey = "TEST-pa1234"
        item = PivotalTrackerItem().withSummary("test_canAddAndUpdateJiraLinksToPivotalStories").withDescription("description")
        item.withJiraUrl("http://www.jira.com/TEST-pa1234").withJiraKey(jiraTicketKey)
        tracker.update(item)
        items = tracker.items()
        items[0].withJiraUrl(newUrl)
        tracker.update(items[0])
        items = tracker.items()
        self.assertEqual(items[0].jiraUrl(), newUrl)
        self.assertEqual(items[0].jiraKey(), jiraTicketKey)

    def test_canAddCommentsToStory(self):
        tracker = self.pivotal_
        item = PivotalTrackerItem().withSummary("test_canAddCommentsToStory").withDescription("description")
        tracker.update(item)
        aComment = Testing.addCommentToItemIn(tracker)
        items = tracker.items()
        self.assertEqual(items[0].comments()[0], aComment)  
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_canConnectToPivotalTrackerTestProject']
    unittest.main()