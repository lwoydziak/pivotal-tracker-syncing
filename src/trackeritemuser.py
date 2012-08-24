'''
Created on Jun 28, 2012

@author: lwoydziak
'''
from mapusers import PivotalToJiraUserMap
from defaultparameter import defaultParameter

class BaseUser(object):
    def __init__(self, seed=None, apiObject=None):
        self.apiObject_ = defaultParameter(PivotalToJiraUserMap, apiObject)
        self.seed_ = seed
        
    def pivotal(self):
        return self.seed_
    
    def jira(self):
        return self.seed_
    
    def __eq__(self, other):
        if other is self:
            return True
        if isinstance(other, BaseUser):
            if self.pivotal() == other.pivotal():
                return self.jira() == other.jira()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def unknown(self):
        if self.jira() is None and self.pivotal() is None:
            return False
        if self.jira() is None or self.pivotal() is None:
            return True
        return False   
    
class PivotalUser(BaseUser):
    def jira(self):
        return self.apiObject_.translateUserTo('jira', self.seed_)
    
class JiraUser(BaseUser):  
    def pivotal(self):
        return self.apiObject_.translateUserTo('pivotal', self.seed_)
        