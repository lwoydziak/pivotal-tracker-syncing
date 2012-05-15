'''
Created on Apr 10, 2012

@author: lwoydziak
'''
from jiraremotestructures import RemoteIssue

class JiraTicket(object):
    '''
    classdocs
    '''


    def __init__(self, details=RemoteIssue()):
        '''
        Constructor
        '''
        self.details_ = details

    
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

    
    
    
    
    
    
    
    
        