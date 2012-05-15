'''
Created on May 15, 2012

@author: lwoydziak
'''
from singletonbase import Singleton

class PivotalToJiraStatusMap(object, metaclass=Singleton):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.reset()
        
    def reset(self):
        self.mappings_ = {}
        self.jiraToPivotalMap_ = {}
        self.pivotalToJiraMap_ = {}        
         
    def addMapping(self, jira, pivotal):
        self.mappings_[jira] = pivotal
        
    def _insert(self, jiraStatus):
        try:
            self.mappings_[jiraStatus.name]
        except KeyError:
            return
        self.pivotalToJiraMap_[self.mappings_[jiraStatus.name]] = jiraStatus.id
        self.jiraToPivotalMap_[jiraStatus.id] = self.mappings_[jiraStatus.name]
    
    def insert(self, jiraStatus):
        if isinstance(jiraStatus, list):
            for status in jiraStatus:
                self._insert(status)
            return
        self._insert(jiraStatus)
        
    def getPivotalStatusFor(self, jiraStatusId):
        return self.jiraToPivotalMap_[jiraStatusId]
    
    def getJiraStatusFor(self, pivotalStatus):
        return self.pivotalToJiraMap_[pivotalStatus]
    
    def __len__(self):
        return len(self.pivotalToJiraMap_)