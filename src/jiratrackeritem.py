'''
Created on Apr 10, 2012

@author: lwoydziak
'''
from trackeritem import TrackerItem 
from jiraticket import JiraTicket
from trackeritemstatus import TrackerItemStatus
from defaultparameter import defaultParameter
from copy import deepcopy
from trackeritemuser import JiraUser

class JiraTrackerItem(TrackerItem):
    '''
    classdocs
    '''
    def __init__(self, ticket=None, timezone=None):
        '''
        Constructor
        '''
        super(JiraTrackerItem, self).__init__()
        self.piecesToUpdate_ = []
        self._addTicket(defaultParameter(JiraTicket, ticket))
        self.withDescription(self.ticket_.description())
        self.withSummary(self.ticket_.summary())
        self.withStatus(TrackerItemStatus(self.ticket_))
        self.withType("bug")
        self.withRequestor(JiraUser(self.ticket_.reporter()))
        self.withOwner(JiraUser(self.ticket_.assignee()))
        self.timezone_ = timezone
        self.piecesToUpdate_ = []
       
        
    def _addTicket(self, ticket):
        if isinstance(ticket, JiraTicket):
            self.ticket_ = ticket
            return
        self.ticket_ = JiraTicket(ticket)        
        
    def underlying(self):
        return self.ticket_ 
    
    def withSummary(self, summary):
        if self.summary() == summary:
            return
        super(JiraTrackerItem, self).withSummary(summary)
        self.ticket_.setSummary(summary)
        self.piecesToUpdate_.append({'id':"summary", 'values':[summary,]})
        return self
    
    def withDescription(self, description):
        if self.description() == description:
            return
        super(JiraTrackerItem, self).withDescription(description)
        self.ticket_.setDescrition(description)
        self.piecesToUpdate_.append({'id':"description", 'values':[description,]})
        return self
    
    def asRemoteItem(self):
        return self.underlying().asDictionary() 
    
    def Id(self):
        return self.underlying().Id()
    
    def piecesToUpdate(self):
        return self.piecesToUpdate_

    def withJiraUrl(self, updateUrl):
        self.url_ = updateUrl
    
    def jiraUrl(self):
        return self.url_

    def jiraKey(self):
        return self.Id()
    
    def withJiraKey(self, jiraKey):
        return
    
    def copyTypeSpecificDataTo(self, item):
        super(JiraTrackerItem, self).copyTypeSpecificDataTo(item)
        item.withJiraKey(self.jiraKey())
        item.withJiraUrl(self.jiraUrl())
    
    def canBeSyncedWith(self, toSyncWith):
        if toSyncWith is None:
            return False
        return toSyncWith.jiraKey() == self.jiraKey()
    
    def withStatus(self, status):
        if status == self.status():
            return
        super(JiraTrackerItem, self).withStatus(status)
        self.piecesToUpdate_.append({'id':"status", 'values':[self.ticket_.status(),]})
        return self
    
    def updatedAt(self):
        dateAndTime = deepcopy(self.underlying().updatedAt()).replace(tzinfo=self.timezone_)
        return self._convertToUtc(dateAndTime)
 
    def withRequestor(self, requestor):
        if self.requestor() == requestor:
            return
        if self.requestor() is not None and self.requestor().unknown():
            return
        if self.requestor() is not None and requestor.jira() is None:
            return
        
        super(JiraTrackerItem, self).withRequestor(requestor)
        self.ticket_.setReporter(requestor.jira())
        self.piecesToUpdate_.append({'id':"reporter", 'values':[requestor.jira(),]})
        return self
    
    def withOwner(self, owner):
        if self.owner() == owner:
            return
        if self.owner() is not None and self.owner().unknown():
            return
        if self.owner() is not None and owner.jira() is None:
            return
        
        super(JiraTrackerItem, self).withOwner(owner)
        self.ticket_.setAssignee(owner.jira())
        self.piecesToUpdate_.append({'id':"assignee", 'values':[owner.jira(),]})
        return self
    
    
    
    
    
    
