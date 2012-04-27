'''
Created on Apr 7, 2012

@author: lwoydziak
'''
from trackeritem import TrackerItem
from pytracker import Story

class PivotalTrackerItem(TrackerItem):
    '''
    classdocs
    '''

    def __init__(self, story=Story() ):
        '''
        Constructor
        '''
        self.story_ = story
        self.withSummary(self.story_.GetName())
        self.withDescription(self.story_.GetDescription())
    
    def underlying(self):
        return self.story_
    
    def withSummary(self, summary):
        super(PivotalTrackerItem, self).withSummary(summary)
        self.story_.SetName(summary)
        return self
    
    def withDescription(self, description):
        super(PivotalTrackerItem, self).withDescription(description)
        self.story_.SetDescription(description)
        return self
    
    def Id(self):
        return self.underlying().GetStoryId()

    
    def withJiraUrl(self, updateUrl):
        self.story_.SetJiraUrl(updateUrl)
        return self
    
    def jiraUrl(self):
        return self.underlying().GetJiraUrl()

    
    def withJiraKey(self, updateJiraId):
        self.story_.SetJiraKey(updateJiraId)
        return self
    
    def jiraKey(self):
        return self.underlying().GetJiraKey()
    
    

    
    
    
    
    
    
    
    


    
    
    
    
        