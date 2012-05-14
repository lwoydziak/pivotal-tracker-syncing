'''
Created on May 3, 2012

@author: lwoydziak
'''

class Testing(object):

    @staticmethod
    def canUpdateItemsIn(tracker, test):
        item = next(tracker.items())
        newSummary = "updated summary"
        newDescription = "yep - updated"
        item.withSummary(newSummary).withDescription(newDescription)
        tracker.update(item)
        item = next(tracker.items())
        test.assertEqual(item.summary(), newSummary)
        test.assertEqual(item.description(), newDescription)
        
    @staticmethod
    def addCommentToItemIn(tracker):
        item = next(tracker.items())
        aComment = "I am adding this comment"
        item.addComment(aComment)
        tracker.update(item)
        return aComment
      
        