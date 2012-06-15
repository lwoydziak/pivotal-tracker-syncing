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
        if actions is None:
            DefaultAction = namedtuple("DefaultAction", ["id"])
            self.action_ = DefaultAction(None)
            return
        
        for action in actions:
            if status.jira() in str(action.name):
                self.action_ = action
                break
        
    def Id(self):
        return self.action_.id
        