'''
Created on May 3, 2012

@author: lwoydziak
'''


class Testing(object):
    '''
    classdocs
    '''
    
    def itemWithCommentsOfType(self, ItemType, issue):
        comment1 = "comment1"
        comment2 = "comment2"
        item = ItemType(issue)
        item.addComment(comment1)
        item.addComment(comment2)
        self.issue = issue
        self.comment1 = comment1
        self.comment2 = comment2
        return item
        