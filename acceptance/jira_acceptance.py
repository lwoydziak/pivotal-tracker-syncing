'''
Created on Mar 29, 2012

@author: lwoydziak
'''
import unittest
import sys
from config import Env
from acceptance_test_support import Testing
from jiraitemfactory import jiraItemFactory
sys.path.insert(0, "src")
from jiratracker import JiraTracker
from mappivotaltojirastatus import PivotalToJiraStatusMap


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
        statuses = tracker.getAvailableStatuses()
        PivotalToJiraStatusMap().addMapping(jira="Closed", pivotal="Accepted")
        PivotalToJiraStatusMap().insert(statuses)
        self.assertEqual(len(PivotalToJiraStatusMap()), 1)
        
#    def test_canAdjustStateOfTicket(self):
#        tracker = self.jira_
#        item = jiraItemFactory(Env().jiraProject, "test_canAdjustStateOfTicket-1", "can comment on this?")
#        tracker.update(item)
#        item = next(tracker.items())
#        status = InTest()
#        item.withStatus(status)
#        tracker.update(item)
#        item = next(tracker.items())
#        self.assertEqual(item.status(), status)
       
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_canConnectToPivotalTrackerTestProject']
    unittest.main()
