'''
Created on May 30, 2012

@author: lwoydziak
'''
from datetime import time

def defaultFilter(item):
    return None

class Sync(object):
    def __init__(self):
        self.filter_ = None
        self.to_ = None
        self.from_ = None
        self.toTracker_ = None
        self.fromTracker_ = None  

    def needsSync(self):
        if self.from_ is None or self.from_.canBeSyncedWith(self.to_) is False:
            return False
        toBeSyncedItemUpdated = self.from_.updatedAt()
        toSyncWithItemUpdated = self.to_.updatedAt()
        return toBeSyncedItemUpdated <= toSyncWithItemUpdated
    
class ForwardSync(Sync):
    def __init__(self, filter, given, toTracker, unused):
        super(ForwardSync, self).__init__()
        self.filter_ = filter
        self.to_ = given
        self.from_ = None
        self.toTracker_ = toTracker
    
    def obtainItem(self):
        for item in self.toTracker_.items(self.filter_(self.to_)):
            if item.canBeSyncedWith(self.to_):
                self.from_ = item

    def sync(self, FilteringOutCommentsFor): 
        self.from_.syncWith(self.to_)
        FilteringOutCommentsFor(self.from_)
        self.toTracker_.update(self.from_)


class ReverseSync(Sync):
    def __init__(self, filter, given, trackerToGetItemToSync, trackerToSyncTo):
        super(ReverseSync, self).__init__()
        self.filter_ = filter
        self.to_ = given
        self.from_ = None
        self.toTracker_ = trackerToSyncTo
        self.fromTracker_ = trackerToGetItemToSync
    
    def obtainItem(self):
        for item in self.fromTracker_.items(self.filter_(self.to_)):
            if item.canBeSyncedWith(self.to_):
                self.from_ = item

    def sync(self, FilteringOutCommentsFor): 
        self.to_.syncWith(self.from_)
        FilteringOutCommentsFor(self.to_)
        self.toTracker_.update(self.to_)


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
    def syncingItem(FilterForItem=defaultFilter, FilteringOutCommentsFor=defaultFilter, Direction=ForwardSync):
        def syncingDetails_(given, toTracker, fromTracker=None):
            syncer = Direction(FilterForItem, given, toTracker, fromTracker)
            try:
                syncer.obtainItem()
            except StopIteration:
                return
            else:
                if syncer.needsSync():
                    syncer.sync(FilteringOutCommentsFor)
        return syncingDetails_
