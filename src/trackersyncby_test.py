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
        when(toTracker).items(any()).thenReturn([])
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
        when(toTracker).items(any()).thenReturn(Testing.MockIterator([detectedItem]))
        when(detectedItem).canBeSyncedWith(detectedItem).thenReturn(True)
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
        when(toTracker).items(filterValue).thenReturn(Testing.MockIterator([detectedItem]))
        when(filterFunction).calledWith(detectedItem).thenReturn(filterValue)
        when(detectedItem).canBeSyncedWith(detectedItem).thenReturn(True)
        syncByAddingItems = TrackerSyncBy.addingItemsOfType(None, filterFunction.calledWith)
        syncByAddingItems(fromTracker, toTracker)
        verify(toTracker).items(filterValue)
        
    def test_whenMultipleItemsMatchFilterAndItemsCanNotBeSyncedWithThenAddNewItem(self):
        toTracker = mock()
        fromTracker = mock()
        detectedItem = mock()
        when(fromTracker).items(any()).thenReturn([detectedItem])
        when(toTracker).items(any()).thenReturn(Testing.MockIterator([detectedItem,detectedItem]))
        when(detectedItem).canBeSyncedWith(detectedItem).thenReturn(False).thenReturn(True)
        syncByAddingItems = TrackerSyncBy.addingItemsOfType(None)
        syncByAddingItems(fromTracker, toTracker)
        verify(toTracker, never).update()
                
    def test_whenMultipleItemsMatchFilterAndItemCanBeSyncedWithThenDoNotAddNewItem(self):
        toTracker = mock()
        fromTracker = mock()
        detectedItem = mock()
        TrackerItemType = mock()
        itemToBeAdded = mock()
        when(fromTracker).items(any()).thenReturn([detectedItem])
        when(toTracker).items(any()).thenReturn(Testing.MockIterator([detectedItem,detectedItem]))
        when(detectedItem).canBeSyncedWith(detectedItem).thenReturn(False)
        when(TrackerItemType).called().thenReturn(itemToBeAdded)
        syncByAddingItems = TrackerSyncBy.addingItemsOfType(TrackerItemType.called)
        syncByAddingItems(fromTracker, toTracker)
        verify(toTracker).update(itemToBeAdded)
        
    def test_addCommentsAndUpdateIssue(self):
        toTracker = mock()
        itemToAddCommentsTo = mock()
        itemToGetCommentsFrom = mock()
        syncCommentsFor = TrackerSyncBy.syncingItem()
        when(toTracker).items(None).thenReturn(Testing.MockIterator([itemToAddCommentsTo]))
        when(itemToAddCommentsTo).canBeSyncedWith(itemToGetCommentsFrom).thenReturn(True)
        syncCommentsFor(itemToGetCommentsFrom, toTracker)
        verify(itemToAddCommentsTo).syncWith(itemToGetCommentsFrom)
        verify(toTracker).update(itemToAddCommentsTo)
        
    def test_doNotAddCommentsWhenItemNotFound(self):
        toTracker = mock()
        item = mock()
        syncCommentsFor = TrackerSyncBy.syncingItem()
        when(toTracker).items(None).thenRaise(StopIteration)
        syncCommentsFor(item, toTracker)
        verify(toTracker, never).update(item) 
        
    def test_onlyTakeCommentsFromIssueForByFilter(self):
        toTracker = mock()
        aTestItemFilter = mock()
        syncCommentsFor = TrackerSyncBy.syncingItem(aTestItemFilter.calledWith)
        when(toTracker).items(None).thenRaise(StopIteration)
        syncCommentsFor(None, toTracker)
        verify(aTestItemFilter).calledWith(None)
        
    def test_doNotAddUnnecessaryComments(self):
        toTracker = mock()
        item = mock()
        testFilter = mock()
        otherItem = mock()
        syncCommentsFor = TrackerSyncBy.syncingItem(FilteringOutCommentsFor=testFilter.calledWith)
        when(toTracker).items(None).thenReturn(Testing.MockIterator([item]))
        when(item).canBeSyncedWith(otherItem).thenReturn(True)
        syncCommentsFor(otherItem, toTracker)
        verify(testFilter).calledWith(item)
        
    def test_commentsNotAddedIfItemIsNotTheSame(self):
        toTracker = mock()
        item = mock()
        otherItem = mock()
        syncCommentsFor = TrackerSyncBy.syncingItem()
        when(toTracker).items(None).thenReturn(Testing.MockIterator([item]))
        when(otherItem).canBeSyncedWith(item).thenReturn(False)
        syncCommentsFor(otherItem, toTracker)
        verify(item, never).syncWith(any())
        verify(toTracker, never).update(item)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()