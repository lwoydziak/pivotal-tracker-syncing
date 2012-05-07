'''
Created on May 3, 2012

@author: lwoydziak
'''

class Testing(object):

    @staticmethod
    def canUpdateItemsIn(tracker, test):
        items = tracker.items()
        newSummary = "updated summary"
        newDescription = "yep - updated"
        items[0].withSummary(newSummary).withDescription(newDescription)
        tracker.update(items[0])
        items = tracker.items()
        test.assertEqual(items[0].summary(), newSummary)
        test.assertEqual(items[0].description(), newDescription)
        
    @staticmethod
    def addCommentToItemIn(tracker):
        items = tracker.items()
        aComment = "I am adding this comment"
        items[0].addComment(aComment)
        tracker.update(items[0])
        return aComment
      
        