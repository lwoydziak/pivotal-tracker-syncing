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
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()