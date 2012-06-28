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
        self.translateToBaseFrom_ = {}
        self.getAllAliasesFor_ = {}
        self.translateStatusTo_ = {'jira': {}, 'pivotal' : {}, 'jiraStatusName': {}}
         
    def addMapping(self, jira, pivotal=None, transitionFrom=None):
        if pivotal is None:
            pivotal = self._getPivotalStatusMappingFor(jira)
            
        if transitionFrom is None:
            self.translateToPivotalStatusFrom_[jira] = pivotal
            self.translateToBaseFrom_[jira] = jira
            return
    
        self.translateToBaseFrom_[transitionFrom] = jira
        try:
            if transitionFrom in self.getAllAliasesFor_[jira]:
                return
        except KeyError:
            self.getAllAliasesFor_[jira] = [jira]
        self.getAllAliasesFor_[jira].append(transitionFrom)  
        
    def _insert(self, jiraStatus):
        try:
            pivotalStatus = self._getPivotalStatusMappingFor(jiraStatus.name)
        except KeyError:
            return
        try:
            jiraStatuses = self.translateStatusTo_['jira'][pivotalStatus]
        except KeyError:
            try: 
                jiraStatuses = self.getAllAliasesFor_[self.translateToBaseFrom_[jiraStatus.name]]
            except KeyError:
                jiraStatuses = [jiraStatus.name]
        self.translateStatusTo_['jira'][pivotalStatus] = jiraStatuses
        self.translateStatusTo_['pivotal'][jiraStatus.name] = pivotalStatus
        self.translateStatusTo_['jiraStatusName'][jiraStatus.id] = jiraStatuses
    
    def insert(self, jiraStatus):
        if isinstance(jiraStatus, list):
            for status in jiraStatus:
                self._insert(status)
            return
        self._insert(jiraStatus)
        
    def _getPivotalStatusMappingFor(self, jiraStatusName):
        try:
            pivotalStatus = self.translateToPivotalStatusFrom_[jiraStatusName]
        except KeyError:
            jiraStatusName = self.translateToBaseFrom_[jiraStatusName]
            pivotalStatus = self.translateToPivotalStatusFrom_[jiraStatusName]
        return pivotalStatus
             
        
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