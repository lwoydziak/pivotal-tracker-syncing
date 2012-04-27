'''
Created on Mar 24, 2012

@author: lwoydziak
'''
import pytracker
from tracker import Tracker
from pivotaltrackeritem import PivotalTrackerItem

class PivotalTrackerFor(Tracker):
    '''
    classdocs
    '''


    def __init__(self, projectNumber):
        '''
        Constructor
        '''
        super(PivotalTrackerFor, self).__init__()
        self.project_ = projectNumber
        self.apiObject(pytracker)
    
    def withCredential(self, password):
        super(PivotalTrackerFor, self).withCredential(password)
        self.authentication_ = self.apiObject_.HostedTrackerAuth(self.user(), self.password())
        self.selectProject(self.project_)
        
    def selectProject(self, number):
        super(PivotalTrackerFor, self).selectProject(number)
        self.trackerInstance_ = self.apiObject_.Tracker(self.project_, self.authentication_)
    
    def items(self):
        times = 3
        while times > 0:
            stories = self._tryToGetStories()
            if stories is not "garbage":
                break
            times = times-1
        return self._storiesToItems(stories)
    
    def _tryToGetStories(self):
        try: 
            stories = self.trackerInstance_.GetStories()
        except Exception:
            return "garbage"
        return stories
    
    
    def update(self, item):
        super(PivotalTrackerFor, self).update(item)
        if (item.Id() is None):
            story = self.trackerInstance_.AddNewStory(item.underlying())
        else:
            story = self.trackerInstance_.UpdateStory(item.underlying())
        return PivotalTrackerItem(story)        
        
    def _deleteById(self, itemId):
        if itemId is None:
            return
        self.trackerInstance_.DeleteStory(itemId)
        
    def _storiesToItems(self, stories):
        return self._convertToItems(PivotalTrackerItem, stories)
