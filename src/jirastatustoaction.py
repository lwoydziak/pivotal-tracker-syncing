'''
Created on Jun 14, 2012

@author: lwoydziak
'''
from collections import namedtuple

class JiraStatusToAction(object):
    '''
    classdocs
    '''


    def __init__(self, status, actions):
        '''
        Constructor
        '''
        DefaultAction = namedtuple("DefaultAction", ["id"])
        self.action_ = DefaultAction(None)
        
        if actions is None:
            return
        
        statuses = status.jira()
        if statuses is None:
            return
        
        for action in actions:
            for status in statuses:
                if str(status) in str(action.name):
                    self.action_ = action
                    return
        
    def Id(self):
        return self.action_.id
        