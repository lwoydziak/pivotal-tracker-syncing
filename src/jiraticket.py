'''
Created on Apr 10, 2012

@author: lwoydziak
'''
from jiraremotestructures import RemoteIssue
from defaultparameter import defaultParameter

class JiraTicket(object):
    '''
    classdocs
    '''


    def __init__(self, details=None):
        '''
        Constructor
        '''
        self.details_ = defaultParameter(RemoteIssue, details)
    
    def summary(self):
        return self.details_.summary
    
    def setSummary(self, summary):
        self.details_.summary = summary
    
    def description(self):
        return self.details_.description
    
    def setDescrition(self, description):
        self.details_.description = description
    
    def Id(self):
        return self.details_.key

    
    def asDictionary(self):
        return self.details_.__dict__
    
    def setStatus(self, statusId):
        self.details_.status = statusId

    def status(self):
        return self.details_.status

    def updatedAt(self):
        return self.details_.updated
    
    
    

    
    
    
    
    
    
    
    
        