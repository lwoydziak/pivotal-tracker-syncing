'''
Created on May 30, 2012

@author: lwoydziak
'''
from datetime import time

def defaultFilter(item):
    return None
    

class TrackerSyncBy(object):
    '''
    classdocs
    '''

    @staticmethod
    def addingItemsOfType(TrackerItemType, MatchingFilter=defaultFilter):
        def addingItems_(fromTracker, toTracker):
            for item in fromTracker.items(None):
                forFilter = MatchingFilter(item)
                itemFound = False
                for found in toTracker.items(forFilter):
                    itemFound = found.canBeSyncedWith(item)
                    if itemFound:
                        break
                if itemFound:
                    continue
                newItem = TrackerItemType()
                newItem = toTracker.update(newItem)
                newItem.syncWith(item)
                toTracker.update(newItem)
        return addingItems_
    
    @staticmethod
    def syncingItem(FilterForItem=defaultFilter, FilteringOutCommentsFor=defaultFilter):
        def syncingDetails_(itemToSyncWith, toTracker):
            forFilter = FilterForItem(itemToSyncWith)
            try:
                item = next(toTracker.items(forFilter))
            except StopIteration:
                return
            else:
                itemUpdated =  item.updatedAt()
                otherItemUpdated = itemToSyncWith.updatedAt()
                if item.canBeSyncedWith(itemToSyncWith) and itemUpdated <= otherItemUpdated:
                    item.syncWith(itemToSyncWith)
                    FilteringOutCommentsFor(item)
                    toTracker.update(item)
        return syncingDetails_