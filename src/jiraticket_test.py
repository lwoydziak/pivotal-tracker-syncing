'''
Created on Apr 10, 2012

@author: lwoydziak
'''
import unittest
from jiraticket import JiraTicket
from jiraremotestructures import RemoteIssue, RemoteComponent, RemoteCustomFieldValue,\
    RemoteVersion
from datetime import datetime




class JiraTicket_Test(unittest.TestCase):
    def test_canGetName(self):
        testTicket = testRemoteIssueFactory()
        ticket = JiraTicket(testTicket)
        self.assertEqual(ticket.summary(),testTicket.summary) 
        pass
    
    def test_canSetSummary(self):
        testTicket = testRemoteIssueFactory()
        ticket = JiraTicket(testTicket)
        summary = "New"
        ticket.setSummary(summary)
        self.assertEqual(ticket.summary(),summary) 
        pass

    def test_canGetRemoteItemDictionary(self):
        testTicket = testRemoteIssueFactory()
        ticket = JiraTicket(testTicket)
        remoteItemDictionary = testTicket.__dict__
        remoteItemDictionary["affectsVersions"][0] = remoteItemDictionary["affectsVersions"][0].__dict__
        remoteItemDictionary["components"][0] = remoteItemDictionary["components"][0].__dict__
        remoteItemDictionary["customFieldValues"][0] = remoteItemDictionary["customFieldValues"][0].__dict__
        remoteItemDictionary["fixVersions"][0] = remoteItemDictionary["fixVersions"][0].__dict__
        self.assertEqual(ticket.asDictionary(),remoteItemDictionary)
        pass
    
    def test_canGetRemoteItemId(self):
        testTicket = testRemoteIssueFactory()
        ticket = JiraTicket(testTicket)
        self.assertEqual(ticket.Id(),testTicket.key)
        pass
    
    def test_canSetStatus(self):
        testTicket = testRemoteIssueFactory()
        ticket = JiraTicket(testTicket)
        statusId = 6
        ticket.setStatus(statusId)
        self.assertEqual(ticket.status(), statusId)
        
    def test_canGetUpdatedDate(self):
        testTicket = testRemoteIssueFactory()
        ticket = JiraTicket(testTicket)
        self.assertEqual(ticket.updatedAt(), testTicket.updated)
        
    def test_canGetReporter(self):
        testTicket = testRemoteIssueFactory()
        ticket = JiraTicket(testTicket)
        self.assertEqual(testTicket.reporter, ticket.reporter())
        
    def test_canUpdateReporter(self):
        testTicket = testRemoteIssueFactory()
        ticket = JiraTicket(testTicket)
        reporter = "me"
        ticket.setReporter(reporter)
        self.assertEqual(reporter, ticket.reporter())
        
    def test_canGetAssignee(self):
        testTicket = testRemoteIssueFactory()
        ticket = JiraTicket(testTicket)
        self.assertEqual(testTicket.assignee, ticket.assignee())
        
    def test_canUpdateAssignee(self):
        testTicket = testRemoteIssueFactory()
        ticket = JiraTicket(testTicket)
        assignee = "me"
        ticket.setAssignee(assignee)
        self.assertEqual(assignee, ticket.assignee())

def testRemoteIssueFactory():
    testRemoteVersion = RemoteVersion()
    testRemoteVersion.archived = False
    testRemoteVersion.id = "11639"
    testRemoteVersion.name = "Test"
    testRemoteVersion.releaseDate = None
    testRemoteVersion.released = False
    testRemoteVersion.sequence = 1
    
    testRemoteComponent = RemoteComponent()
    testRemoteComponent.id = "12032"
    testRemoteComponent.name = "Test"
    
    testRemoteCustomFieldValue = RemoteCustomFieldValue()
    testRemoteCustomFieldValue.customfieldId = "customfield_10164"
    testRemoteCustomFieldValue.key = None
    testRemoteCustomFieldValue.values = ["P3",]
    
    testRemoteIssue = RemoteIssue()
    testRemoteIssue.affectsVersions = [testRemoteVersion,]
    testRemoteIssue.assignee = "lwoydziak"
    testRemoteIssue.attachmentNames = []
    testRemoteIssue.components = [testRemoteComponent, ]
    testRemoteIssue.created = datetime(2012, 4, 10, 19, 58, 7)
    testRemoteIssue.customFieldValues = [testRemoteCustomFieldValue,]
    testRemoteIssue.description = "Test for lwoydziak to try JIRA API"
    testRemoteIssue.duedate = None
    testRemoteIssue.environment = None
    testRemoteIssue.fixVersions = [testRemoteVersion, ]
    testRemoteIssue.id = "12345"
    testRemoteIssue.key = "JEXT-57"
    testRemoteIssue.priority = "3"
    testRemoteIssue.project = "JEXT"
    testRemoteIssue.reporter = "lwoydziak"
    testRemoteIssue.resolution = None
    testRemoteIssue.status = "10004"
    testRemoteIssue.summary = "Test ticket for lwoydziak"
    testRemoteIssue.type = "3"
    testRemoteIssue.updated = datetime(2012, 4, 10, 19, 58, 7)
    testRemoteIssue.votes = 0
    return testRemoteIssue


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()