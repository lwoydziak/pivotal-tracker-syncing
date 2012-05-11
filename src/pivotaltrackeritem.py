'''
Created on Apr 7, 2012

@author: lwoydziak
'''
from trackeritem import TrackerItem
from pytracker import Story
from copy import deepcopy
import re

class PivotalTrackerItem(TrackerItem):
    '''
    classdocs
    '''

    def __init__(self, story=Story() ):
        '''
        Constructor
        '''
        super(PivotalTrackerItem, self).__init__()
        self.story_ = story
        self._normalizeSummary(self.story_.GetName())
        self._normalizeDescription(self.story_.GetDescription())
        
    def _returnRegexMatch(self, regex, subject):    
        match1 = subject
        match2 = None
        regex = re.compile(regex) 
        matches = regex.match(subject)
        if matches is not None:
            match1 = matches.group(2)
            match2 = matches.group(1)
        return match1, match2
            
    def _normalizeSummary(self, summary):
        summary, jiraKey  = self._returnRegexMatch('\[(.*)\]: (.+)', str(summary)) #regex to match everything after [<other tracker id>]:
        if summary is not None:
            self.withSummary(summary)
        if jiraKey is not None:
            self.withJiraKey(jiraKey)
        
    def _normalizeDescription(self, description):
        description, jiraUrl = self._returnRegexMatch('(https://.+)[\n|\r](.*)', str(description)) #regex to match everything after https://<stuff>\n
        if description is not None:
            self.withDescription(description)
        if jiraUrl is not None:
            self.withJiraUrl(jiraUrl)
        
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

    def withJiraUrl(self, jiraUrl):
        self.story_.SetJiraUrl(jiraUrl)
        return self
    
    def jiraUrl(self):
        return self.underlying().GetJiraUrl()
    
    def withJiraKey(self, jiraKey):
        self.story_.SetJiraKey(jiraKey)
        return self
    
    def jiraKey(self):
        return self.underlying().GetJiraKey()    

    def canBeSyncedWith(self, toSyncWith):
        return toSyncWith.canBeSyncedWith(self)

    
    def decoratedStory(self):
        story = deepcopy(self.underlying())
        if self.jiraKey() is not None:
            story.SetName("[" + str(self.jiraKey()) + "]: " + str(self.summary()))
        if self.jiraUrl() is not None:
            story.SetDescription(str(self.jiraUrl()) + "\n" + str(self.description()))
        return story
    
    
    
    
        