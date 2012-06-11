'''
Created on May 30, 2012

@author: lwoydziak
'''

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
                newItem.syncWith(item)
                toTracker.update(newItem)
        return addingItems_
    
    @staticmethod
    def syncingItem(FilterForItem=defaultFilter, FilteringOutCommentsFor=defaultFilter):
        def addingComments_(itemToSyncWith, toTracker):
            forFilter = FilterForItem(itemToSyncWith)
            try:
                item = next(toTracker.items(forFilter))
            except StopIteration:
                return
            else:
                if item.canBeSyncedWith(itemToSyncWith):
                    item.syncWith(itemToSyncWith)
                    FilteringOutCommentsFor(item)
                    toTracker.update(item)
        return addingComments_