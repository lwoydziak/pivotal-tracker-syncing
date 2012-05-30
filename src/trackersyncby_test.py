'''
Created on May 30, 2012

@author: lwoydziak
'''
import unittest
from mockito.mocking import mock
from trackersyncby import TrackerSyncBy
from mockito.mockito import when, verify
from mockito.matchers import any
from mockito.verification import never
from unit_test_support import Testing




class TrackerSyncByTest(unittest.TestCase):
    def test_canAddNewItemsWhenItemsNotInTracker(self):
        toTracker = mock()
        fromTracker = mock()
        itemToBeAdded = mock()
        detectedItem = mock()
        TrackerItemType = mock()
        when(fromTracker).items(any()).thenReturn([detectedItem])
        when(toTracker).items(any()).thenRaise(StopIteration())
        when(TrackerItemType).called().thenReturn(itemToBeAdded)
        syncByAddingItems = TrackerSyncBy.addingItemsOfType(TrackerItemType.called)
        syncByAddingItems(fromTracker, toTracker)
        verify(itemToBeAdded).syncWith(detectedItem)
        verify(TrackerItemType).called()
        verify(toTracker).update(itemToBeAdded)

    def test_doNotAddItemWhenItemInTracker(self):
        toTracker = mock()
        fromTracker = mock()
        detectedItem = mock()
        when(fromTracker).items(any()).thenReturn([detectedItem])
        when(toTracker).items(any()).thenReturn(Testing.MockIterator(detectedItem))
        syncByAddingItems = TrackerSyncBy.addingItemsOfType(None)
        syncByAddingItems(fromTracker, toTracker)
        verify(toTracker, never).update()
    
    def test_doNotAddItemWhenNoItemToAdd(self):
        toTracker = mock()
        fromTracker = mock()
        when(fromTracker).items(any()).thenReturn([])
        syncByAddingItems = TrackerSyncBy.addingItemsOfType(None)
        syncByAddingItems(fromTracker, toTracker)
        verify(toTracker, never).update()
        
    def test_filterFunctionIsUsed(self):
        toTracker = mock()
        fromTracker = mock()
        detectedItem = mock()
        filterValue = "filter"
        filterFunction = mock()
        when(fromTracker).items(any()).thenReturn([detectedItem])
        when(toTracker).items(filterValue).thenReturn(Testing.MockIterator(detectedItem))
        when(filterFunction).called(detectedItem).thenReturn(filterValue)
        syncByAddingItems = TrackerSyncBy.addingItemsOfType(None)
        syncByAddingItems(fromTracker, toTracker, filterFunction.called)
        verify(toTracker).items(filterValue)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()