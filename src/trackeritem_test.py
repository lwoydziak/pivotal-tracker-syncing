'''
Created on Apr 7, 2012

@author: lwoydziak
'''
import unittest
from trackeritem import TrackerItem
from mockito.mocking import mock
from mockito.mockito import verify, when
from trackeritemstatus import TrackerItemStatus
from mockito.matchers import any

class TrackerItemTests(unittest.TestCase):
    def test_canConstructTestItem(self):
        item = TrackerItem()
        self.assertEqual(type(item), TrackerItem)
        pass
    
    def test_canAddSummary(self):
        item = TrackerItem()
        summary = "test"
        item.withSummary(summary)
        self.assertEqual(item.summary(), summary)
        
    def test_canMethodChainSummary(self):
        item = TrackerItem().withSummary("blah")
        self.assertEqual(item.summary(), "blah")
        
    def test_canAddDescription(self):
        item = TrackerItem()
        description = "test"
        item.withDescription(description)
        self.assertEqual(item.description(), description)
        
    def test_canGetId(self):
        item = TrackerItem()
        self.assertEqual(item.Id(), None)
        
    def test_canSyncSummaryWithItem(self):
        summaryToSync = "Check for this"
        item1 = TrackerItem().withSummary("summary")
        item2 = TrackerItem().withSummary(summaryToSync)
        item1.syncWith(item2)
        self.assertEqual(item1.summary(), summaryToSync)
        
    def test_canSyncDescriptionWithItem(self):
        descriptionToSync = "Check for this"
        item1 = TrackerItem().withDescription("summary")
        item2 = TrackerItem().withDescription(descriptionToSync)
        item1.syncWith(item2)
        self.assertEqual(item1.description(), descriptionToSync)
        
    def test_canAddNewComment(self):
        newComment = "new Comment"
        item = TrackerItem()
        item.addComment(newComment)
        self.assertEqual(item.comments('new')[0], newComment)
        
    def test_canAddExistingComment(self):
        existingComment = {'id':1, 'text':"existing comment"}
        item = TrackerItem()
        item.addComment(existingComment, "existing")
        self.assertEqual(item.comments()[0], existingComment)
    
    def test_canCopyNewComments(self):
        item = TrackerItem()
        commentsToCopy = ["comment1", "comment2"]
        item.withComments(commentsToCopy)
        self.assertEqual(item.comments('new'), commentsToCopy)
        
    def test_duplicateCommentIsNotAdded(self):
        item = TrackerItem()
        comment1 = "Don't duplicate me"
        item.addComment(comment1, 'existing')
        item.addComment(comment1, 'existing')
        item.addComment(comment1, 'new')
        self.assertEqual(len(item.comments('new')), 0)
        self.assertEqual(len(item.comments('existing')), 1)
        
    def test_canSyncCommentsWithItem(self):
        commentsToSync = ["check for this"]
        commentsSeed = ["existing comment"]
        itemTarget = TrackerItem().withComments(commentsSeed, 'existing')
        itemSource = TrackerItem().withComments(commentsToSync, 'existing')
        itemTarget.syncWith(itemSource)
        self.assertEqual(len(itemTarget.comments('existing')), 1)
        self.assertEqual(len(itemTarget.comments('new')), 1)
        self.assertEqual(itemTarget.comments('new'), commentsToSync)
        
    def test_syncItemSpecificData(self):
        otherItem = mock()
        thisItem = TrackerItem()
        when(otherItem).comments().thenReturn([])
        thisItem.syncWith(otherItem)
        verify(otherItem).copyTypeSpecificDataTo(thisItem)
        
    def test_noSpecificItemDataIsCopiedForBaseType(self):
        startingItem = TrackerItem()
        endingItem = startingItem
        itemToCopySpecificDataFrom = TrackerItem()
        itemToCopySpecificDataFrom.copyTypeSpecificDataTo(endingItem)
        self.assertEqual(startingItem, endingItem)
        
    def test_canAddStatus(self):
        item = TrackerItem()
        status = TrackerItemStatus()
        item.withStatus(status)
        self.assertEqual(item.status(), status)
        
    def test_canAddType(self):
        item = TrackerItem()
        type = "A Type"
        item.withType(type)
        self.assertEqual(type, item.type())
        
    def test_canSyncType(self):
        type = "A Type"
        typeB = "B Type"
        item1 = TrackerItem().withType(type)
        item2 = TrackerItem().withType(typeB)
        item2.syncWith(item1)
        self.assertEqual(type, item2.type())
        
    def test_canSyncStatus(self):
        statusA = TrackerItemStatus()
        statusB = TrackerItemStatus()
        item1 = TrackerItem().withStatus(statusA)
        item2 = TrackerItem().withStatus(statusB)
        item2.syncWith(item1)
        syncedStatus = item2.status()
        self.assertTrue(syncedStatus is statusA)
        
    def test_canGetUtcTime(self):
        class testing(object):
            def __init__(self, mocking):
                self.mocking_ = mocking
            
            def __add__(self, other):
                return self.mocking_.add(other)
            
            def utcoffset(self):
                return self.mocking_.utcoffset()
                
        item = TrackerItem()
        dateTime = mock()
        testDateTime = testing(dateTime)
        deltaTime = mock()
        finalTime = mock()
        when(dateTime).utcoffset().thenReturn(deltaTime)
        when(dateTime).add(deltaTime).thenReturn(finalTime)
        when(finalTime).replace(tzinfo=None).thenReturn(1)
        newDateTime = item._convertToUtc(testDateTime)
        self.assertEqual(newDateTime, 1)  
        
    def test_canAddRequestor(self):
        item = TrackerItem()
        requestor = "me"
        item.withRequestor(requestor)
        self.assertEqual(requestor, item.requestor())   
                
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()