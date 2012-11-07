'''
Created on Sep 6, 2012

@author: lwoydziak
'''
import unittest
from filterfunctions import matchingAJiraTicket, JiraIssue, andDontFilterComments, PivotalIssue, andOmitPivotalTrackerCreatedComments, dateFilterGenerator
from mockito.mocking import mock
from mockito.mockito import when
from datetime import datetime

class FilterFunctionsTest(unittest.TestCase):
    def test_filterMatchingAJiraTicketReturnsFilterAsSpecified(self):
        jiraTicket = mock()
        when(jiraTicket).jiraKey().thenReturn("blah")
        outputFilter = matchingAJiraTicket(jiraTicket)
        self.assertEqual(outputFilter, "\"blah\" includedone:true")
    
    def test_filterForJiraIssueReturnsFilterAsSpecified(self):
        item = mock()
        when(item).jiraKey().thenReturn("blah")
        outputFilter = JiraIssue(item)
        self.assertEqual(outputFilter, "issuekey = \"blah\"")

    def test_filterAndDontFilterComments(self):
        self.assertEqual(andDontFilterComments(mock()), None)
        
    def test_filterForPivotalIssueReturnsFilterAsSpecified(self):
        jiraTicket = mock()
        when(jiraTicket).jiraKey().thenReturn("blah")
        outputFilter = PivotalIssue(jiraTicket)
        self.assertEqual(outputFilter, "\"blah\" includedone:true")
        
    def test_filterAndOmitPivotalTrackerCreateCommentsRemovesComments(self):
        item = mock()
        comments=["A Pivotal Tracker story",]
        when(item).comments("new").thenReturn(comments)
        andOmitPivotalTrackerCreatedComments(item)
        self.assertListEqual(comments, [])
        
    def test_filterDateFilterGeneratorReturnsFilterSpecified(self):
        date = datetime(2011, 2, 6)
        self.assertDictEqual(dateFilterGenerator(date), 
                             {'jira':" and updatedDate > \"2011/02/06 00:00\"", 'pivotal':"modified_since:02/06/2011 includedone:true"})
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()