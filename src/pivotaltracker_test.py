'''
Created on Mar 24, 2012

@author: lwoydziak
'''
import unittest
from pivotaltracker import PivotalTrackerFor
from mockito.mockito import verify, when
from mockito.mocking import mock
from mockito.matchers import any
from pytracker import Story
from mockito.verification import never


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
        tracker = self.makeTestTracker()
        pivotalApiObject = self.apiObject_
        trackerInstance = mock()
        when(pivotalApiObject).Tracker(any(),any()).thenReturn(trackerInstance)
        pivotalProjectNumber = 0
        tracker.selectProject(pivotalProjectNumber)
        when(trackerInstance).GetStories().thenReturn([Story(),Story()])
        items = tracker.items()
        self.assertEqual(len(items), 2)
        
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
        when(pivotalTrackerItem).underlying().thenReturn(story)
        when(pivotalTrackerItem).Id().thenReturn(None)
        when(trackerInstance).AddNewStory(any()).thenReturn(mock())
        tracker.update(pivotalTrackerItem)
        verify(trackerInstance).AddNewStory(story)
        pass
    
    def test_trackerReturnsUpdatedItemAfterAdded(self):
        tracker = self.makeValidTracker()
        trackerInstance = self.trackerInstance_
        pivotalTrackerItem = mock()
        story = mock()
        updatedTrackerItem = Story()
        updatedTrackerItem.story_id = 1234
        when(pivotalTrackerItem).underlying().thenReturn(story)
        when(pivotalTrackerItem).Id().thenReturn(None)
        when(trackerInstance).AddNewStory(any()).thenReturn(updatedTrackerItem)
        updatedItem = tracker.update(pivotalTrackerItem)
        self.assertEqual(updatedItem.underlying().GetStoryId(), updatedTrackerItem.GetStoryId())
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
        when(pivotalTrackerItem).underlying().thenReturn(story)
        when(pivotalTrackerItem).Id().thenReturn(storyId)
        when(trackerInstance).AddNewStory(any()).thenReturn(mock())
        when(trackerInstance).UpdateStory(any()).thenReturn(mock())
        tracker.update(pivotalTrackerItem)
        verify(trackerInstance).UpdateStory(story)
        pass
    
    def test_retryWhenTryingToGetStoriesAndException(self):
        tracker = self.makeTestTracker()
        pivotalApiObject = self.apiObject_
        trackerInstance = mock()
        when(pivotalApiObject).Tracker(any(),any()).thenReturn(trackerInstance)
        pivotalProjectNumber = 0
        tracker.selectProject(pivotalProjectNumber)
        when(trackerInstance).GetStories().thenRaise(Exception("")).thenReturn([Story(),Story()])
        tracker.items()
        verify(trackerInstance, times=2).GetStories()
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()