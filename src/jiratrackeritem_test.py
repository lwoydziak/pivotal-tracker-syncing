'''
Created on Apr 10, 2012

@author: lwoydziak
'''
import unittest
from jiratrackeritem import JiraTrackerItem
from jiraticket import JiraTicket
from remoteissue import RemoteIssue
from datetime import datetime


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
        testIssue = RemoteIssue()
        description = "Test Description"
        testIssue.description = description
        item = JiraTrackerItem(testIssue)
        self.assertEqual(item.asRemoteItem(), testIssue.__dict__)
        
    def test_canGetItemId(self):
        testIssue = RemoteIssue()
        testId = "TEST-1234"
        testIssue.key = testId
        item = JiraTrackerItem(testIssue)
        self.assertEqual(item.Id(), testId)
        
    def test_summaryAsPeicesToUpdateReturnedWhenItemIsUpdatedWithSummary(self):
        testIssue = RemoteIssue()
        testIssue.key = "Some value"
        item = JiraTrackerItem(testIssue)
        summary = "new value"
        item.withSummary(summary)
        self.assertEqual(item.piecesToUpdate(), [{'id':"summary" , 'values':[summary,]}])
        
    def test_descriptionAsPeicesToUpdateReturnedWhenItemIsUpdatedWithDescription(self):
        testIssue = RemoteIssue()
        testIssue.key = "Some value"
        item = JiraTrackerItem(testIssue)
        description = "new value"
        item.withDescription(description)
        self.assertEqual(item.piecesToUpdate(), [{'id':"description" , 'values':[description,]}])
        
    def test_canAddNewCommentToIssue(self):
        testIssue = RemoteIssue()
        item = JiraTrackerItem(testIssue)
        newComment = "Comments work now"
        item.addComment(newComment)
        comments = item.newComments()
        existingComments = item.comments()
        self.assertEqual(comments[0], newComment)
        self.assertEqual(existingComments, [])
        
    def test_canAddExistingCommentToIssue(self):
        testIssue = RemoteIssue()
        item = JiraTrackerItem(testIssue)
        existingComment = {'created':datetime.now(), 'author':"lwoydziak", 'body':"Comment 1"}
        item.addComment(existingComment)
        comments = item.newComments()
        existingComments = item.comments()
        self.assertEqual(comments, [])
        self.assertEqual(existingComments[0], existingComment)
        
    def test_canCopyNewComments(self):
        item = JiraTrackerItem()
        commentsToCopy = ["comment1", "comment2"]
        item.withNewComments(commentsToCopy)
        self.assertEqual(item.newComments(), commentsToCopy)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()