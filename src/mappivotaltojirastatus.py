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
        self.maps_ = {'jira': {}, 'pivotal' : {}}
         
    def addMapping(self, jira, pivotal):
        self.mappings_[jira] = pivotal
        
    def _insert(self, jiraStatus):
        try:
            self.mappings_[jiraStatus.name]
        except KeyError:
            return
        self.maps_['jira'][self.mappings_[jiraStatus.name]] = jiraStatus.id
        self.maps_['pivotal'][jiraStatus.id] = self.mappings_[jiraStatus.name]
    
    def insert(self, jiraStatus):
        if isinstance(jiraStatus, list):
            for status in jiraStatus:
                self._insert(status)
            return
        self._insert(jiraStatus)
        
    def translateStatusTo(self, kind, statusToTranslate):
        return self.maps_[kind][statusToTranslate]
    
    def __len__(self):
        return len(self.maps_['pivotal'])