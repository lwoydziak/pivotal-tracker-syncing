'''
Created on May 30, 2012

@author: lwoydziak
'''
import unittest
from mockito.mocking import mock
from trackersyncby import TrackerSyncBy, ForwardSync, ReverseSync
from mockito.mockito import when, verify
from mockito.matchers import any
from mockito.verification import never
from unit_test_support import Testing
from mockito import inorder




class TrackerSyncByTest(unittest.TestCase):
    def test_canAddNewItemNotInTrackerAndwhenAddingUpdateItemBeforeUpdatingDetails(self):
        toTracker = mock()
        fromTracker = mock()
        itemToBeAdded = mock()
        detectedItem = mock()
        itemWithDetails = mock()
        TrackerItemType = mock()
        when(fromTracker).items(any()).thenReturn([detectedItem])
        when(toTracker).items(any()).thenReturn([])
        when(TrackerItemType).called().thenReturn(itemToBeAdded)
        when(toTracker).update(itemToBeAdded).thenReturn(itemWithDetails)
        syncByAddingItems = TrackerSyncBy.addingItemsOfType(TrackerItemType.called)
        syncByAddingItems(fromTracker, toTracker)
        inorder.verify(toTracker).items(any())
        inorder.verify(toTracker).update(itemToBeAdded)
        inorder.verify(toTracker).update(itemWithDetails)

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
        when(toTracker).update(itemToBeAdded).thenReturn(itemToBeAdded)
        syncByAddingItems = TrackerSyncBy.addingItemsOfType(TrackerItemType.called)
        syncByAddingItems(fromTracker, toTracker)
        verify(toTracker, times=2).update(itemToBeAdded)
        
    def test_addCommentsAndUpdateIssue(self):
        toTracker = mock()
        itemToAddCommentsTo = mock()
        itemToGetCommentsFrom = mock() 
        syncCommentsFor = TrackerSyncBy.syncingItem()
        when(toTracker).items(None).thenReturn(Testing.MockIterator([itemToAddCommentsTo]))
        when(itemToAddCommentsTo).canBeSyncedWith(itemToGetCommentsFrom).thenReturn(True)
        when(itemToAddCommentsTo).updatedAt().thenReturn(0)
        when(itemToGetCommentsFrom).updatedAt().thenReturn(1)
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
        when(item).updatedAt().thenReturn(0)
        when(otherItem).updatedAt().thenReturn(1)
        syncCommentsFor(otherItem, toTracker)
        verify(testFilter).calledWith(item)
        
    def test_commentsNotAddedIfItemIsNotTheSame(self):
        toTracker = mock()
        item = mock()
        otherItem = mock()
        syncCommentsFor = TrackerSyncBy.syncingItem()
        when(toTracker).items(None).thenReturn(Testing.MockIterator([item]))
        when(item).canBeSyncedWith(otherItem).thenReturn(False)
        syncCommentsFor(otherItem, toTracker)
        verify(item, never).syncWith(any())
        verify(toTracker, never).update(item)
        
    def setupSync(self, syncDirection=ForwardSync):
        toTracker = mock()
        itemToSyncTo = mock()
        itemToSyncFrom = mock()
        syncCommentsFor = TrackerSyncBy.syncingItem(Direction=syncDirection)
        when(toTracker).items(None).thenReturn(Testing.MockIterator([itemToSyncTo]))
        return toTracker, itemToSyncTo, itemToSyncFrom, syncCommentsFor
        
    def test_syncIfItemIsMoreUpToDate(self):
        toTracker, itemToSyncTo, itemToSyncFrom, syncCommentsFor = self.setupSync()
        when(itemToSyncTo).updatedAt().thenReturn(0)
        when(itemToSyncFrom).updatedAt().thenReturn(1)
        when(itemToSyncTo).canBeSyncedWith(itemToSyncFrom).thenReturn(True)
        syncCommentsFor(itemToSyncFrom, toTracker)
        verify(itemToSyncTo).syncWith(itemToSyncFrom)
        verify(toTracker).update(itemToSyncTo)

    def test_doNotSyncIfItemIsLessUpToDate(self):
        toTracker, itemToSyncTo, itemToSyncFrom, syncCommentsFor = self.setupSync()
        when(itemToSyncTo).updatedAt().thenReturn(1)
        when(itemToSyncFrom).updatedAt().thenReturn(0)
        when(itemToSyncTo).canBeSyncedWith(itemToSyncFrom).thenReturn(True)
        syncCommentsFor(itemToSyncFrom, toTracker)
        verify(toTracker, never).update(itemToSyncTo)
        
    def test_reverseSyncGetsItemToSyncToFromCorrectTracker(self):
        toTracker, itemToSyncTo, itemToSyncFrom, syncCommentsFor = self.setupSync(ReverseSync)
        fromTracker = mock()
        when(fromTracker).items(None).thenReturn(Testing.MockIterator([itemToSyncFrom]))
        when(itemToSyncFrom).updatedAt().thenReturn(1)
        when(itemToSyncTo).updatedAt().thenReturn(0)
        when(itemToSyncTo).canBeSyncedWith(itemToSyncFrom).thenReturn(True)
        syncCommentsFor(itemToSyncFrom, toTracker, fromTracker)
        verify(itemToSyncFrom).syncWith(itemToSyncTo)
        verify(fromTracker).update(itemToSyncFrom)
        
    def test_rightItemReturnedWhenMoreThanOneItemReturnedForForwardSync(self):
        toTracker = mock()
        items = [mock(), mock(), mock()]
        when(toTracker).items(any()).thenReturn(Testing.MockIterator([items[1],items[2]]))
        when(items[1]).canBeSyncedWith(items[0]).thenReturn(False)
        when(items[2]).canBeSyncedWith(items[0]).thenReturn(True)
        forwardSync = ForwardSync(mock().function, items[0], toTracker, None)
        forwardSync.obtainItem()
        verify(items[2]).canBeSyncedWith(items[0])
        
    def test_rightItemReturnedWhenMoreThanOneItemReturnedForReverseSync(self):
        toTracker = mock()
        items = [mock(), mock(), mock()]
        when(toTracker).items(any()).thenReturn(Testing.MockIterator([items[1],items[2]]))
        when(items[1]).canBeSyncedWith(items[0]).thenReturn(False)
        when(items[2]).canBeSyncedWith(items[0]).thenReturn(True)
        forwardSync = ReverseSync(mock().function, items[0], toTracker, None)
        forwardSync.obtainItem()
        verify(items[2]).canBeSyncedWith(items[0])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()