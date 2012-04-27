'''
Created on Mar 29, 2012

@author: lwoydziak
'''
import unittest
import sys
from config import Env
from jiraitemfactory import jiraItemFactory
sys.path.insert(0, "src")
from jiratracker import JiraTracker


class JiraAccpetanceTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        tracker = JiraTracker(Env().jiraUrl)
        tracker.loginAs(Env().jiraUsername).withCredential(Env().jiraPassword)
        tracker.selectProject([Env().jiraProject, Env().jiraJql])
        self.jira_ = tracker
        pass
    
    def tearDown(self):
        self.jira_.deleteAllItems()
        self.jira_.finalize()
        unittest.TestCase.tearDown(self)
    
    def test_canConnectToJira(self):
        tracker = self.jira_
        self.assertTrue(tracker.valid())
        
    def test_canDeleteJiraIssue(self):
        tracker = self.jira_
        item = jiraItemFactory(Env().jiraProject, "test_canDeleteJiraIssue", "A test description")
        tracker.update(item)
        items = tracker.items()
        tracker.delete(items[0])
        
    def test_canDownloadStoriesFromJira(self):
        tracker = self.jira_
        item = jiraItemFactory(Env().jiraProject, "test_canDownloadStoriesFromJira-1", "A test description")
        tracker.update(item)
        item.withSummary("test_canDownloadStoriesFromJira-2")
        tracker.update(item)
        stories = tracker.items()
        self.assertEqual(len(stories), 2)
        pass
    
    def test_canAddStoryStoryToJira(self):
        tracker = self.jira_
        name = "test_canAddStoryStoryToPivotal"
        description = "this is a test"
        item = jiraItemFactory(Env().jiraProject, name, description)
        tracker.update(item)
        stories = tracker.items()
        self.assertEqual(stories[0].summary(), name)
        self.assertEqual(stories[0].description(), description)
        
    def test_canRemoveAllStoriesFromJira(self):
        tracker = self.jira_
        item = jiraItemFactory(Env().jiraProject, "test_canRemoveAllStoriesFromPivotal-1", "can delete this?")
        tracker.update(item)
        item.withSummary("test_canRemoveAllStoriesFromPivotal-2")
        tracker.update(item)
        tracker.deleteAllItems()
        stories = tracker.items()
        self.assertEqual(len(stories), 0)
        
    def test_canUpdateItemAlreadyInJira(self):
        tracker = self.jira_
        item = jiraItemFactory(Env().jiraProject, "test_canUpdateItemAlreadyInJira-1", "can update this?")
        tracker.update(item)
        items = tracker.items()
        newSummary = "test_canUpdateItemAlreadyInJira-1"
        newDescription = "yep - updated"
        items[0].withSummary(newSummary).withDescription(newDescription)
        tracker.update(items[0])
        items = tracker.items()
        self.assertEqual(items[0].summary(), newSummary)
        self.assertEqual(items[0].description(), newDescription)
    
    def test_canAddCommentsToTicket(self):
        tracker = self.jira_
        item = jiraItemFactory(Env().jiraProject, "test_canAddCommentsToTicket-1", "can comment on this?")
        tracker.update(item)
        items = tracker.items()
        aComment = "I am adding this comment"
        items[0].addComment(aComment)
        tracker.update(items[0])
        items = tracker.items()
        self.assertEqual(items[0].comments()[0]['body'], aComment)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_canConnectToPivotalTrackerTestProject']
    unittest.main()
