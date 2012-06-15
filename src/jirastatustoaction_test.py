'''
Created on Jun 14, 2012

@author: lwoydziak
'''
import unittest
from jirastatustoaction import JiraStatusToAction
from mockito.mocking import mock
from mockito.mockito import when


class JiraStatusToActionTest(unittest.TestCase):


    def test_whenStatusCanBeMatchedToActionThenReturnActionId(self):
        status = mock()
        potentialAction = mock()
        actions = [potentialAction, ]
        when(status).jira().thenReturn(str(potentialAction.name))
        action = JiraStatusToAction(status, actions)
        self.assertEqual(str(potentialAction.id), str(action.Id()))
        pass
    
    def test_whenNoActionsGivenActionIdIsNone(self):
        status = mock()
        action = JiraStatusToAction(status, None)
        self.assertEqual(None, action.Id())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()