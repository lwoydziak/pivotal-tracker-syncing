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
    MAX_COMMENT_LENGTH = 20001

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
    
    def _getItems(self, forFilter=None):
        times = 3
        while times > 0:
            stories = self._tryToGetStories(forFilter)
            if stories is not "garbage":
                break
            times = times-1
        for story in stories:
            yield self._convertToItem(PivotalTrackerItem, story)
    
    def _tryToGetStories(self, forFilter=None):
        try: 
            stories = self.trackerInstance_.GetStories(forFilter)
        except Exception:
            return "garbage"
        return stories
    
    
    def update(self, item):
        super(PivotalTrackerFor, self).update(item)
        if (item.Id() is None):
            story = self.trackerInstance_.AddNewStory(item.decoratedStory())
        else:
            story = self.trackerInstance_.UpdateStory(item.decoratedStory())
        updatedItem = PivotalTrackerItem(story).withComments(item.comments('new'))
        self.updateCommentsFor(updatedItem)        
        
    def _deleteById(self, itemId):
        if itemId is None:
            return
        self.trackerInstance_.DeleteStory(itemId)
    
    def addCommentsTo(self, item):
        comments = self.trackerInstance_.GetComments(item.Id())
        for comment in comments:
            item.addComment(comment.GetText(), 'existing')
        return item
    
    def updateCommentsFor(self, item):
        for comment in item.comments('new'):
            if len(comment) < self.MAX_COMMENT_LENGTH:
                self.trackerInstance_.AddComment(item.Id(), comment)
