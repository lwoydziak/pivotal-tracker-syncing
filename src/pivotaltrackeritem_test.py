'''
Created on Apr 9, 2012

@author: lwoydziak
'''
import unittest
from pivotaltrackeritem import PivotalTrackerItem
from pytracker import Story


class PivotalTrackerItem_Tests(unittest.TestCase):
    def test_changingSummaryChangesPivotalStorySummary(self):
        item = PivotalTrackerItem()
        summary = "New"
        returnedItem = item.withSummary(summary)
        self.assertEqual(item.underlying().GetName(), summary)
        self.assertEqual(returnedItem, item)
        pass
    
    def test_changingDescriptionChangesPivotalStoryDescription(self):
        item = PivotalTrackerItem()
        description = "New"
        returnedItem = item.withDescription(description)
        self.assertEqual(item.underlying().GetDescription(), description)
        self.assertEqual(returnedItem, item)
        pass
    
    def test_canGetId(self):
        story = Story()
        story.story_id = 1234
        item = PivotalTrackerItem(story)
        self.assertEqual(item.Id(), story.story_id)
        pass
    
    def test_whenSeededWithExistingStorySummaryAndDescriptionValid(self):
        story = Story()
        description = "Hello World"
        summary = "HW"
        story.description = description
        story.name = summary
        item = PivotalTrackerItem(story)
        self.assertEqual(item.summary(), summary)
        self.assertEqual(item.description(), description)
        
    def test_canUpdateJiraUrlOnStory(self):
        story = Story()
        story.jira_url = "http://www.test.com"
        updateUrl = "http://www.updated.com"
        item = PivotalTrackerItem(story)
        item.withJiraUrl(updateUrl)
        self.assertEqual(item.jiraUrl(), updateUrl)
        
    def test_canUpdateJiraKeyOnStory(self):
        story = Story()
        story.jira_id = "TEST-1234"
        updateJiraId = "TEST-12345"
        item = PivotalTrackerItem(story)
        item.withJiraKey(updateJiraId)
        self.assertEqual(item.jiraKey(), updateJiraId)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()