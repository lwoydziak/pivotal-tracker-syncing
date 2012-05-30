'''
Created on May 30, 2012

@author: lwoydziak
'''

class TrackerSyncBy(object):
    '''
    classdocs
    '''

    @staticmethod
    def addingItemsOfType(TrackerItemType):
        def addingItems_(fromTracker, toTracker, FilterMethod=None):
            for item in fromTracker.items(None):
                try:
                    forFilter = FilterMethod(item) if FilterMethod is not None else None 
                    next(toTracker.items(forFilter))
                except StopIteration:
                    newItem = TrackerItemType()
                    newItem.syncWith(item)
                    toTracker.update(newItem)
                    continue
        return addingItems_