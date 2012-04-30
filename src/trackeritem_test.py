'''
Created on Apr 7, 2012

@author: lwoydziak
'''
import unittest
from trackeritem import TrackerItem

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
        self.assertEqual(item.newComments()[0], newComment)
        
    def test_canAddExistingComment(self):
        existingComment = {'id':1, 'text':"existing comment"}
        item = TrackerItem()
        item.addComment(existingComment)
        self.assertEqual(item.comments()[0], existingComment)
    
    def test_canCopyNewComments(self):
        item = TrackerItem()
        commentsToCopy = ["comment1", "comment2"]
        item.withNewComments(commentsToCopy)
        self.assertEqual(item.newComments(), commentsToCopy) 
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()