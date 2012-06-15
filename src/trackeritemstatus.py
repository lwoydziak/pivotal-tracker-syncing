'''
Created on May 15, 2012

@author: lwoydziak
'''
from mappivotaltojirastatus import PivotalToJiraStatusMap
from defaultparameter import defaultParameter

class TrackerItemStatus(object):
    '''
    classdocs
    '''

    def __init__(self, base=None, apiObject=None):
        '''
        Constructor
        '''
        apiObject = defaultParameter(PivotalToJiraStatusMap, apiObject)
        if base is None:
            self.container_ = BaseStatus()
            return
        if isinstance(base, str):
            self.container_ = PivotalStatus(base, apiObject)
            return
        jiraStatusName = apiObject.translateStatusTo('jiraStatusName', base.status()) if base.status() != "" else None
        self.container_ = JiraStatus(jiraStatusName, apiObject)
        
    def __eq__(self, other):
        if other is self:
            return True
        if isinstance(other, self.__class__):
            return self.pivotal() == other.pivotal() and self.jira() == other.jira()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def pivotal(self):
        return self.container_.pivotal()
    
    def jira(self):
        return self.container_.jira()
    
class BaseStatus(object):
    def __init__(self, seed=None, apiObject=None):
        self.apiObject_ = apiObject
        self.seed_ = seed
        
    def pivotal(self):
        return self.seed_
    
    def jira(self):
        return self.seed_    
    
class PivotalStatus(BaseStatus):
    def jira(self):
        return self.apiObject_.translateStatusTo('jira', self.seed_)
    
class JiraStatus(BaseStatus):  
    def pivotal(self):
        return self.apiObject_.translateStatusTo('pivotal', self.seed_)

        