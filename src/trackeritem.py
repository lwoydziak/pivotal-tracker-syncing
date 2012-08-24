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
        self.status_ = None
        self.type_ = None
        self.requestor_ = None
        self.owner_ = None
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
        self.withType(item.type())
        self.withStatus(item.status())
        self.withRequestor(item.requestor())
        self.withOwner(item.owner())
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
        return self
    
    def status(self):
        return self.status_
    
    def withType(self, type):
        self.type_ = type
        return self
    
    def type(self):
        return self.type_
    
    def _convertToUtc(self, dateTime):
        return (dateTime + dateTime.utcoffset()).replace(tzinfo=None)
    
    def withRequestor(self, requestor):
        self.requestor_ = requestor
        return self
    
    def requestor(self):
        return self.requestor_
    
    def withOwner(self, owner):
        self.owner_ = owner
        return self
    
    def owner(self):
        return self.owner_
        