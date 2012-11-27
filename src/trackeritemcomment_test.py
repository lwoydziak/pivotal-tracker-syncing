'''
Created on Nov 19, 2012

@author: lwoydziak
'''
import unittest
from trackeritemcomment import TrackerItemComment, JiraComment, PivotalComment
from jiraremotestructures import RemoteComment
from mockito.mockito import when
from mockito.mocking import mock


class TrackerItemCommentTest(unittest.TestCase):
    def test_canGetTextForTrackerItemComment(self):
        setText = "blah"
        comment = TrackerItemComment(setText)
        self.assertEqual(comment.text(), setText)
        
    def test_canGetJiraDictionay(self):
        setText = "blah"
        comment = TrackerItemComment(setText)
        jiraComment = JiraComment(comment)
        self.assertDictEqual(jiraComment.forJira(), {'body':setText})
        
    def test_canGetTextFromRemoteComment(self):
        remoteComment = RemoteComment()
        comment = JiraComment(remoteComment)
        self.assertEqual(comment.text(), remoteComment.body)
        
    def test_canCheckEquality(self):
        setText = "blah"
        comment = TrackerItemComment(setText)
        another = JiraComment(comment)
        self.assertEqual(comment, another)
        
    def test_canCheckInequality(self):
        setText = "blah"
        comment = TrackerItemComment(setText)
        remoteComment = RemoteComment()
        another = JiraComment(remoteComment)
        self.assertNotEqual(comment, another)
        
    def test_canGetTextFromPivotalComment(self):
        setText = "blah"
        pivotalComment = mock()
        when(pivotalComment).GetText().thenReturn(setText)
        comment = PivotalComment(pivotalComment)
        self.assertEqual(comment.text(), setText)
        
    def test_canGetLenghtOfPivotalComment(self):
        setText = "blah"
        pivotalComment = mock()
        when(pivotalComment).GetText().thenReturn(setText)
        comment = PivotalComment(pivotalComment)
        self.assertEqual(len(comment), len(setText))
        
    def test_commentEqualsSelf(self):
        setText = "blah"
        comment = TrackerItemComment(setText)
        self.assertEqual(comment, comment)
    
    def test_commentNotEqaulsOther(self):
        setText = "blah"
        comment = TrackerItemComment(setText)
        otherText = "other"
        other = TrackerItemComment(otherText)
        self.assertNotEqual(comment, other)
        
    def test_baseForPivotalIsNone(self):
        setText = "blah"
        comment = TrackerItemComment(setText)
        self.assertEqual(comment.forPivotal(), None)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()