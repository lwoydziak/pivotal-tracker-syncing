'''
Created on Apr 7, 2012

@author: lwoydziak
'''

class TrackerItem(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.summary_ = None
        self.description_ = None
        self.newComments_ = []
        self.exisitingComments_ = []
        
    def withSummary(self, summary):
        self.summary_ = summary
        return self
    
    def summary(self):
        return self.summary_
    
    def withDescription(self, description):
        self.description_ = description
        return self
    
    def description(self):
        return self.description_
    
    def Id(self):
        return None
    
    def syncWith(self, item):
        self.withDescription(item.description())
        self.withSummary(item.summary())
        pass
    
    def addComment(self, newComment):
        if isinstance(newComment,str):
            self.newComments_.append(newComment)
            return
        self.exisitingComments_.append(newComment)
        
    def comments(self):
        return self.exisitingComments_
    
    def newComments(self):
        return self.newComments_

    def withNewComments(self, commentsToCopy):
        self.newComments_ = commentsToCopy
        return self

        