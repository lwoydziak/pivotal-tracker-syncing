'''
Created on Apr 7, 2012

@author: lwoydziak
'''
from trackeritem import TrackerItem
from pytracker import Story
from copy import deepcopy
from defaultparameter import defaultParameter
import re
from datetime import datetime
from trackeritemstatus import TrackerItemStatus

class PivotalTrackerItem(TrackerItem):
    '''
    classdocs
    '''

    def __init__(self, story=None ):
        '''
        Constructor
        '''
        super(PivotalTrackerItem, self).__init__()
        self.piecesToUpdate_ = []
        self.story_ = defaultParameter(Story, story)
        self._normalizeSummary(self.story_.GetName())
        self._normalizeDescription(self.story_.GetDescription())
        self.withStatus(TrackerItemStatus(self.story_.GetCurrentState()))
        self.withType(self.story_.GetStoryType())
        self._determineIfNeedToUpdate(story)
        
    def _determineIfNeedToUpdate(self, story):
        self.needToUpdate_ = False
        if story is None:
            self.needToUpdate_ = True
            return
        self.piecesToUpdate_ = []
        
    def _addFieldToUpdate(self, field):
        self.needToUpdate_ = True
        if field not in self.piecesToUpdate_ and field is not None:
            self.piecesToUpdate_.append(field)
    
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
        description, jiraUrl = self._returnRegexMatch('(https?://.+)[\n|\r]([\s\S]*)', str(description)) #regex to match everything after https://<stuff>\n
        if description is not None:
            self.withDescription(description)
        if jiraUrl is not None:
            self.withJiraUrl(jiraUrl)
        
    def underlying(self):
        return self.story_
    
    def withSummary(self, summary):
        if summary == self.summary():
            return self
        super(PivotalTrackerItem, self).withSummary(summary)
        self.story_.SetName(summary)
        self._addFieldToUpdate('name')
        return self
    
    def withDescription(self, description):
        if description == self.description():
            return self
        super(PivotalTrackerItem, self).withDescription(description)
        self.story_.SetDescription(description)
        self._addFieldToUpdate('description')
        return self
    
    def Id(self):
        return self.underlying().GetStoryId()

    def withJiraUrl(self, jiraUrl):
        if str(jiraUrl) == str(self.jiraUrl()):
            return self
        self.story_.SetJiraUrl(jiraUrl)
        self._addFieldToUpdate('description')
        return self
    
    def jiraUrl(self):
        return self.underlying().GetJiraUrl()
    
    def withJiraKey(self, jiraKey):
        if jiraKey == self.jiraKey():
            return self
        self.story_.SetJiraKey(jiraKey)
        self._addFieldToUpdate('name')
        return self
    
    def jiraKey(self):
        return self.underlying().GetJiraKey()    

    def canBeSyncedWith(self, toSyncWith):
        if toSyncWith is None:
            return False
        return toSyncWith.canBeSyncedWith(self)
    
    def decoratedStory(self):
        story = Story()
        if self.needToUpdate_:
            story = self._storyWithJiraInfo()        
        story.UPDATE_FIELDS = self.piecesToUpdate_
        return story
        
    def _storyWithJiraInfo(self):
        story = deepcopy(self.underlying())
        if self.jiraKey() is not None:
            story.SetName("[" + str(self.jiraKey()) + "]: " + str(self.summary()))
        if self.jiraUrl() is not None:
            story.SetDescription(str(self.jiraUrl()) + "\n" + str(self.description()))
        return story
    
    def updatedAt(self):
        return datetime.utcfromtimestamp(self.underlying().GetUpdatedAt())
    
    def addComment(self, comment, kind='new'):
        super(PivotalTrackerItem, self).addComment(comment, kind)
        if kind is 'new':
            self._addFieldToUpdate(None)
            
    def withStatus(self, status):
        if status == self.status() or status is None:
            return
        super(PivotalTrackerItem, self).withStatus(status)
        self.underlying().SetCurrentState(status.pivotal())
        self._addFieldToUpdate('current_state')
        return self
    
    def withType(self, type):
        if type == self.type() or type is None:
            return
        super(PivotalTrackerItem, self).withType(type)
        self.underlying().SetStoryType(type)
        self._addFieldToUpdate('story_type')
        return self
    
    
    
    
    
    
        