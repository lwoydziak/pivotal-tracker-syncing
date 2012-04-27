'''
Created on Apr 10, 2012

@author: lwoydziak
'''
from trackeritem import TrackerItem
from jiraticket import JiraTicket

class JiraTrackerItem(TrackerItem):
    '''
    classdocs
    '''
    def __init__(self, ticket=None):
        '''
        Constructor
        '''
        self.piecesToUpdate_ = []
        self._addTicket(ticket)
        self.withDescription(self.ticket_.description())
        self.withSummary(self.ticket_.summary())
        self.piecesToUpdate_ = []
        self.newComments_ = []
        self.exisitingComments_ = []
        
        
    def _addTicket(self, ticket):
        if ticket is None:
            self.ticket_ = JiraTicket()
            return
        if isinstance(ticket, JiraTicket):
            self.ticket_ = ticket
            return
        self.ticket_ = JiraTicket(ticket)        
        
    def underlying(self):
        return self.ticket_ 
    
    def withSummary(self, summary):
        super(JiraTrackerItem, self).withSummary(summary)
        self.ticket_.setSummary(summary)
        self.piecesToUpdate_.append({'id':"summary", 'values':[summary,]})
        return self
    
    def withDescription(self, description):
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

    
    def addComment(self, newComment):
        if isinstance(newComment,str):
            self.newComments_.append(newComment)
            return
        self.exisitingComments_.append(newComment)
        
    
    def comments(self):
        return self.exisitingComments_

    
    def newComments(self):
        return self.newComments_

    def withNewComments(self, commentsToCopy):
        self.newComments_ = commentsToCopy
        return self
    
    
    
    
    
    
    
    
    
    
    
    
    
    
