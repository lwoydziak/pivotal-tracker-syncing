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
        self.translateToPivotalStatusFrom_ = {}
        self.translateStatusTo_ = {'jira': {}, 'pivotal' : {}, 'jiraStatusName': {}}
         
    def addMapping(self, jira, pivotal):
        self.translateToPivotalStatusFrom_[jira] = pivotal
        
    def _insert(self, jiraStatus):
        try:
            pivotalStatus = self._getPivotalStatusMappingFor(jiraStatus.name)
        except KeyError:
            return
        self.translateStatusTo_['jira'][pivotalStatus] = jiraStatus.name
        self.translateStatusTo_['pivotal'][jiraStatus.name] = pivotalStatus
        self.translateStatusTo_['jiraStatusName'][jiraStatus.id] = jiraStatus.name
    
    def insert(self, jiraStatus):
        if isinstance(jiraStatus, list):
            for status in jiraStatus:
                self._insert(status)
            return
        self._insert(jiraStatus)
        
    def _getPivotalStatusMappingFor(self, jiraStatusName):
        return self.translateToPivotalStatusFrom_[jiraStatusName]
        
    def translateStatusTo(self, kind, fromStatusToTranslate):
        if len(self) == 0:
            return None
        try:
            status = self.translateStatusTo_[kind][fromStatusToTranslate]
        except KeyError:
            return None
        return status
    
    def __len__(self):
        return len(self.translateStatusTo_['pivotal'])