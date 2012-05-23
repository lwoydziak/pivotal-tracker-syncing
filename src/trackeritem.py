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
        self.comments_ = {'new':[], 'existing':[]}
        
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
        self.withComments(item.comments())
        item.copyTypeSpecificDataTo(self)
        pass
    
    def addComment(self, comment, kind='new'):
        existingComments = self.comments_['existing']
        newComments = self.comments_['new']
        if comment in existingComments or comment in newComments:
            return
        self.comments_[kind].append(comment)
        
    def comments(self, kind='existing'):
        return self.comments_[kind]

    def withComments(self, commentsToCopy, kind='new'):
        for comment in commentsToCopy:
            self.addComment(comment, kind)
        return self
    
    def copyTypeSpecificDataTo(self, item):
        pass
    
    def withStatus(self, status):
        self.status_ = status
    
    def status(self):
        return self.status_
    
    
    

        