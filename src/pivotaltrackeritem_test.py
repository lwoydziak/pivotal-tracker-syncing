'''
Created on Apr 9, 2012

@author: lwoydziak
'''
import unittest
from pivotaltrackeritem import PivotalTrackerItem
from pytracker import Story
from mockito.mocking import mock
from mockito.mockito import when
from datetime import timedelta
from timezoneutc import UTC


class PivotalTrackerItem_Tests(unittest.TestCase):
    def test_changingSummaryChangesPivotalStorySummary(self):
        item = PivotalTrackerItem()
        summary = "New"
        returnedItem = item.withSummary(summary)
        self.assertEqual(item.underlying().GetName(), summary)
        self.assertEqual(returnedItem, item)
        storyToUpdate = returnedItem.decoratedStory()
        self.assertEqual(summary, storyToUpdate.GetName())
        self.assertTrue('name' in storyToUpdate.UPDATE_FIELDS)
        pass
    
    def test_whenTryingToChangeStatusToDuplicateStatusNoUpdateIsMade(self):
        summary = "summary"
        story = Story()
        story.SetName(summary)
        item = PivotalTrackerItem(story)
        item.withSummary(summary)
        storyToUpdate = item.decoratedStory()
        self.assertEqual(None, storyToUpdate.GetName())
        self.assertEqual([], storyToUpdate.UPDATE_FIELDS)
    
    def test_changingDescriptionChangesPivotalStoryDescription(self):
        item = PivotalTrackerItem()
        description = "New"
        returnedItem = item.withDescription(description)
        self.assertEqual(item.underlying().GetDescription(), description)
        self.assertEqual(returnedItem, item)
        storyToUpdate = returnedItem.decoratedStory()
        self.assertEqual(description, storyToUpdate.GetDescription())
        self.assertTrue('description' in storyToUpdate.UPDATE_FIELDS)
        pass
    
    def test_whenTryingToChangeDescriptionToDuplicateDescriptionNoUpdateIsMade(self):
        description = "description"
        story = Story()
        story.SetDescription(description)
        item = PivotalTrackerItem(story)
        item.withDescription(description)
        storyToUpdate = item.decoratedStory()
        self.assertEqual(None, storyToUpdate.GetDescription())
        self.assertEqual([], storyToUpdate.UPDATE_FIELDS)
    
    def test_canGetId(self):
        story = Story()
        story.story_id = 1234
        item = PivotalTrackerItem(story)
        self.assertEqual(item.Id(), story.story_id)
        pass
    
    def test_summaryAndDescriptionValidForItemWhenSeededWithExistingValidStorySummaryAndDescription(self):
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
        storyToUpdate = item.decoratedStory()
        self.assertEqual(updateUrl+"\nNone", storyToUpdate.GetDescription())
        self.assertTrue('description' in storyToUpdate.UPDATE_FIELDS)
        
    def test_doNotUpdateJiraUrlOnStoryWhenUpdatedWithDuplicate(self):
        story = Story()
        updateUrl = "http://www.updated.com"
        story.jira_url = updateUrl
        item = PivotalTrackerItem(story)
        item.withJiraUrl(updateUrl)
        storyToUpdate = item.decoratedStory()
        self.assertEqual(None, storyToUpdate.GetDescription())
        self.assertEqual([], storyToUpdate.UPDATE_FIELDS)
        
    def test_canUpdateJiraKeyOnStory(self):
        story = Story()
        story.jira_id = "TEST-pti1234"
        updateJiraId = "TEST-12345"
        item = PivotalTrackerItem(story)
        item.withJiraKey(updateJiraId)
        self.assertEqual(item.jiraKey(), updateJiraId)
        storyToUpdate = item.decoratedStory()
        self.assertEqual("[" + updateJiraId + "]: None", storyToUpdate.GetName())
        self.assertTrue('name' in storyToUpdate.UPDATE_FIELDS)
        
    def test_doNotUpdateJiraKeyOnStoryWhenUpdatedWithDuplicate(self):
        story = Story()
        updateJiraId = "TEST-12345"
        story.jira_id = updateJiraId
        item = PivotalTrackerItem(story)
        item.withJiraKey(updateJiraId)
        storyToUpdate = item.decoratedStory()
        self.assertEqual(None, storyToUpdate.GetName())
        self.assertEqual([], storyToUpdate.UPDATE_FIELDS)
        
    def test_storyCanBeSyncedWithJiraItem(self):
        item = PivotalTrackerItem()
        toSyncWith = mock()
        when(toSyncWith).canBeSyncedWith(item).thenReturn(True)
        self.assertTrue(item.canBeSyncedWith(toSyncWith))
        
    def test_storyCannotBeSyncedWithJiraItem(self):
        item = PivotalTrackerItem()
        toSyncWith = mock()
        when(toSyncWith).canBeSyncedWith(item).thenReturn(False)
        self.assertFalse(item.canBeSyncedWith(toSyncWith))
        
    def test_itemWithoutJiraInfoDoesNotDecorate(self):
        item = PivotalTrackerItem(Story())
        description = "description"
        summary = "summary"
        item.withDescription(description)
        item.withSummary(summary)
        self.assertEqual(item.decoratedStory().GetDescription(), description)
        self.assertEqual(item.decoratedStory().GetName(), summary)
                
    def test_canDecorateStorySummaryWithJiraInfo(self):
        item = PivotalTrackerItem()
        jiraKey = "TEST-pti1234"
        summary = "summary"
        decoratedSummary = "[TEST-pti1234]: summary"
        item.withSummary(summary)
        item.withJiraKey(jiraKey)
        self.assertEqual(item.decoratedStory().GetName(), decoratedSummary)

    def test_canDecorateStoryDescriptionWithJiraInfo(self):
        item = PivotalTrackerItem()
        jiraUrl = "https://www.jira.com/browse/TEST-pti1234"
        description = "description"
        decoratedDescription = "https://www.jira.com/browse/TEST-pti1234\ndescription"
        item.withDescription(description)
        item.withJiraUrl(jiraUrl)
        self.assertEqual(item.decoratedStory().GetDescription(), decoratedDescription)
        
    def test_itemConstructedWithDecoratedStoryWithJiraKeyGetsValidSummary(self):
        story = Story()
        jiraKey = "TEST-pti1234"
        summary = "summary"
        decoratedSummary = "[TEST-pti1234]: summary"
        story.SetName(decoratedSummary)
        item = PivotalTrackerItem(story)
        self.assertEqual(item.summary(), summary)
        self.assertEqual(item.jiraKey(), jiraKey)
    
    def test_itemConstructedWithDecoratedStoryWithJiraKeyGetsValidDescriptionWithHTTP(self):
        story = Story()
        jiraUrl = "http://www.jira.com/TEST-pa1234"
        description = "this is a test\nwith\nmultiple\nlines"
        decoratedDescription = "http://www.jira.com/TEST-pa1234\n" + description
        story.SetDescription(decoratedDescription)
        item = PivotalTrackerItem(story)
        self.assertEqual(item.description(), description)
        self.assertEqual(item.jiraUrl(), jiraUrl)
        
    def test_itemConstructedWithDecoratedStoryWithJiraKeyGetsValidDescriptionWithHTTPS(self):
        story = Story()
        jiraUrl = "https://www.jira.com/TEST-pa1234"
        description = "this is a test\nwith\nmultiple\nlines" 
        decoratedDescription = "https://www.jira.com/TEST-pa1234\n" + description
        story.SetDescription(decoratedDescription)
        item = PivotalTrackerItem(story)
        self.assertEqual(item.description(), description)
        self.assertEqual(item.jiraUrl(), jiraUrl)
        
    def test_previouslyExistingJiraInformationIsNotOverwritternBecauseDecoratedStoryDoesNotYetContainIt(self):
        story = Story()
        jiraId = "blah"
        jiraUrl = "blah2"
        story.jira_id = jiraId
        story.jira_url = jiraUrl
        story.SetName("name")
        story.SetDescription("description")
        item = PivotalTrackerItem(story)
        self.assertEqual(item.jiraKey(), jiraId)
        self.assertEqual(item.jiraUrl(), jiraUrl)
        
    def test_cannotSyncWithNoItem(self):
        item = PivotalTrackerItem()
        self.assertFalse(item.canBeSyncedWith(None))
        
    def test_canGetTimeUpdatedAt(self):
        story = Story()
        story.updated_at = 1240433216
        timezone = UTC()
        item = PivotalTrackerItem(story, timezone)
        self.assertEqual("2009/04/22 20:46:56", item.updatedAt().strftime("%Y/%m/%d %H:%M:%S"))
        self.assertEqual(None, item.updatedAt().tzinfo)
        
    def test_whenCommentAddedStoryIsAvailableToUpdate(self):
        story = Story()
        story.story_id = 1234
        item = PivotalTrackerItem(story)
        comment = "blah"
        item.addComment(comment)
        storyToBeUpdated = item.decoratedStory()
        self.assertEqual(story.story_id, storyToBeUpdated.GetStoryId())
        
    def test_canSetStatusForStory(self):
        story = Story()
        startingStatus = "unscheduled"
        story.SetCurrentState(startingStatus)
        accepted = "Accepted"
        item = PivotalTrackerItem(story)
        self.assertEqual(startingStatus, item.status().pivotal())
        status = mock()
        when(status).pivotal().thenReturn(accepted)
        item.withStatus(status)
        self.assertEqual(story.GetCurrentState(), accepted)
        self.assertEqual(status, item.status())
        self.assertTrue('current_state' in item.decoratedStory().UPDATE_FIELDS)
        
    def test_cannotSetDuplicateStatusForStory(self):
        story = Story()
        startingStatus = "unscheduled"
        story.SetCurrentState(startingStatus)
        item = PivotalTrackerItem(story)
        item.withStatus(item.status())
        self.assertEqual(startingStatus, item.status().pivotal())
        self.assertEqual([], item.decoratedStory().UPDATE_FIELDS)
        
    def test_cannotAddNoneStatus(self):
        story = Story()
        startingStatus = "unscheduled"
        story.SetCurrentState(startingStatus)
        item = PivotalTrackerItem(story)
        item.withStatus(None)
        self.assertEqual(startingStatus, item.status().pivotal())
        self.assertEqual([], item.decoratedStory().UPDATE_FIELDS)
        
        
    def test_canSetTypeForStory(self):
        story = Story()
        defaultStoryType = "feature"
        story.SetStoryType(defaultStoryType)
        item = PivotalTrackerItem(story)
        self.assertEqual(defaultStoryType, item.type())
        type = "bug"
        item.withType(type)
        self.assertEqual(story.GetStoryType(), type)
        self.assertEqual(type, item.type())
        self.assertTrue('story_type' in item.decoratedStory().UPDATE_FIELDS)
        
    def test_cannotSetDuplicateTypeForStory(self):
        story = Story()
        defaultStoryType = "feature"
        story.SetStoryType(defaultStoryType)
        item = PivotalTrackerItem(story)
        item.withType(item.type())
        self.assertEqual(defaultStoryType, item.type())
        self.assertEqual([], item.decoratedStory().UPDATE_FIELDS)
        
    def test_cannotSetNoneTypeForStory(self):
        story = Story()
        defaultStoryType = "feature"
        story.SetStoryType(defaultStoryType)
        item = PivotalTrackerItem(story)
        item.withType(None)
        self.assertEqual(story.GetStoryType(), defaultStoryType)
        self.assertEqual([], item.decoratedStory().UPDATE_FIELDS)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()