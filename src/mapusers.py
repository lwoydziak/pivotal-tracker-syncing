'''
Created on Jun 28, 2012

@author: lwoydziak
'''

from singletonbase import Singleton

class PivotalToJiraUserMap(object, metaclass=Singleton):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.reset()
        
    def reset(self):
        self.translateUserTo_ = {'jira': {}, 'pivotal' : {}, 'jiraStatusName': {}}
        
    def addMapping(self, jira, pivotal):
        self.translateUserTo_['jira'][pivotal] = jira
        self.translateUserTo_['pivotal'][jira] = pivotal
        
    def translateUserTo(self, kind, fromUserToTranslate):
        if len(self) == 0:
            return None
        try:
            return self.translateUserTo_[kind][fromUserToTranslate]
        except KeyError:
            return None
        
    def __len__(self):
        return len(self.translateUserTo_['pivotal'])