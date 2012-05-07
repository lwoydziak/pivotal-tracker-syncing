'''
Created on Mar 27, 2012

@author: lwoydziak
'''
import unittest
from jiratracker import JiraTracker
from mockito.mocking import mock
from mockito.mockito import verify, when
from mockito.matchers import any
from suds import WebFault
from remoteissue import RemoteIssue
from mockito.verification import never
from datetime import datetime
from jiratrackeritem import JiraTrackerItem
from mockito import inorder
from unit_test_support import Testing

class Holder(object):
    pass

class JiraTracker_Test(unittest.TestCase):
    def getMockFor(self, jira):
        jiraApiObject = mock()
        jiraInstance = Holder()
        jiraInstance.service = mock()
        jira.apiObject(jiraApiObject)
        when(jiraApiObject).Client(any(), timeout=any()).thenReturn(jiraInstance)
        self.auth_ = mock()
        when(jiraInstance.service).login(any(),any()).thenReturn(self.auth_)
        jira.withCredential("None")
        return jiraInstance

    def test_canConstructObject(self):
        jira  = JiraTracker()
        self.assertEqual(type(jira), JiraTracker)
        pass
    
    def test_jiraUrlCanBeSet(self):
        jira = JiraTracker()
        url = "http://jira.com"
        jira.setLocationTo(url)
        self.assertEqual(jira.location(),url)
        pass
    
    def test_canSetPassword(self):
        jira = JiraTracker()
        jiraApiObject = mock()
        jiraInstance = Holder()
        jiraInstance.service = mock()
        jira.apiObject(jiraApiObject)
        password = "pass"
        when(jiraApiObject).Client(any(), timeout=any()).thenReturn(jiraInstance)
        jira.withCredential(password)
        verify(jiraInstance.service).login(any(),password)
        pass
    
    def test_authSentWhenGettingBugs(self):
        jira = JiraTracker()
        jiraInstance = self.getMockFor(jira)
        when(jiraInstance.service).getIssuesFromJqlSearch(any(), any(), any()).thenReturn([])
        jira._getItems()
        verify(jiraInstance.service).getIssuesFromJqlSearch(self.auth_, any(), any())
        pass

    def test_canGetBugsForProject(self):
        jira = JiraTracker()
        jiraInstance = self.getMockFor(jira)
        project = ["test","JQL here"]
        jira.selectProject(project)
        when(jiraInstance.service).getIssuesFromJqlSearch(any(), project[1], any()).thenReturn([RemoteIssue(),RemoteIssue(),RemoteIssue()])
        bugs = jira._getItems()
        self.assertEqual(len(bugs), 3)
        pass
    
    def test_canntGetBugsForProject(self):
        jira = JiraTracker()
        jiraInstance = self.getMockFor(jira)
        jira.selectProject(["",""])
        fault = Holder()
        fault.faultstring = ""
        when(jiraInstance.service).getIssuesFromJqlSearch(any(), any(), any()).thenRaise(WebFault(fault, None))
        bugs = jira._getItems()
        self.assertEqual(len(bugs), 0)
    
    def test_finalizeLogsout(self):
        jira = JiraTracker()
        jiraInstance = self.getMockFor(jira)
        jira.finalize()
        verify(jiraInstance.service).logout(any())
        pass
    
    def test_trackerCanAddItem(self):
        jira = JiraTracker()
        jiraInstance = self.getMockFor(jira)
        trackerItem = mock()
        values = {"one" : 1, "two":2}
        when(trackerItem).Id().thenReturn(None)
        when(trackerItem).asRemoteItem().thenReturn(values)
        when(trackerItem).newComments().thenReturn([])
        jira.update(trackerItem)
        verify(jiraInstance.service).createIssue(self.auth_, values)
        pass    
    
    def test_trackerCanDeleteItem(self):
        jira = JiraTracker()
        jiraInstance = self.getMockFor(jira)
        jira.selectProject([])
        jiraTrackerItem = mock()
        itemId = 1234
        when(jiraTrackerItem).Id().thenReturn(itemId)
        jira.delete(jiraTrackerItem)
        verify(jiraInstance.service).deleteIssue(any(), itemId)
        pass
    
    def test_dontDeleteNotAddedItem(self):
        jira = JiraTracker()
        jiraInstance = self.getMockFor(jira)
        jira.selectProject([])
        jiraTrackerItem = mock()
        story = mock()
        when(jiraTrackerItem).underlying().thenReturn(story)
        when(story).GetStoryId().thenReturn(None)
        jira.delete(jiraTrackerItem)
        verify(jiraInstance.service, never).DeleteStory(any())
        pass 
    
    def test_canDeleteAllItems(self):
        jira = JiraTracker()
        jiraInstance = self.getMockFor(jira)
        jira.selectProject(["",""])
        item1 = RemoteIssue()
        item1.key = 1234
        item2 = RemoteIssue()
        item2.key = 12345
        when(jiraInstance.service).getIssuesFromJqlSearch(any(), any(), any()).thenReturn([item1,item2])
        when(jiraInstance.service).getComments(any(),any()).thenReturn([])
        jira.deleteAllItems()
        verify(jiraInstance.service).deleteIssue(any(), item1.key)
        verify(jiraInstance.service).deleteIssue(any(), item2.key)
        pass
    
    def test_noDeletionsWhenNoItems(self):
        jira = JiraTracker()
        jiraInstance = self.getMockFor(jira)
        jira.selectProject(["",""])
        when(jiraInstance.service).getIssuesFromJqlSearch(any(), any(), any()).thenReturn([])
        jira.deleteAllItems()
        verify(jiraInstance.service, never).deleteIssue(any(), any())
        pass
    
    def test_canUpdateExistingIssue(self):
        jira = JiraTracker()
        jiraInstance = self.getMockFor(jira)
        trackerItem = mock()
        values = [{'id':"fieldName" , 'values':"newValue"}, ]
        key = "12345"
        when(trackerItem).Id().thenReturn(key)
        when(trackerItem).piecesToUpdate().thenReturn(values)
        when(trackerItem).newComments().thenReturn([])
        jira.update(trackerItem) 
        verify(jiraInstance.service).updateIssue(self.auth_, key, values)
        pass

    def test_canGetCommentsForTicket(self):
        jira = JiraTracker()
        jiraInstance = self.getMockFor(jira)
        ticket = mock()
        key = "12345"
        twoComments = [{'created':datetime.now(), 'author':"lwoydziak", 'body':"Comment 1"}, {'created':datetime.now(), 'author':"lwoydziak", 'body':"Comment 1"}]
        when(ticket).Id().thenReturn(key)
        when(jiraInstance.service).getComments(any(),any()).thenReturn(twoComments)
        jira.updateItemWithComments(ticket)
        verify(jiraInstance.service).getComments(self.auth_, key)
        verify(ticket, times=2).addComment(any())
        pass
    
    def itemWithComments(self, testing):
        issue = RemoteIssue()
        issue.key = 1234
        return testing.itemWithCommentsOfType(JiraTrackerItem, issue)
    
    def test_canAddCommentsToTicket(self):
        jira = JiraTracker()
        jiraInstance = self.getMockFor(jira)
        testing = Testing()
        item = self.itemWithComments(testing)
        jira.updateCommentsFor(item)
        inorder.verify(jiraInstance.service).login(any(),any())
        inorder.verify(jiraInstance.service).addComment(self.auth_, testing.issue.key, {"body":testing.comment1})
        inorder.verify(jiraInstance.service).addComment(self.auth_, testing.issue.key, {"body":testing.comment2})
        pass
    
    def test_updateAddsNewComments(self):
        jira = JiraTracker()
        jiraInstance = self.getMockFor(jira)
        testing = Testing()
        item = self.itemWithComments(testing)
        jira.update(item)
        verify(jiraInstance.service, times=2).addComment(any(), any(), any())
        pass
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()