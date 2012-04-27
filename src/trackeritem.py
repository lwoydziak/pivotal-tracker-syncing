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
        self.withSummary(None)
        self.withDescription(None)
        
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

        