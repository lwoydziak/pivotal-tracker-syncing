'''
Created on Apr 10, 2012

@author: lwoydziak
'''
import unittest
from jiratrackeritem import JiraTrackerItem
from jiraticket import JiraTicket
from jiraremotestructures import RemoteIssue
from datetime import datetime, date, tzinfo
from mockito.mockito import verify, when
from mockito.mocking import mock
from trackeritemstatus import TrackerItemStatus
from mappivotaltojirastatus import PivotalToJiraStatusMap
from collections import namedtuple
from timezoneutc import UTC
from trackeritemuser import JiraUser

JiraStatus = namedtuple('JiraStatus', ['id', 'name'])


class JiraTrackerItem_Test(unittest.TestCase):
    def test_changingSummaryChangesJiraTicketSummary(self):
        item = JiraTrackerItem()
        summary = "New"
        returnedItem = item.withSummary(summary)
        self.assertEqual(item.underlying().summary(), summary)
        self.assertEqual(returnedItem, item)
        pass
    
    def test_changingDescriptionChangesJiraTicketDescription(self):
        item = JiraTrackerItem()
        description = "New"
        returnedItem = item.withDescription(description)
        self.assertEqual(item.underlying().description(), description)
        self.assertEqual(returnedItem, item)
        pass
    
    def testIssue(self):
        testIssue = RemoteIssue()
        testIssue.key = "TEST-jti1234"
        return testIssue
    
    def test_canSeedWithTicket(self):
        testTicket = JiraTicket()
        summary = "Test Summary"
        testTicket.setSummary(summary)
        item = JiraTrackerItem(testTicket)
        self.assertEqual(item.summary(), summary)
        testIssue = RemoteIssue()
        description = "Test Description"
        testIssue.description = description
        item = JiraTrackerItem(testIssue)
        self.assertEqual(item.description(), description)
        
    def test_canGetItemAsRemoteItem(self):
        testIssue = self.testIssue()
        description = "Test Description"
        testIssue.description = description
        item = JiraTrackerItem(testIssue)
        self.assertEqual(item.asRemoteItem(), testIssue.__dict__)
        
    def test_canGetItemId(self):
        testIssue = self.testIssue()
        item = JiraTrackerItem(testIssue)
        self.assertEqual(item.Id(), testIssue.key)
        
    def test_summaryAsPeicesToUpdateReturnedWhenItemIsUpdatedWithSummary(self):
        testIssue = self.testIssue()
        item = JiraTrackerItem(testIssue)
        summary = "new value"
        item.withSummary(summary)
        self.assertEqual(item.piecesToUpdate(), [{'id':"summary" , 'values':[summary,]}])
        
    def test_summaryAsPiecesNotAddedWhenTryingToAddDuplicateSummary(self):
        testIssue = mock()
        item = JiraTrackerItem(testIssue)
        item.withSummary(testIssue.summary)
        self.assertEqual(item.piecesToUpdate(), [])
        
    def test_descriptionAsPeicesToUpdateReturnedWhenItemIsUpdatedWithDescription(self):
        testIssue = self.testIssue()
        item = JiraTrackerItem(testIssue)
        description = "new value"
        item.withDescription(description)
        self.assertEqual(item.piecesToUpdate(), [{'id':"description" , 'values':[description,]}])
        
    def test_descriptionAsPiecesNotAddedWhenTryingToAddDuplicateDescription(self):
        testIssue = mock()
        item = JiraTrackerItem(testIssue)
        item.withDescription(testIssue.description)
        self.assertEqual(item.piecesToUpdate(), [])
        
    def test_canAddNewCommentToIssue(self):
        item = JiraTrackerItem()
        newComment = "Comments work now"
        item.addComment(newComment)
        comments = item.comments('new')
        existingComments = item.comments()
        self.assertEqual(comments[0], newComment)
        self.assertEqual(existingComments, [])
        
    def test_canAddExistingCommentToIssue(self):
        item = JiraTrackerItem()
        existingComment = {'created':datetime.now(), 'author':"lwoydziak", 'body':"Comment 1"}
        item.addComment(existingComment, "existing")
        comments = item.comments('new')
        existingComments = item.comments()
        self.assertEqual(comments, [])
        self.assertEqual(existingComments[0], existingComment)
        
    def test_canCopyNewComments(self):
        item = JiraTrackerItem()
        commentsToCopy = ["comment1", "comment2"]
        item.withComments(commentsToCopy)
        self.assertEqual(item.comments('new'), commentsToCopy)
        
    def test_canGetJiraUrlFromItem(self):
        item = JiraTrackerItem()
        updateUrl = "http://www.updated.com"
        item.withJiraUrl(updateUrl)
        self.assertEqual(item.jiraUrl(), updateUrl)
        
    def test_canGetJiraKeyOnStory(self):
        testIssue = self.testIssue()
        item = JiraTrackerItem(testIssue)
        self.assertEqual(item.jiraKey(), testIssue.key)
        
    def test_canCopyItemSpecificDataToAnotherItem(self):
        modified = mock()
        testIssue = self.testIssue()
        testIssueUrl = "http://www.jira.com/browse/TEST-12345"
        source = JiraTrackerItem(testIssue)
        source.withJiraUrl(testIssueUrl)
        source.copyTypeSpecificDataTo(modified)
        verify(modified).withJiraKey(testIssue.key)
        verify(modified).withJiraUrl(testIssueUrl)
        
    def test_ifJiraKeyIsSameThenCanSyncWithOtherItem(self):
        testIssue = self.testIssue()
        item = JiraTrackerItem(testIssue)
        toSyncWith = mock()
        when(toSyncWith).jiraKey().thenReturn(testIssue.key)
        self.assertTrue(item.canBeSyncedWith(toSyncWith))
    
    def test_ifJiraKeyIsDifferentThenCannotSyncWithOtherItem(self):
        testIssue = self.testIssue()
        item = JiraTrackerItem(testIssue)
        toSyncWith = mock()
        when(toSyncWith).jiraKey().thenReturn("blah")
        self.assertFalse(item.canBeSyncedWith(toSyncWith))
        
    def test_cannotSyncWithNoItem(self):
        item = JiraTrackerItem()
        self.assertFalse(item.canBeSyncedWith(None))
        
    def test_canAddStatus(self):
        PivotalToJiraStatusMap().addMapping(jira="Closed", pivotal="Accepted")
        jiraStatus = JiraStatus(6, "Closed")
        PivotalToJiraStatusMap().insert(jiraStatus)
        item = JiraTrackerItem()
        statusId = 6
        ticket = JiraTicket()
        ticket.setStatus(statusId)
        status = TrackerItemStatus(ticket)
        item.withStatus(status)
        self.assertEqual(item.status(), status)
        self.assertEqual(item.piecesToUpdate(), [{'id':"status", 'values':['',]},])
        PivotalToJiraStatusMap().reset()
        
    def test_statusAsPiecesNotAddedWhenTryingToAddDuplicateStatus(self):
        testIssue = mock()
        item = JiraTrackerItem(testIssue)
        duplicateStatus = item.status()
        item.withStatus(duplicateStatus)
        self.assertEqual(item.piecesToUpdate(), [])
        
    def test_canGetStatusWhenAddedViaUnderlying(self):
        PivotalToJiraStatusMap().addMapping(jira="Closed", pivotal="Accepted") 
        jiraStatus = JiraStatus(6, "Closed")
        PivotalToJiraStatusMap().insert(jiraStatus)
        testTicket = JiraTicket()
        testTicket.setStatus(jiraStatus.id)
        item = JiraTrackerItem(testTicket)
        self.assertEqual(item.status().jira(), [jiraStatus.name])
        PivotalToJiraStatusMap().reset()

    def test_canGetUpdatedAtDateTime(self):
        testTicket = JiraTicket()
        date = datetime.now()
        testTicket.details_.updated = date
        timezone = UTC()
        item = JiraTrackerItem(testTicket, timezone)
        self.assertEqual(date, item.updatedAt())
        self.assertEqual(None, item.updatedAt().tzinfo)
        
    def test_settingJiraKeyDoesNotChangeUnderlying(self):
        testTicket = mock()
        item = JiraTrackerItem(testTicket)
        tryKey = "jiraKey"
        item.withJiraKey(tryKey)
        self.assertNotEqual(tryKey, item.jiraKey())
        
    def test_jiraItemTypeIsBug(self):
        item = JiraTrackerItem()
        self.assertEqual("bug", item.type())
        
    def test_canChangeReporter(self):
        item = JiraTrackerItem()
        reporter = "me"
        item.withRequestor(JiraUser(reporter))
        self.assertEqual(reporter, item.requestor().jira())
        self.assertEqual(reporter, item.underlying().reporter())
        self.assertEqual(item.piecesToUpdate(), [{'id':"reporter" , 'values':[reporter,]}])
        
    def test_doNotAddDuplicateReporter(self):
        testTicket = mock()
        item = JiraTrackerItem(testTicket)
        item.withRequestor(JiraUser(testTicket.reporter)) 
        self.assertEqual(item.piecesToUpdate(), [])
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()