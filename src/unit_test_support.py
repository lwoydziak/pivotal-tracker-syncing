'''
Created on May 3, 2012

@author: lwoydziak
'''

from trackeritemcomment import TrackerItemComment


class Testing(object):
    '''
    classdocs
    '''
    
    def itemWithCommentsOfType(self, CommentType, ItemType, issue):
        comment1 = TrackerItemComment("comment1")
        comment2 = TrackerItemComment("comment2")
        item = ItemType(issue)
        item.addComment(CommentType(comment1))
        item.addComment(CommentType(comment2))
        self.issue = issue
        self.comment1 = comment1
        self.comment2 = comment2
        return item
    
    @staticmethod
    def stringOfAsOfSize(size):
        stringToReturn = ""
        for _ in range(1, size):
            stringToReturn += "a"
        return stringToReturn
    
    @staticmethod
    def MockIterator(mocks):
        for mock in mocks:
            yield mock
        