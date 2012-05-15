'''
Created on Mar 24, 2012

@author: lwoydziak
'''
import unittest
from pivotaltracker import PivotalTrackerFor
from mockito.mockito import verify, when
from mockito.mocking import mock
from mockito.matchers import any
from pytracker import Story, Comment
from mockito.verification import never
from datetime import datetime
from pivotaltrackeritem import PivotalTrackerItem
from mockito import inorder
from unit_test_support import Testing


class PivotalTrackerTest(unittest.TestCase):
    def makeTestTracker(self):
        myProject = 12345
        self.apiObject_ = mock()
        tracker = PivotalTrackerFor(myProject)
        tracker.apiObject(self.apiObject_)
        return tracker

    def test_canConstructTracker(self):
        tracker = self.makeTestTracker()
        self.assertEqual(type(tracker), PivotalTrackerFor)
        pass
    
    def test_canSetPassword(self):
        tracker = self.makeTestTracker()
        pivotalApiObject = self.apiObject_
        password = "pass"
        tracker.withCredential(password)
        verify(pivotalApiObject).HostedTrackerAuth("None",password)
    
    def test_canGetPivotalProject(self):
        tracker = self.makeTestTracker()
        pivotalApiObject = self.apiObject_
        myProject = 12345
        tracker.selectProject(myProject)
        verify(pivotalApiObject).Tracker(myProject, any())
    
    def test_whenDoingPivotalOperationAuthenticationIsIncluded(self):
        tracker = self.makeTestTracker()
        pivotalApiObject = self.apiObject_
        password = "pass"
        authentication = mock()
        when(pivotalApiObject).HostedTrackerAuth(any(),any()).thenReturn(authentication)
        tracker.withCredential(password)
        verify(pivotalApiObject).Tracker(any(), authentication)
        
    def test_canGetStoriesFromProject(self):
        tracker = self.makeValidTracker()
        trackerInstance = self.trackerInstance_
        when(trackerInstance).GetStories().thenReturn([Story(),Story()])
        when(trackerInstance).GetComments(any()).thenReturn([])
        itemIterator = tracker.items()
        next(itemIterator)
        next(itemIterator)
        self.assertRaises(StopIteration, next, itemIterator)
        
    def test_trackerValidAfterLogin(self):
        tracker = self.makeTestTracker()
        pivotalApiObject = self.apiObject_
        trackerInstance = mock()
        when(pivotalApiObject).Tracker(any(),any()).thenReturn(trackerInstance)
        user = "lukewoydziak"
        password = "pass"
        tracker.loginAs(user).withCredential(password)
        self.assertTrue(tracker.valid())
        
    def makeValidTracker(self):
        tracker = self.makeTestTracker()
        pivotalApiObject = self.apiObject_
        trackerInstance = mock()
        when(pivotalApiObject).Tracker(any(),any()).thenReturn(trackerInstance)
        pivotalProjectNumber = 0
        tracker.selectProject(pivotalProjectNumber)
        self.trackerInstance_ = trackerInstance
        return tracker
        
    def test_trackerCanAddItem(self):
        tracker = self.makeValidTracker()
        trackerInstance = self.trackerInstance_
        pivotalTrackerItem = mock()
        story = mock()
        when(pivotalTrackerItem).decoratedStory().thenReturn(story)
        when(pivotalTrackerItem).Id().thenReturn(None)
        when(trackerInstance).AddNewStory(any()).thenReturn(mock())
        when(pivotalTrackerItem).comments('new').thenReturn([])
        tracker.update(pivotalTrackerItem)
        verify(trackerInstance).AddNewStory(story)
        pass
    
    def test_trackerCanDeleteItem(self):
        tracker = self.makeValidTracker()
        trackerInstance = self.trackerInstance_
        pivotalTrackerItem = mock()
        storyId = 1234
        when(pivotalTrackerItem).Id().thenReturn(storyId)
        tracker.delete(pivotalTrackerItem)
        verify(trackerInstance).DeleteStory(storyId)
        pass
    
    def test_dontDeleteNotAddedItem(self):
        tracker = self.makeValidTracker()
        trackerInstance = self.trackerInstance_
        pivotalTrackerItem = mock()
        when(pivotalTrackerItem).Id().thenReturn(None)
        tracker.delete(pivotalTrackerItem)
        verify(trackerInstance, never).DeleteStory(any())
        pass
    
    def test_canDeleteAllItems(self):
        tracker = self.makeValidTracker()
        trackerInstance = self.trackerInstance_
        item1 = Story()
        item1.story_id = 1234
        item2 = Story()
        item2.story_id = 12345
        when(trackerInstance).GetStories().thenReturn([item1,item2])
        when(trackerInstance).GetComments(any()).thenReturn([])
        tracker.deleteAllItems()
        verify(trackerInstance).DeleteStory(item1.story_id)
        verify(trackerInstance).DeleteStory(item2.story_id)
        pass
    
    def test_noDeletionsWhenNoItems(self):
        tracker = self.makeValidTracker()
        trackerInstance = self.trackerInstance_
        when(trackerInstance).GetStories().thenReturn([])
        tracker.deleteAllItems()
        verify(trackerInstance, never).DeleteStory(any())
        pass
    
    def test_canUpdateExistingStory(self):
        tracker = self.makeValidTracker()
        trackerInstance = self.trackerInstance_
        pivotalTrackerItem = mock()
        story = mock()
        storyId = 12345
        when(pivotalTrackerItem).decoratedStory().thenReturn(story)
        when(pivotalTrackerItem).Id().thenReturn(storyId)
        when(trackerInstance).AddNewStory(any()).thenReturn(mock())
        when(pivotalTrackerItem).comments('new').thenReturn([])
        when(trackerInstance).UpdateStory(any()).thenReturn(mock())
        tracker.update(pivotalTrackerItem)
        verify(trackerInstance).UpdateStory(story)
        pass
    
    def test_retryWhenTryingToGetStoriesAndException(self):
        tracker = self.makeValidTracker()
        trackerInstance = self.trackerInstance_
        when(trackerInstance).GetStories().thenRaise(Exception("")).thenReturn([Story(),Story()])
        when(trackerInstance).GetComments(any()).thenReturn([])
        next(tracker.items())
        verify(trackerInstance, times=2).GetStories()
        
    def test_canGetCommentsForTicket(self):
        tracker = self.makeValidTracker()
        trackerInstance = self.trackerInstance_
        story = mock()
        storyId = "12345"
        comment1 = Comment()
        comment1.text = "Comment 1"
        comment2 = Comment()
        comment2.text = "Comment 2"
        twoComments = [comment1, comment2]
        when(story).Id().thenReturn(storyId)
        when(trackerInstance).GetComments(any()).thenReturn(twoComments)
        tracker.updateItemWithComments(story)
        verify(trackerInstance).GetComments(storyId)
        inorder.verify(story).Id()
        inorder.verify(story).addComment(twoComments[0].GetText(), 'existing')
        inorder.verify(story).addComment(twoComments[1].GetText(), 'existing')
        pass
    
    def itemWithComments(self, testing):
        issue = Story()
        issue.story_id = "1234"
        return testing.itemWithCommentsOfType(PivotalTrackerItem, issue)
        
    def test_canAddCommentsToStoryTicket(self):
        tracker = self.makeValidTracker()
        trackerInstance = self.trackerInstance_
        testing = Testing()
        item = self.itemWithComments(testing)
        tracker.updateCommentsFor(item)
        inorder.verify(trackerInstance).AddComment(testing.issue.GetStoryId(), testing.comment1)
        inorder.verify(trackerInstance).AddComment(testing.issue.GetStoryId(), testing.comment2)
        pass
    
    def test_updateAddsNewComments(self):
        tracker = self.makeValidTracker()
        trackerInstance = self.trackerInstance_
        updatedStory = mock()
        testing = Testing()
        item = self.itemWithComments(testing)
        when(trackerInstance).UpdateStory(any()).thenReturn(updatedStory)
        when(updatedStory).GetName().thenReturn("")
        tracker.update(item)
        verify(trackerInstance, times=2).AddComment(any(), any())
        pass
    
    def test_gettingItemAlsoGetsCommentsForItem(self):
        tracker = self.makeValidTracker()
        trackerInstance = self.trackerInstance_
        story1 = Story()
        story1.story_id = 1234
        story2 = Story()
        story2.story_id = 1235
        when(trackerInstance).GetStories().thenReturn([story1,story2])
        when(trackerInstance).GetComments(any()).thenReturn([])
        itemIterator = tracker.items()
        next(itemIterator)
        next(itemIterator)
        inorder.verify(trackerInstance).GetStories()
        inorder.verify(trackerInstance).GetComments(story1.GetStoryId())
        inorder.verify(trackerInstance).GetComments(story2.GetStoryId())
        
    def test_doNotAddCommentsGreaterThan20000Characters(self):
        tracker = self.makeValidTracker()
        trackerInstance = self.trackerInstance_
        testing = Testing()
        item = self.itemWithComments(testing)
        item.addComment(Testing.stringOfAsOfSize(20002))
        tracker.updateCommentsFor(item)
        verify(trackerInstance, times=2).AddComment(any(), any())
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()